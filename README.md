This is a local test instance of using RAG for tax related questions

features
- Local LLM using Ollama + Mistral
- Embedding via HuggingFace
- RAG pipeline using LlamaIndex + ChromaDB
- Document upload via Streamlit
- IRS and business doc Q&A
- Local-only, no OpenAI API required

tech stack

- Python
- Streamlit
- LlamaIndex
- Ollama
- HuggingFace
- ChromaDB


```bash
git clone https://github.com/YOUR_USERNAME/tax-ai-assistant.git
cd tax-ai-assistant
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
streamlit run src/streamlit_app.py