FROM python:3.9-slim

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the Python script
COPY app.py /app/app.py

# Add directory to access secrets
RUN mkdir -p /run/secrets

CMD ["python3", "/app/app.py"]
