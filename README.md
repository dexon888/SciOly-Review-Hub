# Science Olympiad Review Hub

## Introduction

The Science Olympiad Review Hub is a web-based application designed to help students prepare for various Science Olympiad events. The application generates quizzes with multiple-choice and short-answer questions for a variety of topics, including Anatomy/Physiology, Fossils, Forestry, Astronomy, and more.

## Features

- **Dynamic Quiz Generation**: Generate multiple-choice and short-answer questions for each topic.
- **Real-Time Grading**: Immediate feedback for multiple-choice questions and similarity-based grading for short-answer questions.
- **Engaging UI**: A vibrant and interactive user interface that includes animations and a Science Olympiad-themed design.

## Screenshots

### Home Page
![Home Page](/screenshots/home_page.png)

### Quiz Generation
![Quiz Generation](/screenshots/quiz_generator.png)

### Quiz Page
![Quiz Page](/screenshots/quiz.png)

## Tech Stack

- **Frontend**: Angular, Angular Material, HTML, CSS
- **Backend**: FastAPI, Python, OpenAI API
- **Deployment**: Vercel

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Angular CLI
- Vercel CLI (for deployment)

### Local Development

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/sci-oly-review-hub.git
   cd sci-oly-review-hub

2. **Frontend Setup:**

    ```bash
    cd frontend
    npm install

    #To run the frontend locally:
    ng serve

3. **Backend Setup:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt

    #To run the backend locally:
    uvicorn main:app --reload

4. **Environment Variables**

    Create a .env file in the backend directory with the following contents:
    ```bash
    OPENAI_API_KEY=your-openai-api-key
    ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200,https://sci-oly-review-hub.vercel.app/

5. **Deployment**
    Deploy the frontend and backend separately to Vercel. Ensure that the backend URL is updated in the frontend service (api.service.ts).


### Usage
Open the application in your browser.
Select a Science Olympiad event from the home page.
Answer the quiz questions and submit your answers.
Receive immediate feedback on your answers.

