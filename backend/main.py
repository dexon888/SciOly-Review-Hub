from fastapi import FastAPI, HTTPException
import openai

app = FastAPI()

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
async def generate_quiz(topic: str, mcqCount: int, srqCount: int):
    if topic not in topics:
        raise HTTPException(status_code=400, detail="Invalid topic")

    quiz = []
    prompt = topics[topic]

    for _ in range(mcqCount):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{prompt}\nType: Multiple Choice",
            max_tokens=100
        )
        quiz.append(response.choices[0].text)

    for _ in range(srqCount):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{prompt}\nType: Short Response",
            max_tokens=100
        )
        quiz.append(response.choices[0].text)

    return {"quiz": quiz}
