#!/bin/bash

# Setup script for OpenAI + MLflow integration

echo "🔧 Setting up OpenAI + MLflow integration..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found in current directory."
    echo ""
    echo "Create a .env file with your OpenAI API key:"
    echo ""
    echo "1. Get your API key from: https://platform.openai.com/api-keys"
    echo ""
    echo "2. Create .env file:"
    echo "   echo \"OPENAI_API_KEY='your-api-key-here'\" >> .env"
    echo ""
    exit 1
fi

# Check if OPENAI_API_KEY exists in .env
if ! grep -q "OPENAI_API_KEY" .env; then
    echo "⚠️  OPENAI_API_KEY not found in .env file."
    echo ""
    echo "Add it to your .env with:"
    echo "   echo \"OPENAI_API_KEY='your-api-key-here'\" >> .env"
    echo ""
    exit 1
fi

# Check if required Python packages are installed
echo "📦 Checking Python packages..."

REQUIRED_PACKAGES=("openai" "mlflow" "dotenv:python-dotenv")

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
echo "To run the OpenAI model with MLflow tracking:"
echo "  python3 run-openai-model.py"
echo ""
