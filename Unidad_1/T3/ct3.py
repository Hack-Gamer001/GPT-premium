## instalar librerias

## pip install fastapi uvicorn pyngrok nest_asyncio pydantic llama-cpp-python 
## pip install fastapi uvicorn pyngrok nest_asyncio pydantic requests   
## pip install requests


import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nest_asyncio
from pyngrok import ngrok
import re
import random
from pyngrok import ngrok

# Aplicar nest_asyncio para evitar conflictos con el bucle de eventos de Colab
nest_asyncio.apply()

# Configurar la API
app = FastAPI()

# Configurar la URL del servidor de LM Studio
LM_STUDIO_URL = "http://192.168.56.1:1234/v1/completions"

# Definir el modelo de solicitud simplificado
class ChatRequest(BaseModel):
    pregunta: str

# Ruta para la página de inicio
@app.get("/")
def read_root():
    return {"message": "¡Hola! Esta es la API de tu asistente para niños de 5 a 10 años."}

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

    # Preparar prompt para LM Studio con instrucciones específicas
    prompt_completo = f"""Eres un profesor amable y paciente para niños de 5 a 10 años.
    Explicas conceptos de manera muy simple y divertida.
    Usas ejemplos que los niños pueden entender y relacionar con su vida diaria.
    Evitas palabras complicadas y mantienes un tono positivo.
    Tus respuestas son breves (1-2 oraciones) y directas.
    Si la pregunta es matemática, responde solo con el resultado.
    Si la pregunta es sobre colores, ciencia o naturaleza, da una explicación simple y clara.

    Pregunta: {pregunta_simplificada}
    Respuesta:"""

    # Configurar los parámetros de la solicitud
    payload = {
        "prompt": prompt_completo,
        "max_tokens": 50,  # Limita la longitud de la respuesta
        "temperature": 0.3,  # Reduce la aleatoriedad para respuestas más precisas
        "stop": ["\n", ".", "¡"],  # Detiene la generación en un salto de línea o punto
        "top_p": 0.9,  # Controla la diversidad de la respuesta
        "repetition_penalty": 1.2  # Evita repeticiones
    }

    # Enviar la solicitud al servidor de LM Studio
    response = requests.post(LM_STUDIO_URL, json=payload)

    # Procesar la respuesta
    if response.status_code == 200:
        respuesta_texto = response.json()["choices"][0]["text"].strip()

        # Limpiar la respuesta para que sea más clara y concisa
        respuesta_texto = re.sub(r'\s+', ' ', respuesta_texto)  # Eliminar espacios extra
        respuesta_texto = respuesta_texto.replace("\n", " ")  # Eliminar saltos de línea

        # Si la respuesta es demasiado larga, truncarla
        if len(respuesta_texto.split()) > 15:  # Limitar a 15 palabras
            respuesta_texto = " ".join(respuesta_texto.split()[:15]) + "..."

        return respuesta_texto
    else:
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
ngrok.set_auth_token("2ui17vtgbMrjn2siWw5pXCD4mLX_2wbyY2x8yZyB6dYq3Dk5Z")
ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)

# Configurar y ejecutar el servidor Uvicorn
import uvicorn
if __name__ == "__main__":
    print(f"Iniciando API para niños en http://0.0.0.0:8000")
    print(f"URL pública: {ngrok_tunnel.public_url}")
    uvicorn.run(app, host="0.0.0.0", port=8000)