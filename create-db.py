from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

import os
data = PyPDFLoader(os.path.join(os.path.dirname(__file__), "document_loader/deeplearning.pdf"))
docs = data.load()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap= 200
)
chunks= splitter.split_documents(docs)
embedding_model =  MistralAIEmbeddings(model="mistral-embed")
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="Chroma-db"
)