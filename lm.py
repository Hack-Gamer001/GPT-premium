import requests

# Configura la URL del servidor de LM Studio
url = "http://192.168.56.1:1234/v1/completions"

# Configura los parámetros de la solicitud
payload = {
    "prompt": "¿Por qué el cielo es azul?",  # Tu pregunta o prompt
    "max_tokens": 100,  # Número máximo de tokens en la respuesta
    "temperature": 0.7,  # Controla la creatividad de la respuesta
    "stop": ["\n"]  # Detiene la generación en un salto de línea
}

# Envía la solicitud al servidor
response = requests.post(url, json=payload)

# Procesa la respuesta
if response.status_code == 200:
    respuesta = response.json()["choices"][0]["text"]
    print("Respuesta:", respuesta)
else:
    print("Error:", response.status_code, response.text)