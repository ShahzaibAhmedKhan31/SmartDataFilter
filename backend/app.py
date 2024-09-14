from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.responses import JSONResponse
import pandas as pd
import io
from handleFilteration import HandleFilteration


handle_filteration = HandleFilteration()

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
        df = pd.DataFrame(data.dataframe)

        if df.empty:
            raise HTTPException(status_code=400, detail="DataFrame is empty")

        df_columns = df.columns.tolist()
        df_dtype = df.dtypes.tolist()
        types = [str(typ) for typ in df_dtype]

        unique_values = df.apply(lambda x: x.unique())
        unique_object = {column: unique_values[column].tolist() for column in df.columns}

        ai_response = handle_filteration.tackleUserChainAnswer(data.question, df_columns, types)

        if ai_response == 'Yes':
            filter_ai_respose_code = handle_filteration.filterChainAnswer(data.question, df_columns, types, unique_object)
            print(filter_ai_respose_code)
            filtered_ai_dataframe = handle_filteration.filterDataFrame(df, filter_ai_respose_code)
            return JSONResponse(
                content={
                    "ai_response": filter_ai_respose_code,
                    "filtered_dataframe": filtered_ai_dataframe.to_json(orient="records")
                }
            )
        else:
            raise HTTPException(status_code=400, detail="Your query is not relevant to the data.")

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


