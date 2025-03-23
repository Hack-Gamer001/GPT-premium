import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nest_asyncio
from pyngrok import ngrok
import re
import random

# Aplicar nest_asyncio para evitar conflictos con el bucle de eventos
nest_asyncio.apply()

# Configurar la API
app = FastAPI(title="API Educativa para Niños", 
              description="Asistente educativo interactivo para niños de 5 a 10 años")

# Configurar la URL del servidor de LM Studio
LM_STUDIO_URL = "http://192.168.56.1:1234/v1/completions"

# Definir el modelo de solicitud
class ChatRequest(BaseModel):
    pregunta: str

# Ruta para la página de inicio
@app.get("/")
def read_root():
    return {
        "mensaje": "¡Hola! Soy tu profesor virtual para niños de 5 a 10 años.",
        "instrucciones": "Envía tus preguntas al endpoint /chat con formato JSON {'pregunta': 'tu pregunta aquí'}"
    }

# Categorías temáticas para contextualizar respuestas
CATEGORIAS = {
    "ciencia": ["planeta", "estrella", "animal", "planta", "agua", "aire", "espacio", 
                "dinosaurio", "cuerpo", "cerebro", "corazón", "tierra", "sol", "luna"],
    "matemáticas": ["número", "suma", "resta", "contar", "forma", "círculo", "cuadrado", 
                    "triángulo", "mitad", "doble", "más", "menos", "grande", "pequeño"],
    "arte": ["color", "pintura", "música", "canción", "baile", "dibujo", "crear", 
             "libro", "cuento", "historia", "personaje"],
    "social": ["amigo", "familia", "escuela", "ciudad", "país", "ayudar", "compartir", 
               "jugar", "trabajo", "casa", "normas", "reglas"],
    "tecnología": ["computadora", "internet", "robot", "máquina", "inventor", "energía", 
                  "electricidad", "video", "juego"]
}

# Temas inapropiados que se deben redireccionar
TEMAS_BLOQUEADOS = {
    # Temas inapropiados (redirigir a temas adecuados)
    "sexo": "cómo nacen los bebés de forma sencilla",
    "pornografía": "material apropiado para tu edad",
    "drogas": "medicinas y salud",
    "alcohol": "bebidas saludables",
    "suicidio": "sentimientos de tristeza",
    "violencia": "cómo resolver conflictos pacíficamente",
    "armas": "herramientas y su uso responsable",
    # Temas complejos (simplificar)
    "álgebra": "matemáticas con números y letras",
    "cálculo": "matemáticas de los cambios",
    "trigonometría": "matemáticas de los triángulos",
    "criptografía": "mensajes secretos",
    "física cuántica": "cómo se comportan las cosas muy pequeñitas",
    "química orgánica": "cómo están hechas las cosas vivas",
    "relatividad": "cómo funciona el tiempo y el espacio",
    "logaritmo": "matemáticas especiales para números grandes"
}

# Función para detectar la categoría temática de la pregunta
def detectar_categoria(pregunta: str) -> str:
    pregunta_lower = pregunta.lower()
    
    # Detectar palabras clave en la pregunta
    for categoria, palabras_clave in CATEGORIAS.items():
        for palabra in palabras_clave:
            if palabra in pregunta_lower:
                return categoria
    
    # Si no se detecta ninguna categoría específica
    return "general"

# Función para validar y redirigir preguntas
def validar_y_redirigir(pregunta: str) -> tuple:
    pregunta_lower = pregunta.lower()
    
    # Verificar temas bloqueados
    for tema, alternativa in TEMAS_BLOQUEADOS.items():
        if tema in pregunta_lower:
            if tema in ["sexo", "pornografía", "drogas", "alcohol", "suicidio", "violencia", "armas"]:
                pregunta_redirigida = f"Podrías explicarme sobre {alternativa}"
                return False, pregunta_redirigida
            else:
                pregunta_adaptada = f"Podrías explicarme de forma muy sencilla sobre {alternativa}"
                return True, pregunta_adaptada
    
    return True, pregunta

# Función para adaptar el nivel de respuesta según edad estimada por complejidad de la pregunta
def estimar_nivel_comprension(pregunta: str) -> str:
    palabras = pregunta.split()
    longitud = len(palabras)
    palabras_complejas = sum(1 for palabra in palabras if len(palabra) > 7)
    
    # Estimar nivel según complejidad de la pregunta
    if longitud > 12 and palabras_complejas > 3:
        return "avanzado"  # 9-10 años
    elif longitud > 8 and palabras_complejas > 1:
        return "intermedio"  # 7-8 años
    else:
        return "básico"  # 5-6 años

# Función para generar ejemplos contextualizados según la categoría
def generar_ejemplos(categoria: str) -> str:
    ejemplos = {
        "ciencia": [
            "como cuando juegas con agua y ves que algunas cosas flotan y otras se hunden",
            "igual que cuando ves crecer una plantita desde una semillita",
            "como cuando miras el cielo por la noche y ves todas las estrellas brillando"
        ],
        "matemáticas": [
            "como cuando compartes tus dulces con tus amigos y cuentas cuántos le tocan a cada uno",
            "igual que cuando ordenas tus juguetes por tamaño o color",
            "como cuando usas un calendario para contar los días que faltan para tu cumpleaños"
        ],
        "arte": [
            "como cuando mezclas colores para crear uno nuevo y diferente",
            "igual que cuando inventas una historia con tus personajes favoritos",
            "como cuando escuchas una canción y puedes sentir si es alegre o triste"
        ],
        "social": [
            "igual que cuando aprendes a esperar tu turno en un juego",
            "como cuando haces un nuevo amigo y descubres cosas que les gustan a ambos",
            "igual que cuando ayudas en casa y todos se sienten contentos"
        ],
        "tecnología": [
            "como cuando usas una tablet para jugar y aprender cosas nuevas",
            "igual que cuando envías un mensaje a alguien que está lejos",
            "como cuando ves que un robot puede ayudar a las personas"
        ],
        "general": [
            "como cuando descubres algo nuevo por primera vez",
            "igual que cuando resuelves un problema paso a paso",
            "como cuando explicas a un amigo algo que acabas de aprender"
        ]
    }
    
    return random.choice(ejemplos.get(categoria, ejemplos["general"]))

# Función para generar respuesta mejorada para niños
def generar_respuesta_para_niños(pregunta: str) -> str:
    # Validar y posiblemente redirigir la pregunta
    es_valida, pregunta_procesada = validar_y_redirigir(pregunta)
    
    # Si la pregunta no es válida, pero se ha redirigido
    if not es_valida:
        pregunta = pregunta_procesada
    
    # Detectar categoría temática para contextualizar
    categoria = detectar_categoria(pregunta)
    
    # Estimar nivel de comprensión 
    nivel = estimar_nivel_comprension(pregunta)
    
    # Seleccionar ejemplo contextualizado
    ejemplo = generar_ejemplos(categoria)
    
    # Ajustar longitud de respuesta según nivel
    max_tokens = 60 if nivel == "básico" else (80 if nivel == "intermedio" else 100)
    
    # Preparar prompt mejorado para LM Studio con instrucciones específicas según nivel y categoría
    instrucciones_nivel = {
        "básico": "Usa palabras muy simples y oraciones cortas. Compara con cosas cotidianas como juguetes o comida.",
        "intermedio": "Usa palabras sencillas pero puedes introducir 1-2 términos nuevos explicándolos. Puedes usar ejemplos del colegio.",
        "avanzado": "Puedes usar un vocabulario un poco más avanzado, explicando los términos nuevos. Anima a la curiosidad y el pensamiento crítico."
    }
    
    instrucciones_categoria = {
        "ciencia": "Usa metáforas visuales y menciona cómo se puede observar este fenómeno en la vida diaria.",
        "matemáticas": "Usa ejemplos concretos con números pequeños y situaciones de juego o reparto.",
        "arte": "Conecta con emociones y estimula la imaginación creativa.",
        "social": "Enfatiza valores como compartir, respetar y ayudar a los demás.",
        "tecnología": "Explica cómo la tecnología ayuda a las personas y facilita tareas.",
        "general": "Da ejemplos concretos y relaciona con experiencias cotidianas."
    }
    
    prompt_completo = f"""Eres un profesor especializado en educación infantil para niños de 5 a 10 años.
    
    CONTEXTO:
    - Categoría temática: {categoria}
    - Nivel de comprensión estimado: {nivel}
    
    INSTRUCCIONES ESPECÍFICAS:
    - {instrucciones_nivel[nivel]}
    - {instrucciones_categoria.get(categoria, instrucciones_categoria["general"])}
    - Incluye una pequeña analogía o comparación, {ejemplo}.
    - Transmite entusiasmo por aprender e inspira curiosidad.
    - Si es apropiado, termina con una pequeña pregunta que invite a reflexionar.
    - Respuesta corta (2-3 oraciones para nivel básico, 3-4 para intermedio, 4-5 para avanzado).
    
    Pregunta del niño: {pregunta_procesada}
    Respuesta:"""

    # Configurar los parámetros de la solicitud para LM Studio
    payload = {
        "prompt": prompt_completo,
        "max_tokens": max_tokens,
        "temperature": 0.4,  # Balance entre creatividad y precisión
        "top_p": 0.92,
        "top_k": 40,
        "presence_penalty": 0.1,  # Evita repeticiones
        "frequency_penalty": 0.2,  # Favorece variedad de vocabulario
        "stop": ["Pregunta:", "\n\n"]  # Detiene la generación en ciertas marcas
    }

    # Enviar la solicitud al servidor de LM Studio
    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        # Procesar la respuesta
        respuesta_texto = response.json()["choices"][0]["text"].strip()
        
        # Pulir la respuesta
        respuesta_texto = re.sub(r'\s+', ' ', respuesta_texto)  # Eliminar espacios extra
        respuesta_texto = respuesta_texto.replace(" .", ".").replace(" ,", ",")  # Corregir puntuación
        
        # Añadir emoji según categoría para hacerlo más atractivo
        emojis = {
            "ciencia": "🔍 ",
            "matemáticas": "🔢 ",
            "arte": "🎨 ",
            "social": "👫 ",
            "tecnología": "🤖 ",
            "general": "✨ "
        }
        respuesta_final = emojis.get(categoria, "🌟 ") + respuesta_texto
        
        return respuesta_final
        
    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f"Error al generar respuesta: {str(e)}")
        return "¡Vaya! Mi cerebro está pensando muy fuerte pero no encuentra la respuesta. ¿Podrías preguntarme de otra manera? 🤔"

# Ruta para manejar las solicitudes POST
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        pregunta = request.pregunta.strip()
        
        # Verificar que la pregunta no esté vacía
        if not pregunta:
            return {"respuesta": "¡Hola! No he escuchado tu pregunta. ¿Qué te gustaría saber? 😊"}
            
        # Generar una respuesta adaptada al nivel de comprensión y categoría temática
        respuesta_texto = generar_respuesta_para_niños(pregunta)
        
        # Devolver la respuesta generada
        return {"respuesta": respuesta_texto}

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return {"respuesta": "¡Ups! Algo se enredó en mi cerebro. ¿Podrías intentar con otra pregunta? 🙃"}

# Configurar Ngrok con el authtoken
ngrok.set_auth_token("2uQhy48NKgv5Mok0jXHGzgwCrD9_DB9ZQzzc8EQsjVRMijR6")
ngrok_tunnel = ngrok.connect(8000)
print('URL Pública:', ngrok_tunnel.public_url)

# Configurar y ejecutar el servidor Uvicorn
import uvicorn
if __name__ == "__main__":
    print(f"Iniciando API educativa para niños en http://0.0.0.0:8000")
    print(f"URL pública: {ngrok_tunnel.public_url}")
    print(f"¡Listo para responder preguntas de pequeños curiosos!")
    uvicorn.run(app, host="0.0.0.0", port=8000)