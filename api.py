import os

from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

app = FastAPI()

class Review(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    label: str
    score: int
    theme: str

@app.post("/analyze")
def analyze(review: Review):
    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents= ("Analyze the cutomer review and provide a sentiment label (positive, negative, neutral), a score from 1 to 10, and a theme that summarizes the main topic of the review. The output should be in JSON format with keys 'label', 'score', and 'theme'. Here is the review: " + review.text),
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AnalysisResult,
        )
    )
    return response.parsed