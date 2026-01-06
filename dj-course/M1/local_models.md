# Using Ollama for Local LLM Models

## What is Ollama?

Ollama is an open-source tool that makes it easy to download and run large language models locally on your machine. It provides an OpenAI-compatible API endpoint, making it seamless to integrate with Python scripts.

## Installation

### Option 1: Official Download (Recommended)
1. Download from: https://ollama.ai
2. Install for your OS (macOS, Linux, Windows)
3. Verify installation:
   ```bash
   ollama --version
   ```

### Option 2: Install via apt-get (Linux)

```bash
# Add Ollama repository
curl -fsSL https://ollama.ai/install.sh | sh

# Or on Debian/Ubuntu
sudo apt-get update
sudo apt-get install ollama

# Verify installation
ollama --version
```

After installation, start the service:
```bash
# Start ollama service
sudo systemctl start ollama

# Enable it to start on boot
sudo systemctl enable ollama

# Check status
sudo systemctl status ollama
```

## Python Virtual Environment and Ollama

**Important:** Ollama runs independently of Python virtual environments.

- **Ollama**: System-wide service that runs the LLM server on `http://localhost:11434`
- **Python venv**: Isolated Python environment for your scripts

### Proper Workflow:

```bash
# 1. Start ollama (system-wide, independent of venv)
ollama serve
# OR if installed as service:
sudo systemctl start ollama

# 2. In another terminal, activate your Python venv
source ~/AI/mlflow/bin/activate

# 3. Run your Python scripts that connect to ollama
python3 run-local-model.py
```

The Python script inside the venv connects to the ollama server via HTTP API - they don't need to be in the same environment.

### Installing Python Dependencies

Your venv needs the OpenAI client library to connect to ollama:

```bash
# Activate venv first
source ~/AI/mlflow/bin/activate

# Install dependencies
pip install openai mlflow

# Now your scripts can import these libraries
python3 run-local-model.py
# Scripts came from dj-course/M1/mflow
```

## Downloading Models

Use `ollama pull` to download models to your machine:

```bash
# Download Mistral 7B (recommended for most systems)
ollama pull mistral

# Download other models
ollama pull llama2
ollama pull neural-chat
ollama pull openhermes
```

Models are automatically downloaded to `~/.ollama/models/` and can be quite large (2-40GB depending on the model).

**Browse available models:** https://ollama.ai/library

## Starting the Server

Start the Ollama server to make models accessible via API:

```bash
ollama serve
```

This starts a server on `http://localhost:11434/v1` that is OpenAI API-compatible.

The server will keep running in the terminal. Open another terminal to run your scripts.

## Using with Python

Once the server is running, connect using the OpenAI Python client:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="sk-not-needed",  # API key not required for local server
)

response = client.chat.completions.create(
    model="mistral",  # or "llama2", "neural-chat", etc.
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(response.choices[0].message.content)
```

## Example: Using with MLflow

The `run-local-model.py` script is already configured to work with Ollama:

```python
OLLAMA_SERVER = {
    "engine": "ollama",
    "model": "mistral",  # Change to any model you've pulled
    "base_url": "http://localhost:11434/v1",
}
SERVER = OLLAMA_SERVER
```

Then run:
```bash
python3 run-local-model.py
```

## Quick Start Guide

**Terminal 1 - Start Ollama:**
```bash
ollama pull mistral
ollama serve
```

**Terminal 2 - Run your script:**
```bash
cd ~/AI/dj-course/M1/mlflow
python3 run-local-model.py
```

## Useful Commands

### List Downloaded Models

Lists all models that have been downloaded to your system.

```bash
ollama list
```

**Output example:**
```
NAME              ID              SIZE      MODIFIED       
mistral:latest    6577803aa9a0    4.4 GB    15 minutes ago
llama2:latest     78e26419b446    3.8 GB    2 hours ago
neural-chat:latest a5ffff4c0fa2    4.1 GB    1 day ago
```

**Description:** This command displays a table with:
- **NAME**: Model name and tag (e.g., `mistral:latest`)
- **ID**: Unique model identifier (SHA256 digest)
- **SIZE**: Disk space used by the model
- **MODIFIED**: When the model was last accessed or downloaded

### Run a Model Interactively

Start an interactive chat session with a model:

```bash
ollama run mistral
```

This opens an interactive prompt where you can type questions and get responses directly in the terminal. Press `Ctrl+D` to exit.

### Show Model Information

Display detailed information about a specific model:

```bash
ollama show mistral
```

**Output includes:**
- Model architecture
- Parameters
- Model size and format
- Quantization level

### Remove/Delete a Model

Remove a downloaded model from your system:

```bash
ollama rm mistral
```

This frees up disk space by deleting the model files.

### Copy a Model

Create a copy of an existing model with a new name:

```bash
ollama cp mistral my-mistral-copy
```

### Pull a Specific Model Version

Download a specific version or variant:

```bash
# Pull a specific tag
ollama pull mistral:7b
ollama pull llama2:13b

# List available tags at https://ollama.com/library
```

## Creating Custom Models with Modelfile

### What is a Modelfile?

A **Modelfile** is a configuration file (similar to Dockerfile) that allows you to:
- Customize a base model with system prompts
- Define conversation templates
- Set model parameters (temperature, top_k, top_p)
- Create reusable model variants

### Modelfile Structure

A basic Modelfile contains:

```dockerfile
FROM <base-model>
SYSTEM "<system-prompt>"
TEMPLATE """<prompt-template>"""
PARAMETER temperature <value>
PARAMETER top_k <value>
PARAMETER top_p <value>
```

### Modelfile Components

#### 1. **FROM** (Required)
Specifies the base model to use:

```dockerfile
FROM mistral
FROM llama2:13b
FROM bielik-7b-instruct
```

#### 2. **SYSTEM** (Optional)
Sets the system prompt that guides the model's behavior:

```dockerfile
SYSTEM "You are a helpful programming assistant. Your answers are concise and practical."
```

#### 3. **TEMPLATE** (Optional)
Defines how user messages are formatted for the model:

```dockerfile
TEMPLATE """[INST] {{.System}}

{{.Prompt}} [/INST]"""
```

Variables available:
- `{{.System}}` - System prompt content
- `{{.Prompt}}` - User's input message
- `{{.Response}}` - Model's response

#### 4. **PARAMETER** (Optional)
Set model parameters:

```dockerfile
PARAMETER temperature 0.7    # Creativity (0.0-1.0)
PARAMETER top_k 40          # Top K sampling
PARAMETER top_p 0.9         # Nucleus sampling
PARAMETER repeat_penalty 1.1 # Penalize repetition
```

### Complete Modelfile Example

**File: `Modelfile`**

```dockerfile
FROM mistral

SYSTEM "You are a Polish poet. Your responses are always in Polish poetry form, with rhyming couplets."

TEMPLATE """[INST] {{.System}}

User: {{.Prompt}}
Poet: [/INST]"""

PARAMETER temperature 0.8
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.2
```

### Creating a Custom Model

#### Step 1: Create a Modelfile

```bash
# Create a new directory for your model
mkdir my-custom-model
cd my-custom-model

# Create the Modelfile (no file extension)
cat > Modelfile << 'EOF'
FROM mistral

SYSTEM "You are an expert software engineer. You provide detailed, practical solutions."

TEMPLATE """[INST] {{.System}}

Question: {{.Prompt}} [/INST]"""

PARAMETER temperature 0.5
PARAMETER top_k 40
EOF
```

#### Step 2: Build the Model

```bash
ollama create my-engineer-model -f ./Modelfile
```

**Output:**
```
transferring model data
writing manifest
success
```

#### Step 3: Use Your Custom Model

```bash
# Run interactively
ollama run my-engineer-model

# Use in Python
python3 << 'EOF'
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="sk-not-needed"
)

response = client.chat.completions.create(
    model="my-engineer-model",
    messages=[{"role": "user", "content": "How do I optimize Python code?"}]
)

print(response.choices[0].message.content)
EOF
```

### Real-World Example: Creating a Poet Model

```bash
# Create directory structure
mkdir -p models/poet-model
cd models/poet-model

# Create Modelfile
cat > Modelfile << 'EOF'
FROM mistral

SYSTEM "You are a romantic poet. Write responses in iambic pentameter with emotional depth. Every response should be exactly 8 lines."

TEMPLATE """[INST] {{.System}}

Theme: {{.Prompt}} [/INST]"""

PARAMETER temperature 0.9
PARAMETER top_p 0.9
EOF

# Create the model
ollama create poet -f ./Modelfile

# Test it
ollama run poet
# Type: love, loss, nature, etc.
```

### Managing Custom Models

```bash
# List all models (including custom ones)
ollama list

# Show custom model details
ollama show poet

# Export/backup a model (creates a modelfile)
ollama export poet > poet-backup.modelfile

# Delete a custom model
ollama rm poet
```

### Advanced: Model Parameters Explained

| Parameter | Range | Description |
|-----------|-------|-------------|
| `temperature` | 0.0-1.0 | Lower = more focused, Higher = more creative |
| `top_k` | 1-100 | Consider only top K most likely tokens |
| `top_p` | 0.0-1.0 | Nucleus sampling (consider tokens until probability sum) |
| `repeat_penalty` | 0.0-2.0 | Penalize model for repeating tokens (>1.1 recommended) |
| `num_predict` | -1 to N | Max tokens to generate (-1 = unlimited) |
| `num_ctx` | 128-2048+ | Context window size |

### Updating Existing Custom Models

To modify a custom model, edit the Modelfile and recreate:

```bash
# Edit your Modelfile
nano Modelfile

# Remove the old version
ollama rm my-engineer-model

# Create the updated version
ollama create my-engineer-model -f ./Modelfile
```

## Checking Running Models

To see which model is currently loaded and running:

```bash
# Check if ollama process is running
ps aux | grep ollama

# Check which model is loaded
curl http://localhost:11434/api/tags
```

The output will show:
```json
{
  "models": [
    {
      "name": "mistral:latest",
      "modified_at": "2024-01-15T10:30:00.000Z",
      "size": 5368709120,
      "digest": "abc123..."
    }
  ]
}
```

## Stopping/Deactivating Ollama

### Stop the server:

**Option 1 - Kill the process:**
```bash
# Find ollama process
ps aux | grep ollama

# Kill it (replace PID with actual process ID)
kill <PID>

# Or force kill
killall ollama
```

**Option 2 - Stop gracefully in terminal:**
- If ollama server is running in a terminal, press `Ctrl+C` to stop it

### Unload a specific model without stopping server:

```bash
# This will free up memory without stopping the server
curl -X POST http://localhost:11434/api/generate -d '{"model": "mistral", "prompt": "", "stream": false}'
```

### Check memory usage:

```bash
# See all running processes
ps aux | grep ollama

# On Linux, check memory
free -h
```

## Recommended Models

- **mistral** (7B) - Fast, good for most tasks
- **llama2** (7B) - Good all-rounder
- **neural-chat** (7B) - Optimized for conversation
- **openchat** (3.5B) - Very fast, smaller model

## Troubleshooting

- **"Connection refused"**: Make sure `ollama serve` is running in another terminal
- **Model not found**: Run `ollama pull <model-name>` first
- **Slow responses**: Try a smaller model like `openchat` or `orca-mini`
- **Out of memory**: Use quantized versions or smaller models
