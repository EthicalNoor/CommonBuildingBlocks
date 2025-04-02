# CommonBuildingBlocks/core_sys_config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SystemConfiguration:
    """SystemConfiguration class handles all environment-based settings."""
    
    # ============================
    # Cloud (AWS) Configuration
    # ============================
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    AWS_REGION = os.getenv('AWS_REGION', "eu-west-2")
    
    # ============================
    # API Keys and Endpoints
    # ============================
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
    
    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Google
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Deepgram
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    
    # ElevenLabs
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
    
    # GROQ (Generalized Retrieval of Query) configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    
    # AssemblyAI
    ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
    ASSEMBLYAI_UPLOAD_URL = os.getenv("ASSEMBLYAI_UPLOAD_URL", "https://api.assemblyai.com/v2/upload")
    ASSEMBLYAI_TRANSCRIPT_URL = os.getenv("ASSEMBLYAI_TRANSCRIPT_URL", "https://api.assemblyai.com/v2/transcript")
    
    # ============================
    # External Service Endpoints
    # ============================
    FASTAPI_URL = os.getenv("FASTAPI_URL", "https://a208-34-75-176-82.ngrok-free.app/speak")
    
    # ============================
    # PostgreSQL Database Configuration
    # ============================
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', "innovation_db")
    DB_USER = os.getenv('DB_USER', "admin")
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    TABLE_SCHEMA = """Create Schema Query Here"""
    
    # ============================
    # Language and Localization Settings
    # ============================
    DEFAULT_LANG = os.getenv("DEFAULT_LANG", "en")
    USE_DEFAULT_LANG = os.getenv("USE_DEFAULT_LANG", "false").lower() == 'true'