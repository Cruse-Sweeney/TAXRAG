import os
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings

# Set local embedding model
embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
Settings.embed_model = embed_model

# Ensure folders exist
os.makedirs("data/business_docs", exist_ok=True)

# Upload business docs
st.sidebar.title("📥 Upload Business Documents")
uploaded_files = st.sidebar.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

for file in uploaded_files:
    save_path = os.path.join("data/business_docs", file.name)
    with open(save_path, "wb") as f:
        f.write(file.getbuffer())
    st.sidebar.success(f"Saved: {file.name}")

# Load all docs (IRS + business)
@st.cache_resource
def load_index():
    irs_docs = SimpleDirectoryReader("data/irs_docs").load_data()
    biz_docs = SimpleDirectoryReader("data/business_docs").load_data()
    return VectorStoreIndex.from_documents(irs_docs + biz_docs)

# Chat UI
st.title("🧾 Tax AI Assistant")
query = st.text_input("Ask a tax question...")

if query:
    with st.spinner("Thinking..."):
        index = load_index()
        llm = Ollama(model="mistral")
        engine = index.as_query_engine(
            llm=llm,
            system_prompt=(
                "You are a friendly, accurate tax advisor for small businesses. Use IRS rules and uploaded business documents only."
            )
        )
        response = engine.query(query)
        st.markdown("### 💬 Answer")
        st.write(response.response)

        # Virutal env activation command
# .\taxai-env\Scripts\Activate.ps1

