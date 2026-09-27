import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, age: int = Form(...), weight: int = Form(...), height: int = Form(...), goal: str = Form(...), diet: str = Form(...)):
    prompt = f"Create a 7-day fitness and diet plan for a {age} year old person, {weight}kg, {height}cm. Goal: {goal}, Diet: {diet}. Give workout and food in table format."
    response = model.generate_content(prompt)
    return templates.TemplateResponse("result.html", {"request": request, "plan": response.text, "goal": goal})
