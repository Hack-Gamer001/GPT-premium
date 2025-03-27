import java.util.*;

public class Perceptron {
    private double[] pesos;
    private double bias;

    public Perceptron(int numEntradas) {
        pesos = new double[numEntradas];
        Arrays.fill(pesos, 0.4); // Pesos iniciales aumentados
        bias = 0.4; // Bias ajustado
    }

    public double escalon(double x) { return (x >= 0.8) ? 1 : 0; } 
    public double sigmoide(double x) { return 1 / (1 + Math.exp(-x)); }
    public double relu(double x) { return Math.max(0, x); }
    public double tanh(double x) { return Math.tanh(x); }
    public double softmax(double x) { return Math.exp(x) / (1 + Math.exp(x)); } // Softmax simplificado para una única entrada
    public double lineal(double x) { return x; }

    public double predecir(double[] entrada) {
        double suma = bias;
        for (int i = 0; i < pesos.length; i++) {
            suma += pesos[i] * entrada[i];
        }
        return suma; // Retorna la suma sin aplicar función aún
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        Map<String, Double> palabrasX1 = new HashMap<>();
        palabrasX1.put("gana", 0.5);
        palabrasX1.put("gratis", 0.6);
        palabrasX1.put("iphone", 0.6);
        palabrasX1.put("clic", 0.5);
        palabrasX1.put("oferta", 0.4);
        palabrasX1.put("dinero", 0.5);
        palabrasX1.put("rápido", 0.4);
        palabrasX1.put("préstamo", 0.5);
        palabrasX1.put("cuenta", 0.5);
        palabrasX1.put("exclusiva", 0.4);

        System.out.print("Escribe tu mensaje: ");
        String mensaje = scanner.nextLine().toLowerCase();

        double x1 = 0.0;
        for (String palabra : palabrasX1.keySet()) {
            if (mensaje.contains(palabra)) {
                x1 += palabrasX1.get(palabra);
            }
        }

        double[] entrada = {x1};
        Perceptron perceptron = new Perceptron(1);

        double suma = perceptron.predecir(entrada);

        double resultadoEscalon = perceptron.escalon(suma);
        double resultadoSigmoide = perceptron.sigmoide(suma);
        double resultadoReLU = perceptron.relu(suma);
        double resultadoTanh = perceptron.tanh(suma);
        double resultadoSoftmax = perceptron.softmax(suma);
        double resultadoLineal = perceptron.lineal(suma);

        System.out.println("\nPredicción para el mensaje:");
        System.out.println("Escalón: " + resultadoEscalon);
        System.out.println("Sigmoide: " + resultadoSigmoide);
        System.out.println("ReLU: " + resultadoReLU);
        System.out.println("Tangente Hiperbólica: " + resultadoTanh);
        System.out.println("Softmax: " + resultadoSoftmax);
        System.out.println("Lineal: " + resultadoLineal);

        if (resultadoEscalon == 1 || resultadoSigmoide >= 0.7) {
            System.out.println("\nEl mensaje es considerado SPAM.");
        } else {
            System.out.println("\nEl mensaje NO es spam.");
        }

        scanner.close();
    }
}
