from fastapi import FastAPI
from google import genai
from pydantic import BaseModel, Field

app = FastAPI(title="AI SQL Query Generator")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

schema = """
Database: college

Table: students

Columns:
id INT
name VARCHAR
branch VARCHAR
marks INT
city VARCHAR
"""

class QueryRequest(BaseModel):
    question: str = Field(min_length=5, max_length=100)


@app.post("/generate-sql")
def generate_sql(req: QueryRequest):

    prompt = f"""
You are an SQL expert.

Database Schema:
{schema}

Convert the following English description into a valid MySQL query.

Question:
{req.question}

Return ONLY the SQL query.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "question": req.question,
        "sql": response.text
    }
