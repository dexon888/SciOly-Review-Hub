from dotenv import load_dotenv
import os
import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

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
        " The correct answer should be included at the end of the response in the format 'Correct Answer: [A/B/C/D]'."
    ),
    "fossils": (
        "Generate a difficult question about fossils that requires knowledge of fossil identification, "
        "preservation modes, and evolutionary significance, with a focus on the use of fossils in dating "
        "and correlating rock units. The question should challenge high-school level students in a Science Olympiad competition."
        " The correct answer should be included at the end of the response in the format 'Correct Answer: [A/B/C/D]'."
    ),
    "forestry": (
        "Create a complex question about forestry that tests knowledge of tree identification, ecological characteristics, "
        "and forest management practices. The question should also consider economic aspects of trees and be suitable "
        "for advanced high school students participating in a Science Olympiad competition."
        " The correct answer should be included at the end of the response in the format 'Correct Answer: [A/B/C/D]'."
    ),
    "astronomy": (
        "Generate a rigorous question about stellar evolution, exoplanet detection, or orbital mechanics, requiring detailed "
        "knowledge and data interpretation. The question should challenge students with concepts like Hertzsprung-Russell diagrams, "
        "Kepler’s laws, and multi-wavelength astronomy, appropriate for a Science Olympiad competition."
        " The correct answer should be included at the end of the response in the format 'Correct Answer: [A/B/C/D]'."
    ),
    "disease-detectives": (
        "Generate a difficult question on epidemiology and disease detection, focusing on outbreak investigation, "
        "data interpretation, and the application of epidemiological principles. The question should be at a level "
        "appropriate for high school students in a Science Olympiad competition."
        " The correct answer should be included at the end of the response in the format 'Correct Answer: [A/B/C/D]'."
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
                {"role": "system", "content": "You are a quiz generator."},
                {"role": "user", "content": f"{prompt}\nType: Multiple Choice"},
            ],
            max_tokens=150
        )
        question_content = response['choices'][0]['message']['content'].strip()

        # Remove any part of the text that could contain an answer or explanation
        possible_clues = ["Correct Answer:", "Answer:", "Explanation:", "Correct:",
                          "Explanation", "answer is", "Correct choice", "Answer is", "The correct"]
        for clue in possible_clues:
            question_content = re.split(clue, question_content)[0]

        # Assuming that options are in the format A), B), C), D)
        options = extract_options(question_content)

        # Extract the correct answer (assuming GPT-3 usually places it at the end)
        correct_answer = extract_correct_answer(
            response['choices'][0]['message']['content'])

        question_body = re.split(r'\n', question_content)[
            0].strip()  # Extract the question part

        quiz.append({
            "type": "multiple_choice",
            "question": question_body,
            "options": options,
            "correctAnswer": correct_answer
        })

    # Generate short response questions
    for _ in range(request.srqCount):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a quiz generator."},
                {"role": "user", "content": f"{prompt}\nType: Short Response"},
            ],
            max_tokens=150
        )
        quiz.append({
            "type": "short_response",
            "question": response['choices'][0]['message']['content'].strip()
        })

    return {"quiz": quiz}


def extract_options(content: str) -> list:
    # Assuming options are in the format A) ... B) ... C) ... D)
    options = []
    pattern = re.compile(r'[ABCD]\)\s.*')
    for match in pattern.findall(content):
        options.append(match.strip())
    return options


def extract_correct_answer(content: str) -> str:
    # Use a pattern to find the correct answer assuming the format is "Correct Answer: X"
    match = re.search(r'Correct Answer:\s*([ABCD])', content)
    if match:
        return match.group(1)
    return ""
