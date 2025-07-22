from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
import os

def build_rag_chain(quran_text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(quran_text)

    embedder = OllamaEmbeddings(model="mistral")
    persist_directory = "chroma_db"

    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:
        print("Loading existing ChromaDB...")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedder)
    else:
        print("Creating new ChromaDB...")
        vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=embedder,
            persist_directory=persist_directory
        )
        vectorstore.persist()

    llm = Ollama(model="mistral")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    return qa_chain
