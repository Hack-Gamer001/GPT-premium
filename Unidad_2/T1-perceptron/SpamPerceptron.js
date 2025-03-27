class SpamPerceptron {
    constructor(numEntradas) {
        // Inicializar pesos con valores aleatorios
        this.pesos = new Array(numEntradas).fill(0).map(() => Math.random() * 0.2 - 0.1);
        this.bias = Math.random() * 0.2 - 0.1;

        // Diccionario de palabras clave de spam más completo
        this.palabrasSpam = {
            // Palabras generales de spam
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

            // Palabras específicas de ofertas y engaños
            'iphone': 0.9,
            'clic': 0.6,
            'oferta': 0.6,
            'dinero': 0.7,
            'rápido': 0.6,
            'préstamo': 0.7,
            'exclusiva': 0.6,
            'descuento': 0.7
        };
    }

    // Funciones de activación
    escalon(x) {
        return (x >= 0.5) ? 1.0 : 0.0;
    }

    sigmoide(x) {
        return 1.0 / (1.0 + Math.exp(-x));
    }

    relu(x) {
        return Math.max(0.0, x);
    }

    tanh(x) {
        return Math.tanh(x);
    }

    softmax(x) {
        return Math.exp(x) / (1.0 + Math.exp(x));
    }

    lineal(x) {
        return x;
    }

    predecir(entrada) {
        let suma = this.bias;
        for (let i = 0; i < this.pesos.length; i++) {
            suma += this.pesos[i] * entrada[i];
        }
        return suma;
    }

    calcularPuntajeMensaje(mensaje) {
        let puntajeTotal = 0.0;
        mensaje = mensaje.toLowerCase();

        // Contar ocurrencias de palabras clave
        let contadorPalabrasSpam = 0;
        for (let palabra in this.palabrasSpam) {
            if (mensaje.includes(palabra)) {
                puntajeTotal += this.palabrasSpam[palabra];
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

    esSpam(puntaje) {
        // Criterios más estrictos para spam
        return puntaje >= 0.6 || 
               (this.sigmoide(puntaje) >= 0.7) || 
               (this.escalon(puntaje) == 1.0);
    }

    // Método para analizar mensaje con interfaz de consola
    analizarMensaje(mensaje) {
        const puntaje = this.calcularPuntajeMensaje(mensaje);
        const entrada = [puntaje];
        const suma = this.predecir(entrada);

        // Preparar resultados
        const resultados = {
            'mensaje': mensaje,
            'puntajeDeSPam': puntaje.toFixed(2),
            'sumaPerceptron': suma.toFixed(2),
            'funcionesDeActivacion': {
                'escalon': this.escalon(suma).toFixed(2),
                'sigmoide': this.sigmoide(suma).toFixed(2),
                'relu': this.relu(suma).toFixed(2),
                'tanh': this.tanh(suma).toFixed(2),
                'softmax': this.softmax(suma).toFixed(2),
                'lineal': this.lineal(suma).toFixed(2)
            },
            'esSpam': this.esSpam(puntaje)
        };

        return resultados;
    }
}

// Función para ejecutar en navegador o Node.js
function ejecutarAnalizadorSpam() {
    const perceptron = new SpamPerceptron(1);
    
    // Modo interactivo en Node.js
    if (typeof window === 'undefined') {
        const readline = require('readline');
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        function preguntarMensaje() {
            rl.question('\n🔍 Ingrese un mensaje (o "salir" para terminar): ', (mensaje) => {
                if (mensaje.toLowerCase() === 'salir') {
                    rl.close();
                    return;
                }

                const resultado = perceptron.analizarMensaje(mensaje);
                
                console.log('\n📊 Análisis del Mensaje:');
                console.log(`🔢 Puntaje de Spam:       ${resultado.puntajeDeSPam}`);
                console.log(`📈 Suma Perceptrón:       ${resultado.sumaPerceptron}`);
                
                console.log('\n🧠 Resultados de Funciones de Activación:');
                console.log(`🚦 Escalón:               ${resultado.funcionesDeActivacion.escalon}`);
                console.log(`📊 Sigmoide:             ${resultado.funcionesDeActivacion.sigmoide}`);
                console.log(`🔥 ReLU:                 ${resultado.funcionesDeActivacion.relu}`);
                console.log(`📐 Tangente Hiperbólica: ${resultado.funcionesDeActivacion.tanh}`);
                console.log(`🔄 Softmax:              ${resultado.funcionesDeActivacion.softmax}`);
                console.log(`➡️ Lineal:               ${resultado.funcionesDeActivacion.lineal}`);

                // Clasificación de spam con emojis
                if (resultado.esSpam) {
                    console.log("\n⚠️ ¡Alerta! El mensaje es considerado SPAM 🚫");
                } else {
                    console.log("\n✅ El mensaje NO es spam 👍");
                }

                preguntarMensaje(); // Continuar con el siguiente mensaje
            });
        }

        preguntarMensaje();
    } 
    // Modo para navegador
    else {
        window.analizarMensajeSpam = function(mensaje) {
            const resultado = perceptron.analizarMensaje(mensaje);
            
            // Para navegador, podrías usar esto para mostrar resultados
            console.log('Resultado del análisis:', resultado);
            
            return resultado;
        };
    }
}

// Ejecutar el analizador
ejecutarAnalizadorSpam();