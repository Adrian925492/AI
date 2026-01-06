# Using Google Gemini with MLflow

This guide shows how to use Google's Gemini API with MLflow for experiment tracking.

## Prerequisites

1. **Google API Key** - Get it from https://makersuite.google.com/app/apikey
2. **Python 3.8+**
3. **MLflow running** - Start with: `mlflow ui`

## Setup

### Step 1: Create .env File with Your API Key

Create a `.env` file in the mlflow directory:

```bash
cd ~/AI/course/mlflow
echo "GOOGLE_API_KEY='your-api-key-here'" > .env
```

Or manually create `.env` and add:
```
GOOGLE_API_KEY=your-api-key-here
```

Get your API key from: https://makersuite.google.com/app/apikey

### Step 2: Install Required Packages

```bash
# Activate your Python virtual environment first
source ~/AI/mlflow/bin/activate

# Install dependencies
pip install google-generativeai mlflow python-dotenv openai
```

Or use the setup script:
```bash
bash setup-gemini.sh
```

## Running the Script

### Option 1: Interactive Terminal

**Terminal 1 - Start MLflow UI:**
```bash
mlflow ui
```
Access it at: http://127.0.0.1:5000

**Terminal 2 - Run the Gemini script:**
```bash
cd ~/AI/course/mlflow
source ~/AI/mlflow/bin/activate
python3 run-gemini-model.py
```

### Option 2: Run with Your Own Prompt

Modify `run-gemini-model.py` and change the `user_message` variable:

```python
user_message = "Your custom prompt here"
```

Then run it:
```bash
python3 run-gemini-model.py
```

## Available Gemini Models

- `gemini-2.0-flash-exp` - Latest experimental model (recommended for speed)
- `gemini-1.5-flash` - Fast, efficient model (good balance)
- `gemini-1.5-pro` - Most capable model (slower)
- `gemini-1.0-pro` - Standard model
- `gemini-pro-vision` - For multimodal input

Change the model in `run-gemini-model.py`:
```python
"model": "gemini-2.0-flash-exp",
```

## MLflow Integration Features

The script logs the following to MLflow:

- **Parameters:**
  - Model name
  - Temperature setting
  - Max tokens

- **Metrics:**
  - Response length

- **Artifacts:**
  - Full response text (`gemini_response.txt`)
  - Errors (if any)

## Viewing Results in MLflow

After running the script, visit http://127.0.0.1:5000 to see:

1. **Experiments** - All Gemini model runs
2. **Runs** - Individual experiment runs
3. **Parameters & Metrics** - Configuration and results
4. **Artifacts** - Saved responses

## Troubleshooting

### "GOOGLE_API_KEY not found in .env file"
Make sure your `.env` file exists with your API key:
```bash
echo "GOOGLE_API_KEY='your-api-key-here'" > .env
```

### "Connection refused" on MLflow
Make sure MLflow UI is running:
```bash
mlflow ui
```

### "API rate limit exceeded"
Google Gemini has rate limits. Wait a few minutes before retrying.

### "Safety threshold exceeded"
The script disables safety filters for testing. You can enable them by modifying the `safety_settings` in the script.

## Comparing with Other Models

You can compare Gemini with other models by checking MLflow experiments:

- **Ollama local** - See `../M1/mlflow/run-local-model.py`
- **OpenAI** - Create similar script using OpenAI API
- **Anthropic Claude** - Create similar script using Anthropic API

## Cost Considerations & Quotas

Google Gemini API has **free tier quotas**:

- **gemini-1.5-flash**: 15 requests per minute (free tier)
- **gemini-2.0-flash**: 10 requests per minute (free tier)
- **Daily limits** also apply - check at https://ai.dev/usage

### If You Hit Quota Limits (429 Error)

**Option 1: Wait for quota reset**
- Free tier quotas reset daily (usually midnight UTC)
- The script will retry automatically with delays

**Option 2: Upgrade to paid plan**
- Visit https://ai.google.dev/pricing
- Enable billing to increase quotas significantly
- Pay only for what you use

**Option 3: Monitor usage**
- Check current usage: https://ai.dev/usage?tab=rate-limit
- Set billing alerts to avoid surprises

### Script Features

- **Automatic retries** with exponential backoff for quota errors
- **Retry delays** to respect rate limits (5, 10, 15 second delays)
- **Error logging** to MLflow for troubleshooting
- **Quota detection** - will inform you when free tier is exceeded

## Next Steps

1. Modify the prompt for your use case
2. Experiment with different models
3. Compare results in MLflow UI
4. Deploy to production using MLflow model registry
