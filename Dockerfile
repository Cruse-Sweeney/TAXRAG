FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3.10 python3-pip git curl && apt-get clean

WORKDIR /app

COPY src /app/src
COPY src/requirements.txt /app/requirements.txt
COPY data /app/data

RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt

# Install Ollama (but don't pull model during build)
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app/src

EXPOSE 7860

RUN mkdir -p /workspace/data/business_docs /workspace/data/irs_docs


# ✅ Pull the model & run everything at container start
CMD bash -c "ollama serve & sleep 3 && ollama pull llama3:70b-instruct && streamlit run streamlit_app.py --server.port=7860 --server.address=0.0.0.0"
