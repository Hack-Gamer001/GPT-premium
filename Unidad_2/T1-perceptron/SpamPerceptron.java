import java.io.UnsupportedEncodingException;
import java.util.*;

public class SpamPerceptron {
    private double[] pesos;
    private double bias;
    private Map<String, Double> palabrasSpam;

    public SpamPerceptron(int numEntradas) {
        // Inicializar pesos con valores más aleatorios
        pesos = new double[numEntradas];
        Random random = new Random();
        for (int i = 0; i < pesos.length; i++) {
            pesos[i] = random.nextDouble() * 0.2 - 0.1;
        }
        bias = random.nextDouble() * 0.2 - 0.1;

        // Diccionario de palabras clave de spam más completo
        palabrasSpam = new HashMap<>();
        
        // Palabras generales de spam
        palabrasSpam.put("gana", 0.7);
        palabrasSpam.put("gratis", 0.8);
        palabrasSpam.put("ganaste", 0.9);
        palabrasSpam.put("premio", 0.7);
        palabrasSpam.put("sorteo", 0.7);
        palabrasSpam.put("herencia", 0.8);
        palabrasSpam.put("millones", 0.8);
        palabrasSpam.put("oportunidad", 0.7);
        palabrasSpam.put("urgente", 0.6);
        palabrasSpam.put("increíble", 0.6);

        // Palabras específicas de ofertas y engaños
        palabrasSpam.put("iphone", 0.9);
        palabrasSpam.put("clic", 0.6);
        palabrasSpam.put("oferta", 0.6);
        palabrasSpam.put("dinero", 0.7);
        palabrasSpam.put("rápido", 0.6);
        palabrasSpam.put("préstamo", 0.7);
        palabrasSpam.put("exclusiva", 0.6);
        palabrasSpam.put("descuento", 0.7);
    }

    // Funciones de activación (igual que antes)
    public double escalon(double x) {
        return (x >= 0.5) ? 1.0 : 0.0;
    }

    public double sigmoide(double x) {
        return 1.0 / (1.0 + Math.exp(-x));
    }

    public double relu(double x) {
        return Math.max(0.0, x);
    }

    public double tanh(double x) {
        return Math.tanh(x);
    }

    public double softmax(double x) {
        return Math.exp(x) / (1.0 + Math.exp(x));
    }

    public double lineal(double x) {
        return x;
    }

    public double predecir(double[] entrada) {
        double suma = bias;
        for (int i = 0; i < pesos.length; i++) {
            suma += pesos[i] * entrada[i];
        }
        return suma;
    }

    public double calcularPuntajeMensaje(String mensaje) {
        double puntajeTotal = 0.0;
        mensaje = mensaje.toLowerCase();
        
        // Contar ocurrencias de palabras clave
        int contadorPalabrasSpam = 0;
        for (String palabra : palabrasSpam.keySet()) {
            if (mensaje.contains(palabra)) {
                puntajeTotal += palabrasSpam.get(palabra);
                contadorPalabrasSpam++;
            }
        }

        // Bonus por múltiples palabras de spam
        if (contadorPalabrasSpam > 1) {
            puntajeTotal *= (1 + (contadorPalabrasSpam * 0.2));
        }

        // Normalizar puntaje
        return Math.min(puntajeTotal, 1.0);
    }

    public boolean esSpam(double puntaje) {
        // Criterios más estrictos para spam
        return puntaje >= 0.6 || 
               (this.sigmoide(puntaje) >= 0.7) || 
               (this.escalon(puntaje) == 1.0);
    }

    public static void main(String[] args) {
        // Configurar la codificación UTF-8
        try {
            System.setOut(new java.io.PrintStream(System.out, true, "UTF-8"));
        } catch (UnsupportedEncodingException e) {
            System.err.println("Error al configurar la codificación UTF-8");
        }

        // Usar Scanner con UTF-8
        Scanner scanner = new Scanner(System.in, "UTF-8");
        SpamPerceptron perceptron = new SpamPerceptron(1);

        while (true) {
            System.out.print("\n🔍 Ingrese un mensaje (o 'salir' para terminar): ");
            String mensaje = scanner.nextLine();

            if (mensaje.equalsIgnoreCase("salir")) {
                break;
            }

            double puntaje = perceptron.calcularPuntajeMensaje(mensaje);
            double[] entrada = {puntaje};
            double suma = perceptron.predecir(entrada);

            // Imprimir resultados con emojis y colores
            System.out.println("\n📊 Análisis del Mensaje:");
            System.out.printf("🔢 Puntaje de Spam:       %.2f%n", puntaje);
            System.out.printf("📈 Suma Perceptrón:       %.2f%n", suma);
            System.out.println("\n🧠 Resultados de Funciones de Activación:");
            System.out.printf("🚦 Escalón:               %.2f%n", perceptron.escalon(suma));
            System.out.printf("📊 Sigmoide:             %.2f%n", perceptron.sigmoide(suma));
            System.out.printf("🔥 ReLU:                 %.2f%n", perceptron.relu(suma));
            System.out.printf("📐 Tangente Hiperbólica: %.2f%n", perceptron.tanh(suma));
            System.out.printf("🔄 Softmax:              %.2f%n", perceptron.softmax(suma));
            System.out.printf("➡️ Lineal:               %.2f%n", perceptron.lineal(suma));

            // Clasificación de spam con emojis y criterios más precisos
            if (perceptron.esSpam(puntaje)) {
                System.out.println("\n⚠️ ¡Alerta! El mensaje es considerado SPAM 🚫");
            } else {
                System.out.println("\n✅ El mensaje NO es spam 👍");
            }
        }

        scanner.close();
        System.out.println("\n👋 ¡Hasta luego!");
    }
}