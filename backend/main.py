from fastapi import FastAPI
import openai

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Science Olympiad Quiz API"}

@app.post("/generate-question")
async def generate_question(topic: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Generate a multiple choice question about {topic}",
        max_tokens=100
    )
    return {"question": response.choices[0].text}
