import os
import streamlit as st 
import dotenv # type: ignore
import arxiv
import google.generativeai as genai
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

from langchain_text_splitters import RecursiveCharacterTextSplitter # type: ignore
from langchain_community.vectorstores import FAISS # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document

# Load environment variables from .env file
# Use explicit path to ensure .env is found even when Streamlit runs from a different directory
env_path = os.path.join(os.path.dirname(__file__), ".env")
dotenv.load_dotenv(env_path, override=True)

# Explicitly set the API key for Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# Configure Google Generative AI
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    # Will show error message in the sidebar below
    GOOGLE_API_KEY = None

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="arXiv Research Paper Q&A",
    page_icon="📚",
    layout="wide"
)

st.title("📚 arXiv Research Paper Q&A Bot")
st.write("Ask questions about an arXiv research paper using RAG + Gemini.")

# --------------------------------------------------
# API KEY VALIDATION
# --------------------------------------------------

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY is missing from the .env file.")
    st.info("""
    To use this app, you need a Google API key:
    1. Go to https://makersuite.google.com/app/apikey
    2. Create a new API key
    3. Copy it and paste it into the .env file:
       GOOGLE_API_KEY=your_api_key_here
    4. Save and refresh the app
    """)
    st.stop()

# Debug: Show that API key is loaded (without showing the full key)
api_key_preview = GOOGLE_API_KEY[:20] + "..." if GOOGLE_API_KEY else "❌ Not loaded"
st.sidebar.caption(f"✅ API Key loaded: {api_key_preview}")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("⚙️ Settings")

    paper_id = st.text_input(
        "Enter arXiv Paper ID",
        placeholder="e.g. 1706.03762"
    )

    load_paper = st.button(
        "📥 Load Paper",
        use_container_width=True
    )

# --------------------------------------------------
# LOAD PAPER
# --------------------------------------------------

if load_paper:

    if not paper_id:
        st.warning("Please enter an arXiv paper ID.")
        st.stop()

    with st.spinner("Downloading research paper..."):

        try:
            # Load paper from arXiv using arxiv library
            client = arxiv.Client()
            paper = next(client.results(arxiv.Search(query=paper_id, max_results=1)))
            
            # Get paper details
            paper_title = paper.title
            paper_summary = paper.summary
            
            # Create a document from the paper
            document = Document(
                page_content=f"Title: {paper_title}\n\nSummary: {paper_summary}",
                metadata={"source": paper.entry_id}
            )
            documents = [document]

            if not documents:
                st.error("Paper not found.")
                st.stop()

            # --------------------------------------------------
            # SPLIT DOCUMENT
            # --------------------------------------------------

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=150
            )

            chunks = text_splitter.split_documents(documents)

            # --------------------------------------------------
            # EMBEDDINGS WITH GOOGLE GENERATIVE AI
            # --------------------------------------------------

            # Get embeddings for all chunks
            chunk_texts = [chunk.page_content for chunk in chunks]
            chunk_embeddings = []
            
            with st.spinner("Creating embeddings..."):
                for text in chunk_texts:
                    try:
                        response = genai.embed_content(
                            model='models/gemini-embedding-001',
                            content=text
                        )
                        chunk_embeddings.append(response['embedding'])
                    except Exception as e:
                        st.error(f"Error creating embedding: {e}")
                        st.stop()

            # --------------------------------------------------
            # VECTOR DATABASE
            # --------------------------------------------------

            # Create a fake embeddings object for FAISS compatibility
            from langchain_core.embeddings import Embeddings
            
            class FakeEmbeddings(Embeddings):
                def embed_documents(self, texts):
                    return chunk_embeddings[:len(texts)]
                
                def embed_query(self, text):
                    return chunk_embeddings[0] if chunk_embeddings else [0] * 3072
            
            embeddings = FakeEmbeddings()
            
            # Create FAISS vector store manually
            import faiss
            import numpy as np
            
            embeddings_array = np.array(chunk_embeddings, dtype=np.float32)
            index = faiss.IndexFlatL2(embeddings_array.shape[1])
            index.add(embeddings_array)
            
            # Store in Streamlit session
            st.session_state.faiss_index = index
            st.session_state.chunks = chunks
            st.session_state.chunk_embeddings = chunk_embeddings
            st.session_state.paper = documents[0]

            st.success(
                f"Paper loaded successfully! "
                f"Created {len(chunks)} text chunks."
            )

        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg:
                st.error("❌ Invalid Google API Key")
                st.warning("""
                The API key in your .env file is invalid or expired.
                
                Please get a new one:
                1. Go to https://makersuite.google.com/app/apikey
                2. Create a new API key
                3. Update the GOOGLE_API_KEY in your .env file
                4. Refresh the app
                """)
            else:
                st.error(f"Error loading paper: {e}")

# --------------------------------------------------
# Q&A
# --------------------------------------------------

if "faiss_index" in st.session_state:

    st.subheader("🔎 Ask a Question")

    question = st.text_input(
        "Your question",
        placeholder="What is the main contribution of this paper?"
    )

    ask = st.button("🤖 Ask Gemini")

    if ask:

        if not question:
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner("Searching the paper..."):
            
            # --------------------------------------------------
            # RETRIEVAL
            # --------------------------------------------------
            
            # Embed the question
            question_embedding = genai.embed_content(
                model='models/gemini-embedding-001',
                content=question
            )['embedding']
            
            # Search FAISS index
            import numpy as np
            query_embedding = np.array([question_embedding], dtype=np.float32)
            distances, indices = st.session_state.faiss_index.search(query_embedding, k=4)
            
            # Get relevant documents
            relevant_docs = [st.session_state.chunks[i] for i in indices[0]]
            
            context = "\n\n".join(
                doc.page_content
                for doc in relevant_docs
            )

            # --------------------------------------------------
            # GEMINI
            # --------------------------------------------------

            llm = genai.GenerativeModel(
                model_name="gemini-3.6-flash"
            )

            prompt = f"""
You are a research paper assistant.

Answer the user's question ONLY using the
provided research paper context.

If the answer cannot be found in the context,
say:

"I could not find the answer in the paper."

Do not invent information.

Research Paper Context:
-----------------------
{context}
-----------------------

Question:
{question}

Give a clear and concise answer.
"""

            response = llm.generate_content(prompt)

            # --------------------------------------------------
            # DISPLAY ANSWER
            # --------------------------------------------------

            st.subheader("💡 Answer")

            st.write(response.text)

            # --------------------------------------------------
            # SOURCES
            # --------------------------------------------------

            with st.expander("📖 Retrieved Sources"):

                for i, doc in enumerate(relevant_docs):

                    st.markdown(
                        f"**Source {i + 1}**"
                    )

                    st.write(
                        doc.page_content[:1000]
                    )

                    st.divider()

else:

    st.info(
        "👈 Enter an arXiv paper ID and click "
        "**Load Paper** to begin."
    )