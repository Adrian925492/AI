#!/bin/bash

# Setup script for Gemini MLflow integration

echo "🔧 Setting up Gemini + MLflow integration..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found in current directory."
    echo ""
    echo "Create a .env file with your Google API key:"
    echo ""
    echo "1. Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
    echo "2. Create .env file:"
    echo "   echo \"GOOGLE_API_KEY='your-api-key-here'\" > .env"
    echo ""
    exit 1
fi

# Check if required Python packages are installed
echo "📦 Checking Python packages..."

REQUIRED_PACKAGES=("google.generativeai:google-generativeai" "mlflow" "dotenv:python-dotenv")

for package in "${REQUIRED_PACKAGES[@]}"; do
    # Split package name and import name
    IFS=':' read -r import_name install_name <<< "$package"
    import_name=${import_name:-$install_name}
    
    python3 -c "import $import_name" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ Package '$install_name' not found. Installing..."
        pip install "$install_name"
    else
        echo "✅ $install_name is installed"
    fi
done

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the Gemini model with MLflow tracking:"
echo "  python3 run-gemini-model.py"
echo ""
