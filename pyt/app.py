import time
import random
import pybreaker
from flask import Flask, Response
from tenacity import retry, stop_after_attempt, stop_after_delay, wait_exponential, retry_if_exception_type

app = Flask(__name__)

# --- MARKET STANDARD: Initialize Circuit Breaker ---
# Threshold: 3 failures trips it; Recovery: Wait 30s before trying again
db_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=30)

# --- THE BUSINESS LOGIC ---
# Order: Retry wraps the Breaker to try again before giving up
@retry(
    stop=(stop_after_attempt(3) | stop_after_delay(5)), # RETRY: 3 tries OR 5s total
    wait=wait_exponential(multiplier=1, min=1, max=4),   # BACKOFF: 1s, 2s, 4s
    retry=retry_if_exception_type(Exception),
    reraise=True # Important: let the final error bubble up to the API
)
@db_breaker # CIRCUIT BREAKER: Monitor these attempts
def call_downstream_service():
    # Simulate a "Slow Response" (This triggers the 5s stop_after_delay above)
    # time.sleep(6) 

    # Simulate a 50% chance of a "Transient Blip"
    if random.random() < 0.5:
        print("--- Log: Transient failure! ---")
        raise Exception("Database Blip")
    
    return "Data from Database"

# --- THE API ENDPOINT ---
@app.route('/')
def index():
    try:
        result = call_downstream_service()
        return f"SUCCESS: {result}\n"
    
    except pybreaker.CircuitBreakerError:
        return Response("CIRCUIT OPEN: Stopping traffic to save DB\n", status=503)
    
    except Exception as e:
        return Response(f"FAILED after retries: {str(e)}\n", status=500)

if __name__ == "__main__":
    # Gunicorn handles the production serving, this is for local/dev
    app.run(host='0.0.0.0', port=8080)
