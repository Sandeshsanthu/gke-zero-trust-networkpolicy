import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # Force a 5-second delay for every single request
    time.sleep(5) 
    return "Finally finished after 5 seconds!\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
