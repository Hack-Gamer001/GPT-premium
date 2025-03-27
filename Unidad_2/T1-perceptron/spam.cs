using System;
using System.Linq;
using System.Numerics;
using System.Windows.Forms;
using LiveCharts;
using LiveCharts.WinForms;
using LiveCharts.Wpf;

public class ActivationFunctions
{
    public static double Linear(double x) => x;
    public static double Step(double x) => x > 0 ? 1 : 0;
    public static double Sigmoid(double x) => 1 / (1 + Math.Exp(-x));
    public static double ReLU(double x) => Math.Max(0, x);
    public static double Tanh(double x) => Math.Tanh(x);
}

public class Perceptron
{
    private double[] weights;
    private double bias;
    private int inputSize;
    private string activationFunc;
    private double learningRate;
    private int epochs;

    public Perceptron(int inputSize, string activationFunc = "sigmoid", double learningRate = 0.1, int epochs = 100)
    {
        this.inputSize = inputSize;
        this.activationFunc = activationFunc;
        this.learningRate = learningRate;
        this.epochs = epochs;
        this.weights = new double[inputSize];
        this.bias = new Random().NextDouble();

        // Inicializar pesos aleatorios
        Random rand = new Random();
        for (int i = 0; i < inputSize; i++)
            weights[i] = rand.NextDouble();
    }

    private double Activate(double x)
    {
        return activationFunc switch
        {
            "linear" => ActivationFunctions.Linear(x),
            "step" => ActivationFunctions.Step(x),
            "sigmoid" => ActivationFunctions.Sigmoid(x),
            "relu" => ActivationFunctions.ReLU(x),
            "tanh" => ActivationFunctions.Tanh(x),
            _ => throw new ArgumentException("Función de activación no válida"),
        };
    }

    public double Predict(double[] inputs)
    {
        double z = inputs.Zip(weights, (x, w) => x * w).Sum() + bias;
        return Activate(z);
    }

    public void Train(double[][] X, double[] y)
    {
        for (int epoch = 0; epoch < epochs; epoch++)
        {
            for (int i = 0; i < X.Length; i++)
            {
                double prediction = Predict(X[i]);
                double error = y[i] - prediction;

                for (int j = 0; j < inputSize; j++)
                    weights[j] += learningRate * error * X[i][j];

                bias += learningRate * error;
            }
        }
    }
}

public class MainForm : Form
{
    private CartesianChart chart;

    public MainForm()
    {
        Text = "Perceptrón - Clasificación de Spam";
        Width = 800;
        Height = 600;

        chart = new CartesianChart
        {
            Dock = DockStyle.Fill
        };
        Controls.Add(chart);

        RunPerceptron();
    }

    private void RunPerceptron()
    {
        double[][] trainingData =
        {
            new double[] {7, 4, 0.57},
            new double[] {8, 3, 0.38},
            new double[] {7, 0, 0.0},
            new double[] {6, 4, 0.67},
            new double[] {5, 3, 0.6},
            new double[] {7, 4, 0.57}
        };

        double[] labels = { 1, 0, 0, 1, 0, 1 };

        Perceptron perceptron = new Perceptron(inputSize: 3, activationFunc: "sigmoid");
        perceptron.Train(trainingData, labels);

        double[] predictions = trainingData.Select(sample => perceptron.Predict(sample)).ToArray();
        double accuracy = predictions.Select((p, i) => Math.Round(p) == labels[i] ? 1 : 0).Average();

        chart.Series = new SeriesCollection
        {
            new LineSeries
            {
                Title = "Precisión",
                Values = new ChartValues<double> { accuracy }
            }
        };
        chart.AxisX.Add(new Axis { Title = "Entrenamiento", Labels = new[] { "Época 1" } });
        chart.AxisY.Add(new Axis { Title = "Precisión", MinValue = 0, MaxValue = 1 });
    }
}

public static class Program
{
    [STAThread]
    public static void Main()
    {
        Application.EnableVisualStyles();
        Application.Run(new MainForm());
    }
}
