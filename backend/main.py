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


@app.post("/generate-question")
async def generate_question(topic: str):
    if topic not in topics:
        raise HTTPException(status_code=400, detail="Invalid topic")
    prompt = topics[topic]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return {"question": response.choices[0].text}
