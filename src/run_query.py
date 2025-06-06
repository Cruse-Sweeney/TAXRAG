from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

# ✅ Set local embedding model globally
embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
Settings.embed_model = embed_model

# Load IRS documents
docs = SimpleDirectoryReader(input_dir="data/irs_docs").load_data()
print(f"Loaded {len(docs)} documents")

# Build index
index = VectorStoreIndex.from_documents(docs)

# Query engine using local Mistral via Ollama
llm = Ollama(model="mistral")
query_engine = index.as_query_engine(llm=llm)

# Ask a test question
query = "I have a small business what can I deduct from my taxes?"
response = query_engine.query(query)

print("\n--- Result ---\n")
print(response.response)
