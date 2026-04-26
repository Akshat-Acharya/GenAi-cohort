from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from langchain_qdrant import QdrantVectorStore


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")


print(api_key)

pdf_path = Path(__file__).parent / "nodejs_test.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
)

split_docs = text_splitter.split_documents(documents=docs)

embedder = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
# Vector storing done 
# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embedder
# )



# vector_store.add_documents(documents=split_docs)

print("Injection Done")

#retriever 
retriver  =  QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder
)

relevant_chunks = retriver.similarity_search(
    query="What is FS Module?"
)

SYSTEM_PROMPT =f'''
You are an helpfull AI Assistant who responds base of the available context.

Context:
{relevant_chunks}
'''