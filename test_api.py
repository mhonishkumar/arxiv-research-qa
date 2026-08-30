import google.generativeai as genai
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

try:
    genai.configure(api_key='AQ.Ab8RN6Ju3NUDVjAcLF5smZDr1ZtB55PIJJ2gBrdHlel8t7E2ew')
    
    # Try with correct model name
    print("Testing with models/gemini-embedding-001...")
    result = genai.embed_content(
        model='models/gemini-embedding-001',
        content='This is a test message'
    )
    print('✅ Embeddings API works!')
    print('Embedding dimension:', len(result['embedding']))
except Exception as e:
    print('❌ Error:', str(e))
