import mlflow
import openai
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- OpenAI Configuration ---
# Load API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found in .env file. "
        "Add it to .env with: OPENAI_API_KEY='your-api-key-here'"
    )

OPENAI_CONFIG = {
    "engine": "openai",
    "model": "gpt-3.5-turbo",  # Or use "gpt-4", "gpt-4-turbo", etc.
    "api_key": OPENAI_API_KEY,
    "max_retries": 3,
    "retry_delay": 2,  # seconds
}

# Configure the OpenAI client
client = openai.OpenAI(api_key=OPENAI_CONFIG["api_key"])

# --- MLflow Configuration ---
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("DJ_openai_model_tracking")

# --- Perform Inference and Tracking ---
with mlflow.start_run() as run:
    print(f"Tracking started in MLflow Run ID: {run.info.run_id}")
    print(f"Using model: {OPENAI_CONFIG['model']}")
    print("-" * 50)

    # Model call with retry logic
    model_response = None
    last_error = None
    
    for attempt in range(OPENAI_CONFIG["max_retries"]):
        try:
            # Create the prompt
            system_prompt = "You are a helpful AI assistant."
            user_message = "Write a short note on why it is worth using MLflow."

            # Call OpenAI API
            response = client.chat.completions.create(
                model=OPENAI_CONFIG["model"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=150,
            )

            # Extract the response
            model_response = response.choices[0].message.content
            print("\n--- Model Response ---")
            print(model_response)
            print("\n" + "-" * 50)

            # Log to MLflow
            mlflow.log_param("model", OPENAI_CONFIG["model"])
            mlflow.log_param("system_prompt", system_prompt)
            mlflow.log_param("user_message", user_message)
            mlflow.log_param("temperature", 0.7)
            mlflow.log_param("max_tokens", 150)
            mlflow.log_param("attempt", attempt + 1)
            mlflow.log_metric("response_length", len(model_response))
            mlflow.log_metric("prompt_tokens", response.usage.prompt_tokens)
            mlflow.log_metric("completion_tokens", response.usage.completion_tokens)
            mlflow.log_metric("total_tokens", response.usage.total_tokens)
            mlflow.log_text(model_response, "openai_response.txt")

            print(f"\n✅ Success! Response logged to MLflow")
            print(f"📊 Tokens used - Prompt: {response.usage.prompt_tokens}, Completion: {response.usage.completion_tokens}, Total: {response.usage.total_tokens}")
            break

        except openai.RateLimitError as e:
            last_error = str(e)
            error_message = f"Attempt {attempt + 1}/{OPENAI_CONFIG['max_retries']}: Rate limit - {str(e)}"
            print(f"\n❌ {error_message}")
            
            if attempt < OPENAI_CONFIG["max_retries"] - 1:
                wait_time = OPENAI_CONFIG["retry_delay"] * (attempt + 1)
                print(f"⏳ Rate limited. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("\n⚠️  Rate limit exceeded after retries.")
                mlflow.log_text(f"Rate limit exceeded after {attempt + 1} attempts", "rate_limit_error.txt")

        except openai.APIConnectionError as e:
            last_error = str(e)
            error_message = f"Attempt {attempt + 1}/{OPENAI_CONFIG['max_retries']}: Connection error - {str(e)}"
            print(f"\n❌ {error_message}")
            
            if attempt < OPENAI_CONFIG["max_retries"] - 1:
                wait_time = OPENAI_CONFIG["retry_delay"] * (attempt + 1)
                print(f"⏳ Connection error. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                mlflow.log_text(error_message, "connection_error.txt")

        except Exception as e:
            last_error = str(e)
            error_message = f"Error: {str(e)}"
            print(f"\n❌ {error_message}")
            mlflow.log_text(error_message, "error.txt")
            raise

    if not model_response and last_error:
        raise Exception(f"Failed after {OPENAI_CONFIG['max_retries']} attempts: {last_error}")

    print(f"🏃 View run at: http://127.0.0.1:5000/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}")
    print(f"🧪 View experiment at: http://127.0.0.1:5000/#/experiments/{run.info.experiment_id}")
