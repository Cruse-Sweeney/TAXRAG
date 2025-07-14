import os
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="TaxRag", page_icon="🯞", layout="wide")

# -------------------------------
# EMBEDDING MODEL SETUP
# -------------------------------
embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
Settings.embed_model = embed_model

# -------------------------------
# CSS STYLING
# -------------------------------
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            font-size: 16px;
        }
        .stChatMessage {
            font-size: 16px;
        }
        h1 {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# DIRECTORIES
# -------------------------------
biz_doc_dir = "/workspace/data/business_docs"
irs_doc_dir = "/workspace/data/irs_docs"
os.makedirs(biz_doc_dir, exist_ok=True)
os.makedirs(irs_doc_dir, exist_ok=True)

# -------------------------------
# INDEXING FUNCTION
# -------------------------------
@st.cache_resource
def load_index():
    irs_docs = SimpleDirectoryReader(irs_doc_dir).load_data()
    biz_docs = SimpleDirectoryReader(biz_doc_dir).load_data()
    return VectorStoreIndex.from_documents(irs_docs + biz_docs)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("# TaxRag")

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# TABS: Chat is first
# -------------------------------
tab_chat, tab_upload = st.tabs(["💬 Ask a Tax Question", "📄 Upload Documents"])

# -------------------------------
# CHAT TAB
# -------------------------------
with tab_chat:
    st.markdown("""
        <style>
        .stChatInputContainer {
            position: fixed !important;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            padding: 1rem;
            border-top: 1px solid #eee;
            z-index: 9999;
        }
        .chat-container {
            padding-bottom: 120px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Type your question here..."):
        st.chat_message("user").write(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Searching IRS guidelines and your documents..."):
                index = load_index()
                llm = Ollama(model="llama3:70b-instruct", base_url="http://localhost:11434")
                engine = index.as_query_engine(
                    llm=llm,
                    system_prompt=(
                        "You are a friendly, accurate tax advisor for small businesses. Use IRS rules and uploaded business documents only."
                    )
                )
                response = engine.query(prompt)
                st.markdown(response.response)
                st.session_state.chat_history.append({"role": "assistant", "content": response.response})

# -------------------------------
# UPLOAD TAB
# -------------------------------
with tab_upload:
    st.header("📥 Upload Your Documents")

    st.subheader("📄 Business PDFs")
    biz_files = st.file_uploader("Upload business documents", type=["pdf"], accept_multiple_files=True, key="biz_uploader")

    if biz_files:
        for file in biz_files:
            save_path = os.path.join(biz_doc_dir, file.name)
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
            st.success(f"Saved business doc: {file.name}")

    st.subheader("📘 IRS Reference PDFs")
    irs_files = st.file_uploader("Upload IRS documents", type=["pdf"], accept_multiple_files=True, key="irs_uploader")

    if irs_files:
        for file in irs_files:
            save_path = os.path.join(irs_doc_dir, file.name)
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
            st.success(f"Saved IRS doc: {file.name}")

    st.info("Uploaded documents are stored persistently and will be used in your queries.")
