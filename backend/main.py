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


# Define the topics and tailored prompts for Science Olympiad events
topics = {
    "anatomy-physiology": (
        "Generate a challenging, high-school level multiple choice or short response question "
        "on the anatomy and physiology of the cardiovascular, lymphatic, and excretory systems, "
        "including advanced topics such as ECG/EKG interpretation, effects of drugs on cardiac physiology, "
        "and detailed anatomical knowledge. This question should be suitable for a Science Olympiad competition."
    ),
    "fossils": (
        "Generate a difficult question about fossils that requires knowledge of fossil identification, "
        "preservation modes, and evolutionary significance, with a focus on the use of fossils in dating "
        "and correlating rock units. The question should challenge high-school level students in a Science Olympiad competition."
    ),
    "forestry": (
        "Create a complex question about forestry that tests knowledge of tree identification, ecological characteristics, "
        "and forest management practices. The question should also consider economic aspects of trees and be suitable "
        "for advanced high school students participating in a Science Olympiad competition."
    ),
    "astronomy": (
        "Generate a rigorous question about stellar evolution, exoplanet detection, or orbital mechanics, requiring detailed "
        "knowledge and data interpretation. The question should challenge students with concepts like Hertzsprung-Russell diagrams, "
        "Kepler’s laws, and multi-wavelength astronomy, appropriate for a Science Olympiad competition."
    ),
    "disease-detectives": (
        "Generate a difficult question on epidemiology and disease detection, focusing on outbreak investigation, "
        "data interpretation, and the application of epidemiological principles. The question should be at a level "
        "appropriate for high school students in a Science Olympiad competition."
    )
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
                {"role": "system",
                    "content": "You are a quiz generator for Science Olympiad."},
                {"role": "user", "content": f"{prompt}\nType: Multiple Choice"},
            ],
            max_tokens=150  # Increased tokens for more detailed questions
        )
        quiz.append({
            "type": "multiple_choice",
            "question": response['choices'][0]['message']['content'].strip()
        })

    # Generate short response questions
    for _ in range(request.srqCount):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                    "content": "You are a quiz generator for Science Olympiad."},
                {"role": "user", "content": f"{prompt}\nType: Short Response"},
            ],
            max_tokens=150  # Increased tokens for more detailed questions
        )
        quiz.append({
            "type": "short_response",
            "question": response['choices'][0]['message']['content'].strip()
        })

    return {"quiz": quiz}
