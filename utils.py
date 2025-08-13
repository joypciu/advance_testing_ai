import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai import types

def setup_logging():
    # Load environment variables
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    
    # Configure logging based on .env settings
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', 'app.log')
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def get_gemini_api():
    """Get Gemini API key from environment variables"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    return api_key

def get_gemini_client():
    """Initialize and return a Gemini client instance"""
    api_key = get_gemini_api()
    return genai.Client(api_key=api_key)



def get_ai_model():
    """Get the configured AI model name from .env"""
    return os.getenv('AI_MODEL', 'gemma-3n-e2b-it')
