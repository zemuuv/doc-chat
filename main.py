from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import logging

app = FastAPI()

# Configurar logging para depuración
logging.basicConfig(level=logging.INFO)

class Question(BaseModel):
    question: str

@app.post("/chat")
async def chat(question: Question):
    try:
        # Definir el prompt para que solo responda preguntas médicas y desactivar el stream
        payload = {
            "prompt": f"Pregunta médica: {question.question}. Responde solo preguntas relacionadas con la medicina.",
            "model": "llama2",  # Nombre del modelo que estás utilizando
            "stream": False  # Asegurarse de que el stream esté desactivado
        }

        # Enviar una solicitud POST a la API de Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",  # Reemplaza con la URL real de tu API de Ollama
            json=payload  # El cuerpo de la solicitud contiene el prompt, el modelo y la configuración de stream
        )

        response.raise_for_status()  # Verifica si la solicitud tuvo éxito, si no, lanza una excepción
        data = response.json()  # Analiza la respuesta JSON de la API de Ollama

        # Extraer el campo "response" de la respuesta de Ollama API
        ollama_response = data.get("response")
        if not ollama_response:
            # Si no se obtiene una respuesta, lanza una excepción HTTP con código 500
            raise HTTPException(status_code=500, detail="No se pudo obtener una respuesta de Ollama API")

        # Retorna solo el campo "response" de la respuesta obtenida de la API de Ollama
        return {"response": ollama_response}
    except requests.RequestException as e:
        # Si hay un error en la solicitud, lanza una excepción HTTP con el mensaje de error
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """
    Este endpoint simplemente confirma que la API está funcionando.

    Retorna:
    - Un mensaje indicando que la API de chat está funcionando.
    """
    return {"message": "API de chat está funcionando"}
