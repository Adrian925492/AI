import mlflow
import google.genai as genai
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Google Gemini Configuration ---
# Load API key from .env file
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file. "
        "Add it to .env with: GOOGLE_API_KEY='your-api-key-here'"
    )

GEMINI_CONFIG = {
    "engine": "gemini",
    "model": "gemini-2.0-flash-lite",  # Lightweight model with better free tier quotas
    "api_key": GEMINI_API_KEY,
    "max_retries": 3,
    "retry_delay": 5,  # seconds
}

# Configure the Gemini client
client = genai.Client(api_key=GEMINI_CONFIG["api_key"])

# --- MLflow Configuration ---
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("DJ_gemini_model_tracking")

# --- Perform Inference and Tracking ---
with mlflow.start_run() as run:
    print(f"Tracking started in MLflow Run ID: {run.info.run_id}")
    print(f"Using model: {GEMINI_CONFIG['model']}")
    print("-" * 50)

    # Model call with retry logic
    model_response = None
    last_error = None
    
    for attempt in range(GEMINI_CONFIG["max_retries"]):
        try:
            # Create the prompt
            system_prompt = "You are a helpful AI assistant."
            user_message = "Write a short note on why it is worth using MLflow."

            # Call Gemini API using the new google.genai package
            response = client.models.generate_content(
                model=GEMINI_CONFIG["model"],
                contents=user_message,
            )

            # Log the response
            model_response = response.text
            print("\n--- Model Response ---")
            print(model_response)
            print("\n" + "-" * 50)

            # Log to MLflow
            mlflow.log_param("model", GEMINI_CONFIG["model"])
            mlflow.log_param("system_prompt", system_prompt)
            mlflow.log_param("user_message", user_message)
            mlflow.log_param("attempt", attempt + 1)
            mlflow.log_metric("response_length", len(model_response))
            mlflow.log_text(model_response, "gemini_response.txt")

            print(f"\n✅ Success! Response logged to MLflow")
            break

        except Exception as e:
            last_error = str(e)
            error_message = f"Attempt {attempt + 1}/{GEMINI_CONFIG['max_retries']}: {str(e)}"
            print(f"\n❌ {error_message}")
            
            # Check if it's a quota error
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < GEMINI_CONFIG["max_retries"] - 1:
                    wait_time = GEMINI_CONFIG["retry_delay"] * (attempt + 1)
                    print(f"⏳ Quota exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("\n⚠️  Free tier quota exceeded. Options:")
                    print("   1. Wait for quota reset (usually daily)")
                    print("   2. Upgrade to paid plan: https://ai.google.dev/pricing")
                    print("   3. Check usage: https://ai.dev/usage")
                    mlflow.log_text(f"Quota exceeded after {attempt + 1} attempts", "quota_error.txt")
            else:
                # Other errors - don't retry
                mlflow.log_text(error_message, "error.txt")
                raise

    if not model_response and last_error:
        raise Exception(f"Failed after {GEMINI_CONFIG['max_retries']} attempts: {last_error}")

    print(f"🏃 View run at: http://127.0.0.1:5000/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}")
    print(f"🧪 View experiment at: http://127.0.0.1:5000/#/experiments/{run.info.experiment_id}")
