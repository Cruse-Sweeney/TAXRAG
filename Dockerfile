FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y python3.10 python3-pip git curl && apt-get clean

# Set working directory
WORKDIR /app

# Copy source code and requirements into container
COPY src /app/src
COPY src/requirements.txt /app/requirements.txt
COPY data /app/data  

# Install Python packages
RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pull your model
RUN ollama pull Llama3.3-70B-Instruct

# Run Streamlit app
WORKDIR /app/src
CMD ollama serve & streamlit run streamlit_app.py --server.port=7860 --server.address=0.0.0.0
