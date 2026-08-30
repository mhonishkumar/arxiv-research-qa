# 📚 arXiv Research Paper Q&A Bot

An AI-powered Research Paper Question & Answer chatbot that allows users to load research papers from **arXiv** and ask questions about their content.

Built using **Python, Streamlit, LangChain, Google Gemini, and FAISS**.

## 🚀 Features

- 📄 Load research papers directly from arXiv
- 🤖 Ask questions about the research paper
- 🔍 Semantic search using vector embeddings
- 🧠 Google Gemini for AI-powered answers
- 📚 Retrieval-Augmented Generation (RAG)
- ⚡ Fast similarity search using FAISS
- 🖥️ Simple and interactive Streamlit interface
- 🚫 Reduces hallucination by answering based on retrieved paper content

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Google Gemini
- Google Generative AI Embeddings
- FAISS
- arXiv
- python-dotenv

## 🏗️ Architecture

```text
                    arXiv Research Paper
                             │
                             ▼
                       ArxivLoader
                             │
                             ▼
                      Extract Text
                             │
                             ▼
                       Text Splitter
                             │
                             ▼
                    Text Chunks
                             │
                             ▼
                  Gemini Embeddings
                             │
                             ▼
                           FAISS
                       Vector Store
                             │
                             ▼
                     User Question
                             │
                             ▼
                    Similarity Search
                             │
                             ▼
                   Relevant Paper Chunks
                             │
                             ▼
                     Google Gemini
                             │
                             ▼
                       AI Answer
📂 Project Structure
arxiv-research-qa/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/arxiv-research-qa.git
cd arxiv-research-qa
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment
Windows PowerShell
.\.venv\Scripts\Activate.ps1
Windows CMD
.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
🔑 API Key Setup

Create a .env file in the project directory:

GOOGLE_API_KEY=your_google_api_key

Never commit your .env file to GitHub.

The .gitignore file should contain:

.venv/
venv/
__pycache__/
.env
*.pyc
▶️ Run the Application
streamlit run app.py

The application will open in your browser.

Usually:

http://localhost:8501
📖 How to Use
Enter an arXiv Paper ID.
Click Load Paper.
Wait for the paper to be processed.
Enter your question.
Click Ask Gemini.
The system retrieves relevant sections from the paper and generates an answer.
Example

Use this arXiv paper:

1706.03762

Then ask:

What is the main contribution of this paper?

Other example questions:

Explain the Transformer architecture.

Why does the paper use self-attention?

What are the advantages of the proposed approach?

What problem does this research solve?
🧠 RAG Workflow

This project uses Retrieval-Augmented Generation (RAG).

The workflow is:

Research Paper
      ↓
Document Loading
      ↓
Text Splitting
      ↓
Embeddings
      ↓
FAISS Vector Database
      ↓
Question
      ↓
Relevant Chunks Retrieved
      ↓
Google Gemini
      ↓
Answer

Instead of asking the LLM to answer solely from its pretrained knowledge, the application retrieves relevant information from the research paper and provides it as context to Gemini.

🔮 Future Improvements
💬 Chat history and multi-turn conversations
📄 Upload research paper PDFs
📚 Ask questions across multiple papers
🔗 Support arXiv URLs
📝 Automatic paper summarization
📊 Research paper comparison
📑 Page-level source citations
🎯 Beginner-friendly explanation mode
🌐 Deploy the application online
👨‍💻 Author

Mhonish Kumar J

BE Computer Science Engineering

Interested in:

Python
SQL
Data Analytics
Power BI
Artificial Intelligence
Generative AI
⭐ If you find this project useful

Give the repository a ⭐ on GitHub!
