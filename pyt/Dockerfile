FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
# Ensure gunicorn is installed explicitly if not in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
# Change "app:app" to "[your_filename]:[your_flask_variable_name]"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
