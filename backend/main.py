from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.responses import JSONResponse
import pandas as pd
import io
import configparser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('CONFIG.INI')

key = config.get('OPENAI', 'KEY')
model = config.get('OPENAI', 'MODEL')

llm = ChatOpenAI(
    model=model,
    temperature=0,
    api_key=key
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            '''You are working with a pandas DataFrame in Python named `df`. Below you will find information about the DataFrame:

                **Columns:** {df_columns}  
                **DataType:** {types}  
                **UniqueValues:** {unique_object}

                Your task is to generate Python pandas code that accurately addresses the user query using the DataFrame. The code must be directly executable in Python. 

                **Example:**  
                **Columns:** ["Name", "Age", "Gender"]  
                **DataType:** ["object", "float64", "object"]  
                **UniqueValues:** {{"Name": ["Shahzaib", "Anusha", "Shahrukh"], "Age": [24, 29, 19], "Gender": ["Male", "Female"]}}  
                **Question:** Give me all males  

                **Output:** df = df[df['Gender'] == 'Male']  

                Ensure that your output is a single line of Python code that performs the requested operation on the DataFrame. Do not include extra text or formatting.
                ''',
        ),
        ("human", "{input_question}"),
    ]
)

chain = prompt | llm

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    # Check if the uploaded file is a CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    # Read the file contents into a Pandas DataFrame
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

    # Convert the DataFrame to JSON
    df_json = df.to_json(orient="records")

    # Return the DataFrame as a JSON response
    return JSONResponse(content={"data": df_json})


class DataRow(BaseModel):
    dataframe: List[Dict[str, Any]]
    question: str

@app.post("/filter")
async def json_to_dataframe(data: DataRow):
    try:
        # Convert list of dicts to DataFrame
        df = pd.DataFrame(data.dataframe)

        # Prepare a local variable dictionary to be used by exec
        local_vars = {"df": df}

        # Check DataFrame creation
        if df.empty:
            raise ValueError("DataFrame is empty")

        df_columns = df.columns.tolist()
        df_dtype = df.dtypes.tolist()
        types = [str(typ) for typ in df_dtype]

        # Get unique values for each column
        unique_values = df.apply(lambda x: x.unique())

        unique_object = {column: unique_values[column].tolist() for column in df.columns}

        ai_response = chain.invoke( { "input_question": data.question, "df_columns": df_columns, "types": types, "unique_object": unique_object } )

        # Simulate AI response for testing (usually you would call an actual AI service here)
        
        print(ai_response)
        executable_code = ai_response.content
        print("Executing code:", executable_code)

        # Execute code to filter DataFrame
        try:
           # Execute the code in the local context
            exec(executable_code, globals(), local_vars)
        except Exception as e:
            print(f"Error executing code: {e}")
            return {"error": "Code execution failed"}
        
        df = local_vars["df"]

        print("Filtered DataFrame:", df)

        # # Return AI response and filtered DataFrame (converted to JSON for simplicity)
        # return {
        #     "ai_response": ai_response,
        #     "filtered_dataframe": df.to_json(orient="records")
        # }
        # Return the DataFrame as a JSON response
        return JSONResponse(content={"ai_response": executable_code,"filtered_dataframe": df.to_json(orient="records")})
    
    except ValueError as e:
        print(f"Error converting JSON to DataFrame: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}
    

