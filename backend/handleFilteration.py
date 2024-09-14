from fastapi import HTTPException
import configparser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('CONFIG.INI')

class HandleFilteration():


    def __init__(self):

        self.model = config.get('OPENAI', 'MODEL')
        if not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = config.get('OPENAI', 'KEY')
        self.tackle_user_input_chain = self.tackleUserInputLLMChain()
        self.filter_chain = self.FilterLLMChain()
        
    
    def FilterLLMChain(self):
        llm = ChatOpenAI( model=self.model, temperature=0)
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

        print("Filter LLM Chain is successfully created!!!")
        return chain
        


    def tackleUserInputLLMChain(self):
        llm = ChatOpenAI(model=self.model, temperature=0)
        prompt = ChatPromptTemplate.from_messages([
        ("system", '''Hello, you are a helpful assistant that analyze the user query and determine whether it is relevant to the dataframe. Below you will find information about a dataframe's columns and their data types:
                    - **Columns:** {df_columns}  
                    - **DataType:** {types}

                    Your task is to analyze the user query and determine whether it is relevant to the dataframe. A query is considered RELEVANT if it refers to one or more of the provided **Columns** or if the requested operation aligns with the **Datatype**. Answer with **Yes** or **No**.

         '''),
        ("human", "{input_question}")
    ])
        chain = prompt | llm

        print("Tackle User Input LLM Chain is successfully created!!!")
        return chain
    

    def filterChainAnswer(self, user_query, columns, types, unique_objects):
        try:
            answer = self.filter_chain.invoke({ "input_question": user_query, "df_columns": columns, "types": types, "unique_object": unique_objects })
            return answer.content
        except Exception as e:
            print(f"Error in filter Chain: {e}")
            # Raise an HTTPException with a detailed error message
            raise HTTPException(status_code=500, detail=f"Error in filter Chain: {str(e)}")
            
    
    def tackleUserChainAnswer(self, user_query, columns, types):
        try:
            answer = self.tackle_user_input_chain.invoke({ "input_question": user_query, "df_columns": columns, "types": types})
            return answer.content
        except Exception as e:
            print(f"Error in tackle User Chain: {e}")
            # Raise an HTTPException with a detailed error message
            raise HTTPException(status_code=500, detail=f"Error in tackle User Chain: {str(e)}")
    
    def filterDataFrame(self, dataframe, filter_code):
        df = dataframe
        # Prepare a local variable dictionary to be used by exec
        local_vars = {"df": df}

        # Execute code to filter DataFrame
        try:
           # Execute the code in the local context
            exec(filter_code, globals(), local_vars)
        except Exception as e:
            print(f"Error executing code: {e}")
            return {"error": "Code execution failed"}
        
        df = local_vars["df"]

        print("Filtered DataFrame:", df)

        return df