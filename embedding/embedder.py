import numpy as np
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GEMINI_API_KEY

# Google Gemini Embedding dimensions is 768 (MiniLM was 384)
_model = None

def _get_model():
    global _model
    if _model is None:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        _model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GEMINI_API_KEY
        )
    return _model

def get_embeddings(texts: list[str]) -> np.ndarray:
    """
    Generate embeddings using Google Gemini API.
    Returns: numpy array of shape (len(texts), 768), dtype float32.
    """
    model = _get_model()
    # Langchain's embed_documents returns a list of lists
    embeddings = model.embed_documents(texts)
    return np.array(embeddings, dtype=np.float32)

def get_single_embedding(text: str) -> np.ndarray:
    """
    Generate single embedding using Google Gemini API.
    """
    model = _get_model()
    embedding = model.embed_query(text)
    return np.array([embedding], dtype=np.float32)
