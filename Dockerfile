# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the server
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code
COPY . .

# Tell Google to open port 8080 (the default for Cloud Run)
EXPOSE 8080

# The command to launch your Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
