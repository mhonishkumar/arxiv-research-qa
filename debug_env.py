import os
import sys

print("Current working directory:", os.getcwd())
print("Python executable:", sys.executable)
print(".env file exists at s:\\re\\.env:", os.path.exists("s:\\re\\.env"))

# Try loading .env
import dotenv
dotenv.load_dotenv("s:\\re\\.env")

print("GOOGLE_API_KEY after loading:", os.getenv("GOOGLE_API_KEY")[:20] + "..." if os.getenv("GOOGLE_API_KEY") else "NOT SET")

# Try loading from current directory too
dotenv.load_dotenv()
print("GOOGLE_API_KEY after loading from current dir:", os.getenv("GOOGLE_API_KEY")[:20] + "..." if os.getenv("GOOGLE_API_KEY") else "NOT SET")
