from fastapi import FastAPI
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")

# Create FastAPI app
app = FastAPI(title="AI SQL Query Generator")

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

@app.get("/")
def home():
    return {"message": "AI SQL Query Generator API is running!"}

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

    try:
        response = model.generate_content(prompt)

        return {
            "question": req.question,
            "sql": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }
