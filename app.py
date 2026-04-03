import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from dotenv import load_dotenv
from httpcore import request
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

embedding_model = MistralAIEmbeddings(model="mistral-embed")
llm = ChatMistralAI(model="mistral-small-2506", api_key=os.getenv("MISTRAL_API_KEY"))

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
     You are a helpful assistant for answering questions based on the provided context.
     If you don't know the answer, say you don't know."""),
    ("human", """context:
        {context}
        Question: {question}
    """)
])

retriever = None

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
      return templates.TemplateResponse(request=request, name="index.html")


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global retriever

    # sirf PDF allow
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Sirf PDF file allowed hai!")

    # file size check
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File 25MB se badi nahi honi chahiye!")

    # save karo
    file_path = f"document_loader/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)

    # process karo
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="Chroma-db"
    )

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5}
    )

    return {"message": f"PDF upload ho gaya! Ab question pooch sakte ho."}


@app.post("/ask")
async def ask_question(data: dict):
    global retriever

    if retriever is None:
        raise HTTPException(status_code=400, detail="Pehle PDF upload karo!")

    query = data.get("question")
    if not query:
        raise HTTPException(status_code=400, detail="Question khaali nahi hona chahiye!")

    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt_template.invoke({
        "context": context,
        "question": query
    })

    response = llm.invoke(final_prompt)

    return {"answer": response.content}