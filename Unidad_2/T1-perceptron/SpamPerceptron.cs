using System;
using System.Collections.Generic;

class SpamPerceptron
{
    private double[] pesos;
    private double bias;
    private Dictionary<string, double> palabrasSpam;

    public SpamPerceptron(int numEntradas)
    {
        // Inicializar pesos con valores aleatorios
        Random random = new Random();
        pesos = new double[numEntradas];
        for (int i = 0; i < pesos.Length; i++)
        {
            pesos[i] = random.NextDouble() * 0.2 - 0.1;
        }
        bias = random.NextDouble() * 0.2 - 0.1;

        // Diccionario de palabras clave de spam más completo
        palabrasSpam = new Dictionary<string, double>
        {
            // Palabras generales de spam
            {"gana", 0.7},
            {"gratis", 0.8},
            {"ganaste", 0.9},
            {"premio", 0.7},
            {"sorteo", 0.7},
            {"herencia", 0.8},
            {"millones", 0.8},
            {"oportunidad", 0.7},
            {"urgente", 0.6},
            {"increíble", 0.6},

            // Palabras específicas de ofertas y engaños
            {"iphone", 0.9},
            {"clic", 0.6},
            {"oferta", 0.6},
            {"dinero", 0.7},
            {"rápido", 0.6},
            {"préstamo", 0.7},
            {"exclusiva", 0.6},
            {"descuento", 0.7}
        };
    }

    // Funciones de activación
    public double Escalon(double x)
    {
        return (x >= 0.5) ? 1.0 : 0.0;
    }

    public double Sigmoide(double x)
    {
        return 1.0 / (1.0 + Math.Exp(-x));
    }

    public double ReLU(double x)
    {
        return Math.Max(0.0, x);
    }

    public double Tanh(double x)
    {
        return Math.Tanh(x);
    }

    public double Softmax(double x)
    {
        return Math.Exp(x) / (1.0 + Math.Exp(x));
    }

    public double Lineal(double x)
    {
        return x;
    }

    public double Predecir(double[] entrada)
    {
        double suma = bias;
        for (int i = 0; i < pesos.Length; i++)
        {
            suma += pesos[i] * entrada[i];
        }
        return suma;
    }

    public double CalcularPuntajeMensaje(string mensaje)
    {
        double puntajeTotal = 0.0;
        mensaje = mensaje.ToLower();

        // Contar ocurrencias de palabras clave
        int contadorPalabrasSpam = 0;
        foreach (var palabra in palabrasSpam.Keys)
        {
            if (mensaje.Contains(palabra))
            {
                puntajeTotal += palabrasSpam[palabra];
                contadorPalabrasSpam++;
            }
        }

        // Bonus por múltiples palabras de spam
        if (contadorPalabrasSpam > 1)
        {
            puntajeTotal *= (1 + (contadorPalabrasSpam * 0.2));
        }

        // Normalizar puntaje
        return Math.Min(puntajeTotal, 1.0);
    }

    public bool EsSpam(double puntaje)
    {
        // Criterios más estrictos para spam
        return puntaje >= 0.6 || 
               (this.Sigmoide(puntaje) >= 0.7) || 
               (this.Escalon(puntaje) == 1.0);
    }

    static void Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        SpamPerceptron perceptron = new SpamPerceptron(1);

        while (true)
        {
            Console.Write("\n🔍 Ingrese un mensaje (o 'salir' para terminar): ");
            string mensaje = Console.ReadLine();

            if (mensaje.ToLower() == "salir")
            {
                break;
            }

            double puntaje = perceptron.CalcularPuntajeMensaje(mensaje);
            double[] entrada = { puntaje };
            double suma = perceptron.Predecir(entrada);

            // Imprimir resultados con emojis
            Console.WriteLine("\n📊 Análisis del Mensaje:");
            Console.WriteLine($"🔢 Puntaje de Spam:       {puntaje:F2}");
            Console.WriteLine($"📈 Suma Perceptrón:       {suma:F2}");
            Console.WriteLine("\n🧠 Resultados de Funciones de Activación:");
            Console.WriteLine($"🚦 Escalón:               {perceptron.Escalon(suma):F2}");
            Console.WriteLine($"📊 Sigmoide:             {perceptron.Sigmoide(suma):F2}");
            Console.WriteLine($"🔥 ReLU:                 {perceptron.ReLU(suma):F2}");
            Console.WriteLine($"📐 Tangente Hiperbólica: {perceptron.Tanh(suma):F2}");
            Console.WriteLine($"🔄 Softmax:              {perceptron.Softmax(suma):F2}");
            Console.WriteLine($"➡️ Lineal:               {perceptron.Lineal(suma):F2}");

            // Clasificación de spam con emojis y criterios más precisos
            if (perceptron.EsSpam(puntaje))
            {
                Console.WriteLine("\n⚠️ ¡Alerta! El mensaje es considerado SPAM 🚫");
            }
            else
            {
                Console.WriteLine("\n✅ El mensaje NO es spam 👍");
            }
        }

        Console.WriteLine("\n👋 ¡Hasta luego!");
    }
}