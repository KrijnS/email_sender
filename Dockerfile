FROM python:3.9-slim

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the Python script
COPY app.py /app/app.py

# Run the script
CMD ["python3", "/app/app.py"]
