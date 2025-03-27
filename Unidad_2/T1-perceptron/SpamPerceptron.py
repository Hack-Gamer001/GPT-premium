import numpy as np
import matplotlib.pyplot as plt
import random

class SpamPerceptron:
    def __init__(self, num_entradas):
        # Inicializar pesos con valores aleatorios
        self.pesos = np.array([random.uniform(-0.1, 0.1) for _ in range(num_entradas)])
        self.bias = random.uniform(-0.1, 0.1)

        # Diccionario de palabras clave de spam
        self.palabras_spam = {
            # Palabras generales de spam
            'gana': 0.7,
            'gratis': 0.8,
            'ganaste': 0.9,
            'premio': 0.7,
            'sorteo': 0.7,
            'herencia': 0.8,
            'millones': 0.8,
            'oportunidad': 0.7,
            'urgente': 0.6,
            'increíble': 0.6,

            # Palabras específicas de ofertas y engaños
            'iphone': 0.9,
            'clic': 0.6,
            'oferta': 0.6,
            'dinero': 0.7,
            'rápido': 0.6,
            'préstamo': 0.7,
            'exclusiva': 0.6,
            'descuento': 0.7
        }

    # Funciones de activación
    def escalon(self, x):
        return 1.0 if x >= 0.5 else 0.0

    def sigmoide(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def relu(self, x):
        return np.maximum(0.0, x)

    def tanh(self, x):
        return np.tanh(x)

    def softmax(self, x):
        return np.exp(x) / (1.0 + np.exp(x))

    def lineal(self, x):
        return x

    def predecir(self, entrada):
        return np.dot(self.pesos, entrada) + self.bias

    def calcular_puntaje_mensaje(self, mensaje):
        mensaje = mensaje.lower()
        puntaje_total = 0.0
        contador_palabras_spam = 0

        for palabra, valor in self.palabras_spam.items():
            if palabra in mensaje:
                puntaje_total += valor
                contador_palabras_spam += 1

        # Bonus por múltiples palabras de spam
        if contador_palabras_spam > 1:
            puntaje_total *= (1 + (contador_palabras_spam * 0.2))

        return min(puntaje_total, 1.0)

    def es_spam(self, puntaje):
        return (puntaje >= 0.6 or 
                self.sigmoide(puntaje) >= 0.7 or 
                self.escalon(puntaje) == 1.0)

    def analizar_mensaje(self, mensaje):
        puntaje = self.calcular_puntaje_mensaje(mensaje)
        entrada = [puntaje]
        suma = self.predecir(entrada)

        return {
            'mensaje': mensaje,
            'puntaje_spam': puntaje,
            'suma_perceptron': suma,
            'funciones_activacion': {
                'escalon': self.escalon(suma),
                'sigmoide': self.sigmoide(suma),
                'relu': self.relu(suma),
                'tanh': self.tanh(suma),
                'softmax': self.softmax(suma),
                'lineal': self.lineal(suma)
            },
            'es_spam': self.es_spam(puntaje)
        }

    def graficar_funciones_activacion(self):
        # Crear un rango de valores para graficar
        x = np.linspace(-5, 5, 100)

        # Crear la figura con subplots
        plt.figure(figsize=(15, 10))
        
        # Funciones a graficar
        funciones = [
            ('Escalón', self.escalon),
            ('Sigmoide', self.sigmoide),
            ('ReLU', self.relu),
            ('Tangente Hiperbólica', self.tanh),
            ('Softmax', self.softmax),
            ('Lineal', self.lineal)
        ]

        # Graficar cada función
        for i, (nombre, funcion) in enumerate(funciones, 1):
            plt.subplot(2, 3, i)
            y = [funcion(val) for val in x]
            plt.plot(x, y)
            plt.title(f'Función de Activación: {nombre}')
            plt.xlabel('Entrada (x)')
            plt.ylabel('Salida')
            plt.grid(True)

        plt.tight_layout()
        plt.show()

def main():
    # Crear el perceptrón
    perceptron = SpamPerceptron(1)

    # Ejemplos de mensajes
    ejemplos_mensajes = [
        "Ganaste un iPhone gratis",
        "Reunión de equipo mañana",
        "Oferta exclusiva por tiempo limitado",
        "Hola, ¿cómo estás?",
        "Últimas horas para reclamar tu premio"
    ]

    # Analizar cada mensaje
    for mensaje in ejemplos_mensajes:
        resultado = perceptron.analizar_mensaje(mensaje)
        print("\n📊 Análisis del Mensaje:")
        print(f"Mensaje: {resultado['mensaje']}")
        print(f"Puntaje de Spam: {resultado['puntaje_spam']:.2f}")
        print(f"Es Spam: {resultado['es_spam']}")
        print("\n🧠 Resultados de Funciones de Activación:")
        for nombre, valor in resultado['funciones_activacion'].items():
            print(f"{nombre}: {valor:.2f}")

    # Graficar funciones de activación
    perceptron.graficar_funciones_activacion()

if __name__ == "__main__":
    main()