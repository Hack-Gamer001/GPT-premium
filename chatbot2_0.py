# Instalar dependencias necesarias
# !pip install fastapi uvicorn pyngrok nest_asyncio pydantic llama-cpp-python

# Descargar el modelo si no existe
# !mkdir -p models
# !wget -O models/llama-3.2-3b-instruct-q8_0.gguf https://huggingface.co/hugging-quants/Llama-3.2-3B-Instruct-Q8_0-GGUF/resolve/main/llama-3.2-3b-instruct-q8_0.gguf

# Importar librerías
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
import nest_asyncio
from pyngrok import ngrok
from llama_cpp import Llama
import re
import json
import time
import logging
import random
from fastapi.middleware.cors import CORSMiddleware

# Resto del código...

# Importar librerías
from fastapi import FastAPI
from pydantic import BaseModel
import nest_asyncio
from pyngrok import ngrok
from llama_cpp import Llama
import re
import random

# Aplicar nest_asyncio para evitar conflictos con el bucle de eventos de Colab
nest_asyncio.apply()

# Configurar la API
app = FastAPI()

# Cargar el modelo de lenguaje (Llama)
llm = Llama(
    model_path="models/llama-3.2-3b-instruct-q8_0.gguf",
    n_ctx=2048,
    n_batch=512  # Optimización para rendimiento
)

# Definir el modelo de solicitud simplificado
class ChatRequest(BaseModel):
    pregunta: str

# Ruta para la página de inicio
@app.get("/")
def read_root():
    return {"message": "¡Hola! Esta es la API de Llama 3.2, tu asistente para niños de 5 a 10 años."}

# Palabras bloqueadas con diferentes niveles de complejidad
PALABRAS_BLOQUEADAS = [
    # Matemáticas y ciencias avanzadas
    "álgebra", "cálculo", "trigonometría", "criptografía", "física cuántica",
    "química orgánica", "bioquímica", "genética", "relatividad", "logaritmo",
    # Temas inapropiados
    "sexo", "pornografía", "drogas", "suicidio", "violencia", "armas"
]

# Palabras simples que podrían formar parte de explicaciones adecuadas
PALABRAS_PERMITIDAS = [
    "física básica", "química simple", "biología básica"
]

# Función para validar la pregunta
def validar_pregunta(pregunta: str) -> bool:
    pregunta_lower = pregunta.lower()

    # Verificar palabras bloqueadas
    for palabra in PALABRAS_BLOQUEADAS:
        if palabra in pregunta_lower:
            # Verificar si es parte de una palabra permitida
            es_permitida = False
            for palabra_permitida in PALABRAS_PERMITIDAS:
                if palabra in palabra_permitida and palabra_permitida in pregunta_lower:
                    es_permitida = True
                    break

            if not es_permitida:
                return False

    return True

# Función para generar respuesta para niños
def generar_respuesta_para_niños(pregunta: str) -> str:
    # Asegurarse de que la pregunta sea adecuada para niños
    if not validar_pregunta(pregunta):
        return "Esa pregunta es demasiado avanzada. Pregunta algo más sencillo y te guiaré con gusto."

    # Simplificar términos complejos
    reemplazos = {
        "gravitación": "por qué las cosas caen",
        "fotosíntesis": "cómo las plantas comen luz",
        "molecular": "sobre las partes muy pequeñas",
        "atmósfera": "aire alrededor de la Tierra",
        "ecosistema": "lugar donde viven animales y plantas juntos"
    }

    pregunta_simplificada = pregunta
    for complejo, simple in reemplazos.items():
        pregunta_simplificada = re.sub(r'\b' + complejo + r'\b', simple, pregunta_simplificada, flags=re.IGNORECASE)

    # Preparar prompt para Llama con instrucciones específicas
    prompt_completo = f"""<sys>Eres un profesor amable y paciente para niños de 5 a 10 años.
    Explicas conceptos de manera muy simple y divertida.
    Usas ejemplos que los niños pueden entender y relacionar con su vida diaria.
    Evitas palabras complicadas y mantienes un tono positivo.
    Tus respuestas son breves (3-4 oraciones) pero completas.
    Incluyes pequeños ejemplos o analogías divertidas.</sys>

    <user>Responde como si fueras un profesor para niños de 5 a 10 años: {pregunta_simplificada}</user>

    <assistant>"""

    # Generar respuesta usando Llama
    try:
        respuesta = llm(
            prompt_completo,
            max_tokens=256,
            stop=["</assistant>", "<user>"],
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            repeat_penalty=1.1
        )

        # Extraer la respuesta generada
        respuesta_texto = respuesta["choices"][0]["text"].strip()

        # Limpiar la respuesta para que sea más clara y concisa
        respuesta_texto = re.sub(r'\s+', ' ', respuesta_texto)  # Eliminar espacios extra
        respuesta_texto = respuesta_texto.replace("\n", " ")  # Eliminar saltos de línea

        # Añadir un toque didáctico aleatorio
        frases_didacticas = [
            " ¡Esto es muy interesante!",
            " ¡Qué divertido es aprender!",
            " ¿No te parece fascinante?",
            " ¡La ciencia es como magia que puedes entender!",
            " ¡Ahora ya sabes algo nuevo!"
        ]

        if random.random() > 0.7:  # 30% de probabilidad
            respuesta_texto += random.choice(frases_didacticas)

        return respuesta_texto

    except Exception:
        return "Lo siento, no pude pensar en una buena respuesta. ¿Podrías preguntarme de otra manera?"

# Ruta para manejar las solicitudes POST
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        pregunta = request.pregunta

        # Verificar si la pregunta es válida
        if not validar_pregunta(pregunta):
            return {"respuesta": "Esa pregunta es demasiado avanzada. Pregunta algo más sencillo y te guiaré con gusto."}

        # Generar una respuesta adecuada para niños
        respuesta_texto = generar_respuesta_para_niños(pregunta)

        # Devolver la respuesta generada
        return {"respuesta": f"La respuesta es: {respuesta_texto}"}

    except Exception:
        return {"respuesta": "Lo siento, hubo un problema. ¿Podrías intentar con otra pregunta?"}

# Configurar Ngrok con el authtoken
ngrok.set_auth_token("2uQhy48NKgv5Mok0jXHGzgwCrD9_DB9ZQzzc8EQsjVRMijR6")
ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)

# Configurar y ejecutar el servidor Uvicorn
import uvicorn
if __name__ == "__main__":
    print(f"Iniciando API Llama 3.2 para niños en http://0.0.0.0:8000")
    print(f"URL pública: {ngrok_tunnel.public_url}")
    uvicorn.run(app, host="0.0.0.0", port=8000)

