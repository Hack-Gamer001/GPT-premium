#!/bin/bash

# run.sh - Script para ejecutar código en diferentes lenguajes
# Uso: ./run.sh <lenguaje>
# Lenguajes soportados: js, java, py, cs

# Función para mostrar ayuda
usage() {
    echo "Usage: ./run.sh <language>"
    echo "Supported languages:"
    echo "  js   - JavaScript (Node.js)"
    echo "  java - Java"
    echo "  py   - Python"
    echo "  cs   - C# (.NET)"
    exit 1
}

# Verificar argumentos
if [ $# -eq 0 ]; then
    usage
fi

# Configuración para C#
setup_csharp_project() {
    # Crear proyecto solo si no existe
    if [ ! -f "SpamPerceptron.csproj" ]; then
        echo "Creating new .NET project..."
        dotnet new console --force > /dev/null 2>&1
        
        # Renombrar el archivo original si existe
        if [ -f "Program.cs" ]; then
            mv Program.cs Program.cs.bak
        fi
        
        # Copiar nuestro archivo como Program.cs
        if [ -f "SpamPerceptron.cs" ]; then
            cp SpamPerceptron.cs Program.cs
        else
            echo "Error: SpamPerceptron.cs not found!"
            exit 1
        fi
    fi
}

# Ejecutar según el lenguaje
case "$1" in
    js)
        echo "Running SpamPerceptron.js with Node.js..."
        [ -f "SpamPerceptron.js" ] && node SpamPerceptron.js || echo "Error: SpamPerceptron.js not found!"
        ;;
    java)
        echo "Compiling and running SpamPerceptron.java..."
        if [ -f "SpamPerceptron.java" ]; then
            javac SpamPerceptron.java && java SpamPerceptron
        else
            echo "Error: SpamPerceptron.java not found!"
        fi
        ;;
    py)
        echo "Running SpamPerceptron.py with Python..."
        [ -f "SpamPerceptron.py" ] && python3 SpamPerceptron.py || echo "Error: SpamPerceptron.py not found!"
        ;;
    cs)
    echo "Running SpamPerceptron.cs directly..."
    if [ -f "SpamPerceptron.cs" ]; then
        # Método 1: Usar dotnet-script si está instalado
        if command -v dotnet-script &> /dev/null; then
            dotnet-script SpamPerceptron.cs
        else
            # Método 2: Compilación temporal minimalista
            TEMP_DIR=$(mktemp -d)
            dotnet build -nologo -v:q \
                /p:GenerateRuntimeConfigurationFiles=false \
                /p:GenerateBuildDependencyFile=false \
                /p:OutputPath="$TEMP_DIR" \
                SpamPerceptron.cs > /dev/null 2>&1
            
            if [ -f "$TEMP_DIR/SpamPerceptron.dll" ]; then
                dotnet "$TEMP_DIR/SpamPerceptron.dll"
                rm -rf "$TEMP_DIR"
            else
                echo "Error: Compilation failed"
                exit 1
            fi
        fi
    else
        echo "Error: SpamPerceptron.cs not found!"
        exit 1
    fi
    ;;
    *)
        echo "Unsupported language: $1"
        usage
        ;;
esac

exit 0