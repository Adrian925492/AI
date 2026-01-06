#!/usr/bin/env python3
"""
List available Gemini models from the API
"""
import google.genai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Configure the client
client = genai.Client(api_key=GEMINI_API_KEY)

print("📋 Available Gemini Models:\n")
print("-" * 60)

try:
    # List available models
    models = client.models.list()
    
    for model in models:
        print(f"Name: {model.name}")
        if hasattr(model, 'display_name'):
            print(f"Display Name: {model.display_name}")
        if hasattr(model, 'description'):
            print(f"Description: {model.description}")
        if hasattr(model, 'input_token_limit'):
            print(f"Max Input Tokens: {model.input_token_limit}")
        if hasattr(model, 'output_token_limit'):
            print(f"Max Output Tokens: {model.output_token_limit}")
        print("-" * 60)

except Exception as e:
    print(f"❌ Error listing models: {e}")
