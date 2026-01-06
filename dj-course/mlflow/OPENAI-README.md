# Using OpenAI GPT with MLflow

This guide shows how to use OpenAI's GPT models (GPT-3.5, GPT-4, etc.) with MLflow for experiment tracking.

## Prerequisites

1. **OpenAI API Key** - Get it from https://platform.openai.com/api-keys
2. **Python 3.8+**
3. **MLflow running** - Start with: `mlflow ui`

## Setup

### Step 1: Add Your OpenAI API Key to .env

Edit your `.env` file and add:

```
OPENAI_API_KEY=your-api-key-here
```

Or create it with:
```bash
cd ~/AI/course/mlflow
echo "OPENAI_API_KEY='your-api-key-here'" >> .env
```

Get your API key from: https://platform.openai.com/api-keys

### Step 2: Install Required Packages

```bash
# Activate your Python virtual environment first
source ~/AI/mlflow/bin/activate

# Install dependencies
pip install openai mlflow python-dotenv
```

Or use the setup script:
```bash
bash setup-openai.sh
```

## Running the Script

### Option 1: Interactive Terminal

**Terminal 1 - Start MLflow UI:**
```bash
mlflow ui
```
Access it at: http://127.0.0.1:5000

**Terminal 2 - Run the OpenAI script:**
```bash
cd ~/AI/course/mlflow
source ~/AI/mlflow/bin/activate
python3 run-openai-model.py
```

### Option 2: Run with Your Own Prompt

Modify `run-openai-model.py` and change:
- `user_message` - Your custom prompt
- `OPENAI_CONFIG["model"]` - Different model (see below)

```python
user_message = "Your custom prompt here"
```

Then run it:
```bash
python3 run-openai-model.py
```

## Available OpenAI Models

### Current Models (Recommended)

- `gpt-4o` - Latest multimodal model (best quality)
- `gpt-4-turbo` - High capability model
- `gpt-4` - Original GPT-4 (slower but capable)
- `gpt-3.5-turbo` - Fast and cost-effective (default)

### Legacy Models (Deprecated)

- `gpt-3` - Older model (not recommended)
- `text-davinci-003` - Fine-tuning only

Change the model in `run-openai-model.py`:
```python
"model": "gpt-4o",
```

## MLflow Integration Features

The script logs the following to MLflow:

### Parameters
- Model name
- System prompt
- User message
- Temperature
- Max tokens
- Attempt number (for retries)

### Metrics
- Response length
- Prompt tokens used
- Completion tokens used
- Total tokens used

### Artifacts
- Full response text (`openai_response.txt`)
- Errors (if any)

## Viewing Results in MLflow

After running the script, visit http://127.0.0.1:5000 to see:

1. **Experiments** - All OpenAI model runs
2. **Runs** - Individual experiment runs
3. **Parameters & Metrics** - Configuration and token usage
4. **Artifacts** - Saved responses

## Cost Considerations

OpenAI API usage is **pay-as-you-go**:

### Pricing (as of 2025)
- **GPT-4o**: ~$2.50-10/1M input tokens, ~$10-30/1M output tokens
- **GPT-4-turbo**: ~$10/1M input tokens, ~$30/1M output tokens
- **GPT-3.5-turbo**: ~$0.50/1M input tokens, ~$1.50/1M output tokens

### Cost Optimization
1. Use `gpt-3.5-turbo` for simple tasks
2. Use `gpt-4o` for complex reasoning
3. Monitor usage at: https://platform.openai.com/usage
4. Set billing limits to avoid surprises

### Token Counter
The script logs all token usage to MLflow. Check the "Metrics" tab to see:
- Prompt tokens (your input)
- Completion tokens (model output)
- Total cost based on pricing

## Troubleshooting

### "OPENAI_API_KEY not found"
Make sure your `.env` file has your API key:
```bash
grep OPENAI_API_KEY .env
# If not present, add it:
echo "OPENAI_API_KEY='your-key'" >> .env
```

### "Connection refused" on MLflow
Make sure MLflow UI is running:
```bash
mlflow ui
```

### "Rate limit exceeded"
OpenAI has rate limits based on your plan:
- Free trial: Lower limits
- Paid account: Higher limits

Wait a moment and retry. The script automatically retries with exponential backoff.

### "Insufficient quota"
Your account may have no remaining credits:
1. Check usage: https://platform.openai.com/usage
2. Add a payment method if needed
3. Top up your balance

### "Invalid API key"
Check your API key is correct:
```bash
cat .env | grep OPENAI_API_KEY
```

## Comparing Models

### GPT-3.5-turbo (Fast & Cheap)
- Best for: Simple questions, summarization
- Speed: Very fast
- Cost: Lowest
- Quality: Good for simple tasks

### GPT-4-turbo (Balanced)
- Best for: Complex reasoning, coding
- Speed: Moderate
- Cost: Moderate
- Quality: High

### GPT-4o (Best)
- Best for: Creative, complex reasoning, multimodal
- Speed: Moderate
- Cost: Higher
- Quality: Highest

## Integration with Other Models

You can compare OpenAI with other providers:

- **Local**: See `../M1/mlflow/run-local-model.py` (Ollama)
- **Gemini**: See `GEMINI-README.md` (Google's API)
- **Anthropic**: Create similar script using Claude API

## Next Steps

1. Modify the prompt for your use case
2. Experiment with different models and parameters
3. Compare token usage and costs in MLflow UI
4. Deploy to production using MLflow model registry

## Useful Links

- OpenAI API Documentation: https://platform.openai.com/docs/api-reference
- API Key Management: https://platform.openai.com/api-keys
- Usage & Billing: https://platform.openai.com/usage
- Model Comparison: https://platform.openai.com/docs/models
