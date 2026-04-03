# 📄 RAG-APP

A Retrieval-Augmented Generation (RAG) application that lets you upload any PDF and chat with it using AI — powered by Mistral AI and LangChain.

---

## 🚀 Features

- 📁 Upload any PDF file (up to 25MB)
- 💬 Ask questions about your PDF in natural language
- 🧠 Powered by Mistral AI (Embeddings + LLM)
- 🔍 MMR-based smart retrieval for diverse, relevant context
- ⚡ FastAPI backend with clean chat UI
- 🗄️ ChromaDB vector store for efficient document search

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python |
| LLM | Mistral AI (mistral-small) |
| Embeddings | Mistral AI (mistral-embed) |
| Vector Store | ChromaDB |
| RAG Framework | LangChain |
| Frontend | HTML, CSS, JavaScript |

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/abhaydv77/RAG-APP.git
cd RAG-APP

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Setup

Create a `.env` file in the root directory:

```
MISTRAL_API_KEY=your_mistral_api_key_here
```

---

## ▶️ Run Locally

```bash
uvicorn app:app --reload
```

Then open your browser at `http://localhost:8000`

---

## 💡 How It Works

```
User uploads PDF
      ↓
PDF is split into chunks
      ↓
Chunks are converted to embeddings (Mistral)
      ↓
Embeddings stored in ChromaDB
      ↓
User asks a question
      ↓
MMR retrieval fetches relevant chunks
      ↓
Mistral LLM generates answer based on context
```

---

## 🔮 Future Upgrades

- [ ] 🚀 **Deployment** — Hosting on Railway (coming soon)
- [ ] 🔐 **User Authentication** — Login/signup so each user has their own session
- [ ] 📂 **Multi-PDF Support** — Upload and chat with multiple PDFs at once
- [ ] 🗂️ **Chat History** — Save and revisit previous conversations
- [ ] 🌐 **User API Key Input** — Let users bring their own Mistral API key
- [ ] 📊 **Source Citations** — Show which part of the PDF the answer came from
- [ ] 🎨 **React Frontend** — Upgrade UI to a full React application

---

## 👨‍💻 Author

**Abhay** — 17 y/o developer 
---
## 📸 Screenshot
<img width="1440" height="900" alt="Screenshot 2026-04-03 at 2 22 40 PM" src="https://github.com/user-attachments/assets/ba17b832-595c-42d5-ac0d-b503d28ce2a5" />
<img width="1440" height="900" alt="Screenshot 2026-04-03 at 2 24 06 PM" src="https://github.com/user-attachments/assets/4eb579e1-f203-471c-8159-5f33f077ac38" />


## 📝 License

MIT License — feel free to use and modify!
