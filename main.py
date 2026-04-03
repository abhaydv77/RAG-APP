import os
from dotenv import load_dotenv
from langchain_community import retrievers
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
import langchain_mistralai

load_dotenv()

embedding_model = MistralAIEmbeddings(model="mistral-embed")

vector_store = Chroma(
    embedding_function=embedding_model,
    persist_directory="Chroma"
)

retriever =  vector_store.as_retriever(
    search_type="mmr",
    search_kwargs= {
        "k":4,
        "fetch_k": 10,
        "lambda_mult": 0.5

    }
)


llm = langchain_mistralai.ChatMistralAI(model="mistral-small-2506", api_key=os.getenv("MISTRAL_API_KEY"))


# prompt template
prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system",
         """ 
         You are a helpful assistant for answering questions based on the provided context
         if you don't know the answer, say you don't know"""),
        ("human",
          """context:
            {context}
            Question: {question}
         """)

    ]

)

print("rag system created successfully! ")

print("press 0 to exit")

while True:
    query = input("Enter your question: ")
    if query =="0":
        print("Exiting the RAG system. Goodbye! ")
        break

    docs = retriever.invoke(query)
    context = "\n\n".join(
        [doc.page_content for doc in docs]

    )

    final_prompt= prompt_template.invoke(
        {
            "context": context,
            "question": query
        })
    response = llm.invoke(final_prompt)

    print(f"\n AI:{response.content}\n")



    
