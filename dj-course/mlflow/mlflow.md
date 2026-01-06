# MLflow - Model Tracking and Management

## What is MLflow?

MLflow is an open-source platform for managing machine learning workflows. It helps you:
- Track experiments and parameters
- Log metrics and models
- Compare model performance
- Manage model versions
- Deploy models

For this course, we use MLflow to track LLM interactions, prompts, responses, and performance metrics.

## Installation

MLflow is already installed in the `~/AI/mlflow` virtual environment:

```bash
source ~/AI/mlflow/bin/activate
pip install mlflow
```

## Starting MLflow Server

MLflow provides a web UI to view your experiments and runs.

### Start the server:

```bash
# Activate venv first
source ~/AI/mlflow/bin/activate

# Start MLflow UI on localhost:5000
mlflow ui --host 127.0.0.1 --port 5000
```

The UI will be available at: `http://127.0.0.1:5000`

### Using different backend storage:

```bash
# SQLite (local, file-based)
mlflow ui --backend-store-uri sqlite:///./mlflow.db

# Default (in-memory, for testing)
mlflow ui
```

## Stopping MLflow Server

### Option 1 - In the terminal:
Press `Ctrl+C` in the terminal where MLflow is running.

### Option 2 - Kill the process:
```bash
# Find the MLflow process
ps aux | grep mlflow

# Kill it (replace PID)
kill <PID>

# Or force kill
pkill -f mlflow
```

## Configuring MLflow with Different LLM Providers

### 1. Using with Ollama (Local)

**Setup:**
```python
import mlflow
from openai import OpenAI

# Configure MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("ollama_experiments")
mlflow.openai.autolog()

# Connect to Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="sk-not-needed"
)

# Use in MLflow tracking
with mlflow.start_run():
    response = client.chat.completions.create(
        model="mistral",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)
```

**Requirements:**
- Ollama running: `ollama serve`
- MLflow server: `mlflow ui --host 127.0.0.1 --port 5000`

---

### 2. Using with Google Generative AI (Gemini)

**Setup:**

```bash
# Install Gemini SDK
pip install google-generativeai
```

```python
import mlflow
import google.generativeai as genai

# Configure API key
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

# Configure MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("gemini_experiments")

# Use Gemini with MLflow tracking
with mlflow.start_run():
    model = genai.GenerativeModel('gemini-pro')
    
    mlflow.log_param("model", "gemini-pro")
    
    response = model.generate_content("Hello, how are you?")
    
    mlflow.log_text(response.text, "response.txt")
    print(response.text)
```

**Get API Key:**
1. Go to: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Set environment variable: `export GOOGLE_API_KEY="your-key-here"`

---

### 3. Using with OpenAI (via Copilot/ChatGPT API)

**Setup:**

```bash
# Install OpenAI SDK
pip install openai
```

```python
import mlflow
from openai import OpenAI

# Configure MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("openai_experiments")
mlflow.openai.autolog()

# Connect to OpenAI
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# Use with MLflow tracking
with mlflow.start_run():
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)
```

**Get API Key:**
1. Go to: https://platform.openai.com/account/api-keys
2. Create a new API key
3. Set environment variable: `export OPENAI_API_KEY="your-key-here"`

---

### 4. Using with Anthropic Claude (via Copilot)

**Setup:**

```bash
# Install Anthropic SDK
pip install anthropic
```

```python
import mlflow
from anthropic import Anthropic

# Configure MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("claude_experiments")

# Connect to Claude
client = Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

# Use with MLflow tracking
with mlflow.start_run():
    mlflow.log_param("model", "claude-3-opus")
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
    
    text = response.content[0].text
    mlflow.log_text(text, "response.txt")
    print(text)
```

**Get API Key:**
1. Go to: https://console.anthropic.com/account/keys
2. Create a new API key
3. Set environment variable: `export ANTHROPIC_API_KEY="your-key-here"`

---

## Complete Workflow Example

### Terminal 1 - Start Ollama:
```bash
ollama serve
```

### Terminal 2 - Start MLflow:
```bash
source ~/AI/mlflow/bin/activate
mlflow ui --host 127.0.0.1 --port 5000
```

### Terminal 3 - Run your script:
```bash
cd ~/AI/dj-course/M1/mlflow
source ~/AI/mlflow/bin/activate
python3 run-local-model.py
```

Visit `http://127.0.0.1:5000` to see your experiments tracked.

## MLflow Commands

```bash
# View all experiments
mlflow experiments list

# View runs for an experiment
mlflow runs list --experiment-name "ollama_experiments"

# Export run data
mlflow runs export --run-id <RUN_ID> --output-path ./export

# Serve a model
mlflow models serve -m ./path/to/model
```

## Logging Data to MLflow

```python
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("temperature", 0.7)
    mlflow.log_param("max_tokens", 150)
    
    # Log metrics
    mlflow.log_metric("response_time", 1.23)
    mlflow.log_metric("tokens_used", 45)
    
    # Log artifacts (files)
    mlflow.log_text(response_text, "response.txt")
    mlflow.log_artifact("./config.json")
    
    # Log tags
    mlflow.set_tag("model_type", "ollama")
    mlflow.set_tag("environment", "local")
```

## Comparing Models

MLflow UI makes it easy to compare:
1. Open `http://127.0.0.1:5000`
2. Go to "Experiments"
3. Select runs to compare
4. View side-by-side metrics and parameters

This helps you evaluate which model/configuration works best for your use case.

## Troubleshooting

- **Port 5000 already in use**: Use `mlflow ui --port 5001` instead
- **Connection refused**: Make sure MLflow server is running
- **Autolog not working**: Restart the script after starting MLflow server
- **API key not found**: Set environment variables: `export OPENAI_API_KEY="..."`
