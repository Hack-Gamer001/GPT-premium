const XLSX = require('xlsx');
const fs = require('fs');

// Función para cargar datos desde un archivo Excel
function loadExcelData(filename) {
    const workbook = XLSX.readFile(filename);
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(sheet);
    return data;
}

// Pedir archivo Excel al usuario
const filename = "deteccion_spam.xlsx"; // Reemplázalo con la ruta del archivo real
if (!fs.existsSync(filename)) {
    console.error("El archivo Excel no existe. Asegúrate de proporcionar un archivo válido.");
    process.exit(1);
}

const dataset = loadExcelData(filename);

// Convertir datos del Excel a formato adecuado para el perceptrón
const X_train = dataset.map(row => [row['Frecuencia'], row['PalabraClave1'], row['PalabraClave2'], row['PalabraClave3'], row['PalabraClave4']]);
const y_train = dataset.map(row => row['Spam']);

// Funciones de activación
function linear(x) {
    return x;
}

function step(x) {
    return x >= 0 ? 1 : 0;
}

function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
}

function relu(x) {
    return Math.max(0, x);
}

function softmax(arr) {
    let exps = arr.map(x => Math.exp(x - Math.max(...arr)));
    let sumExps = exps.reduce((a, b) => a + b, 0);
    return exps.map(x => x / sumExps);
}

function tanh(x) {
    return Math.tanh(x);
}

// Perceptrón binario
class Perceptron {
    constructor(inputSize, activation = sigmoid, lr = 0.01, epochs = 20) {
        this.weights = Array.from({ length: inputSize }, () => Math.random());
        this.bias = Math.random();
        this.activation = activation;
        this.lr = lr;
        this.epochs = epochs;
    }

    train(X, y) {
        for (let epoch = 0; epoch < this.epochs; epoch++) {
            let totalError = 0;
            for (let i = 0; i < X.length; i++) {
                let z = X[i].reduce((sum, val, j) => sum + val * this.weights[j], this.bias);
                let yPred = this.activation(z);
                let error = y[i] - yPred;
                totalError += Math.abs(error);
                
                // Actualización de pesos
                for (let j = 0; j < this.weights.length; j++) {
                    this.weights[j] += this.lr * error * X[i][j];
                }
                this.bias += this.lr * error;
            }
            console.log(`Época ${epoch + 1}, Error: ${totalError}`);
        }
    }

    predict(X) {
        return X.map(x => {
            let z = x.reduce((sum, val, j) => sum + val * this.weights[j], this.bias);
            return this.activation(z) >= 0.5 ? 1 : 0;
        });
    }
}

// Entrenar el perceptrón con activación sigmoidal
const perceptron = new Perceptron(X_train[0].length);
perceptron.train(X_train, y_train);

console.log("Pesos finales:", perceptron.weights);
console.log("Bias final:", perceptron.bias);

// Predicción de un nuevo correo (simulado)
const X_test = [[0.2, 0.1, 0.4, 0.0, 0.3]];
console.log("Predicción:", perceptron.predict(X_test));
