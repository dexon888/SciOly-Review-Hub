from dotenv import load_dotenv
import os
import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
from difflib import SequenceMatcher

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Define the CORS policy
origins = os.getenv('ALLOWED_ORIGINS',
                    "http://localhost:4200,http://127.0.0.1:4200,https://sci-oly-review-hub.vercel.app/").split(',')

app.add_middleware(
    CORSMiddleware,
    # Allow all origins for testing, replace with specific origins later
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Define the request model


class QuizRequest(BaseModel):
    topic: str
    mcqCount: int
    srqCount: int


class ShortResponseRequest(BaseModel):
    user_response: str
    correct_answer: str


# Define the topics and tailored prompts for Science Olympiad events
topics = {
    "anatomy-physiology": (
        "Generate a challenging, high-school level multiple choice question "
        "on the anatomy and physiology of the cardiovascular, lymphatic, and excretory systems, "
        "including advanced topics such as ECG/EKG interpretation, effects of drugs on cardiac physiology, "
        "and detailed anatomical knowledge. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "fossils": (
        "Generate a difficult multiple choice question about fossils that requires knowledge of fossil identification, "
        "preservation modes, and evolutionary significance, with a focus on the use of fossils in dating "
        "and correlating rock units. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "forestry": (
        "Create a complex multiple choice question about forestry that tests knowledge of tree identification, ecological characteristics, "
        "and forest management practices. The question should also consider economic aspects of trees. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "astronomy": (
        "Generate a rigorous multiple choice question about stellar evolution, exoplanet detection, or orbital mechanics, requiring detailed "
        "knowledge and data interpretation. The question should challenge students with concepts like Hertzsprung-Russell diagrams, "
        "Kepler’s laws, and multi-wavelength astronomy. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "disease-detectives": (
        "Generate a difficult multiple choice question on epidemiology and disease detection, focusing on outbreak investigation, "
        "data interpretation, and the application of epidemiological principles. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "chemistry-lab": (
        "Generate a challenging, high-school level multiple choice question "
        "focused on the scientific processes of chemistry, particularly in the areas of Periodicity and Equilibrium. "
        "Questions may involve tasks like equilibrium reactions, periodic trends, titration calculations, "
        "molecular structure, and related chemical principles. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "dynamic-planet": (
        "Generate a challenging, high-school level multiple choice question "
        "focused on the large-scale processes affecting Earth's crust structure, including plate tectonics, "
        "earthquakes, and volcanoes. Questions should explore topics like the structure of Earth's interior, "
        "magma composition, geologic history, and the impact of plate movements on global and environmental changes. "
        "Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "ecology": (
        "Generate a challenging, high-school level multiple choice question "
        "focused on the principles of ecology, adaptations in biomes, and human impact on ecosystems. "
        "Topics should include food webs, nutrient cycling, population dynamics, biodiversity, "
        "climate change, and conservation biology. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "microbe-mission": (
        "Generate a challenging, high-school level multiple choice question "
        "focused on microbiology topics, including microbial structure and function, "
        "bacterial growth, antibiotic resistance, and the roles of microbes in industry and ecology. "
        "Questions may involve topics such as bacterial cell structures, growth conditions, genetic regulation, "
        "and microbial interactions. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
    "optics": (
        "Generate a challenging, high-school level multiple choice question "
        "focused on the principles of optics, including reflection, refraction, mirrors and lenses, color theory, "
        "and the structure and function of the human eye. Questions should also cover advanced topics such as "
        "Snell's law, critical angle, polarization, and lasers. Format the response as follows:\n\n"
        "Question: <question text>\n"
        "A) <option A>\n"
        "B) <option B>\n"
        "C) <option C>\n"
        "D) <option D>\n"
        "Correct answer: <correct option letter>\n"
        "Explanation: <brief explanation>"
    ),
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
            max_tokens=200  # Increase max tokens to accommodate explanation
        )
        question_content = response['choices'][0]['message']['content'].strip()

        # Extract the correct answer and explanation in the specified format
        correct_answer, explanation = extract_correct_answer_and_explanation(
            question_content)

        # Assuming that options are in the format A), B), C), D)
        options = extract_options(question_content)

        question_body = re.split(r'\n', question_content)[
            0].strip()  # Extract the question part

        quiz.append({
            "type": "multiple_choice",
            "question": question_body,
            "options": options,
            "correctAnswer": correct_answer,
            "explanation": explanation
        })

    # Generate short response questions
    for _ in range(request.srqCount):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a quiz generator."},
                {"role": "user", "content": f"{prompt}\nType: Short Response"},
            ],
            max_tokens=200
        )
        short_response_content = response['choices'][0]['message']['content'].strip(
        )

        # Extract the question and correct answer (assuming it's given in the same response)
        # You may need to modify the prompt to ensure the correct answer is provided in the output
        question = short_response_content.split("Correct answer:")[0].strip()
        correct_answer = short_response_content.split("Correct answer:")[
            1].strip()

        quiz.append({
            "type": "short_response",
            "question": question,
            "correctAnswer": correct_answer
        })

    return {"quiz": quiz}


@app.post("/grade-short-response")
async def grade_short_response(request: ShortResponseRequest):
    try:
        # Use OpenAI to generate a similarity score or use a simple string matching technique
        similarity_score = SequenceMatcher(
            None, request.user_response, request.correct_answer).ratio()

        # Convert the similarity score to a percentage
        similarity_percentage = round(similarity_score * 100, 2)

        # Determine grading based on similarity score
        if similarity_percentage > 80:
            result = "Correct"
        elif similarity_percentage > 50:
            result = "Partial Credit"
        else:
            result = "Incorrect"

        return {
            "user_response": request.user_response,
            "correct_answer": request.correct_answer,
            "similarity_percentage": similarity_percentage,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def extract_options(content: str) -> list:
    # Assuming options are in the format A) ... B) ... C) ... D)
    options = []
    pattern = re.compile(r'[ABCD]\)\s.*')
    for match in pattern.findall(content):
        options.append(match.strip())
    return options


def extract_correct_answer_and_explanation(content: str) -> tuple:
    # Extract correct answer and explanation using specific markers
    correct_answer_match = re.search(r'Correct answer:\s*([ABCD])', content)
    explanation_match = re.search(r'Explanation:\s*(.*)', content)

    correct_answer = correct_answer_match.group(
        1).strip() if correct_answer_match else ""
    explanation = explanation_match.group(
        1).strip() if explanation_match else ""

    return correct_answer, explanation
