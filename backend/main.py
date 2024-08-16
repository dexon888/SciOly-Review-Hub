from dotenv import load_dotenv
import os
import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Define the CORS policy
origins = [
    "http://localhost:4200",  # Angular development server
    "http://127.0.0.1:4200"   # Alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define the request model


class QuizRequest(BaseModel):
    topic: str
    mcqCount: int
    srqCount: int


# Define the topics and prompts
topics = {
    "anatomy-physiology": "Generate a multiple choice question about human anatomy and physiology.",
    "fossils": "Generate a multiple choice question about fossils.",
    "forestry": "Generate a multiple choice question about forestry.",
    "astronomy": "Generate a multiple choice question about astronomy.",
    "disease-detectives": "Generate a multiple choice question about epidemiology and disease detection."
}


@app.get("/")
def read_root():
    return {"message": "Welcome to the Science Olympiad Quiz API"}


@app.post("/generate-quiz")
async def generate_quiz(request: QuizRequest):
    if request.topic not in topics:
        raise HTTPException(status_code=400, detail="Invalid topic")

    quiz = []
    prompt = topics[request.topic]

    # Generate multiple choice questions
    for _ in range(request.mcqCount):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a quiz generator."},
                {"role": "user", "content": f"{prompt}\nType: Multiple Choice"},
            ],
            max_tokens=100
        )
        quiz.append(response['choices'][0]['message']['content'].strip())

    # Generate short response questions
    for _ in range(request.srqCount):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a quiz generator."},
                {"role": "user", "content": f"{prompt}\nType: Short Response"},
            ],
            max_tokens=100
        )
        quiz.append(response['choices'][0]['message']['content'].strip())

    return {"quiz": quiz}
