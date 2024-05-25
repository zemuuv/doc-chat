from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configuración de la aplicación FastAPI
app = FastAPI()

# Configuración de CORS para permitir solicitudes desde el frontend
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5500",  # Agrega este si estás usando Live Server en VS Code
    "http://127.0.0.1:5500",  # Agrega este si estás usando Live Server en VS Code
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definición del modelo de datos para la pregunta
class Question(BaseModel):
    question: str

# Configuración del logger
logging.basicConfig(level=logging.INFO)

# Ruta para manejar solicitudes POST en /chat
@app.post("/chat")
async def chat(question: Question):
    try:
        # Prompt modificado para incluir la restricción de responder solo preguntas médicas en español
        modified_prompt = f"Por favor, responde solo preguntas relacionadas con medicina en español. Pregunta: {question.question}"

        # Realiza una solicitud a la API de Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"prompt": modified_prompt, "model": "llama2", "stream": False}
        )
        response.raise_for_status()
        data = response.json()
        
        # Obtiene la respuesta de la API de Ollama
        answer = data.get("response")
        if not answer:
            raise HTTPException(status_code=500, detail="No se pudo obtener una respuesta")
        
        return {"response": answer}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta raíz para comprobar el funcionamiento de la API
@app.get("/")
async def root():
    return {"message": "API de chat está funcionando"}
