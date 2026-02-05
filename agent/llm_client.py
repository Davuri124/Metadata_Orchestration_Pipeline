import requests
import json
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"

MAX_RETRIES = 5
BACKOFF_SECONDS = 5

def call_explanation_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.2
        }
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                OLLAMA_URL,
                json=payload,
                stream=True,
                timeout=300
            )
            response.raise_for_status()

            output = []
            for line in response.iter_lines():
                if not line:
                    continue
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    output.append(data["response"])

            return "".join(output).strip()

        except requests.exceptions.ConnectionError:
            if attempt == MAX_RETRIES:
                break
            print(
                f"[LLM busy] retry {attempt}/{MAX_RETRIES} "
                f"in {BACKOFF_SECONDS}s"
            )
            time.sleep(BACKOFF_SECONDS)

        except requests.exceptions.RequestException as e:
            return (
                "[LLM explanation unavailable]\n\n"
                "The explanation layer could not be reached at this time. "
                "This does not affect pipeline execution or governance.\n\n"
                f"Error: {str(e)}"
            )

    return (
        "[LLM busy]\n\n"
        "The local LLM was temporarily unavailable due to resource constraints. "
        "This explanation can be regenerated later without re-running the pipeline."
    )
