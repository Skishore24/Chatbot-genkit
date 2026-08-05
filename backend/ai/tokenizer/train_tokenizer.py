import os
import json
from ai.tokenizer.tokenizer import SimpleTokenizer
from config import settings

def train_tokenizer_from_corpus(corpus_texts: list, save_path: str = settings.TOKENIZER_VOCAB_PATH):
    print("🔤 Training custom Subword/Word Tokenizer...")
    tokenizer = SimpleTokenizer()
    
    for text in corpus_texts:
        tokens = tokenizer.tokenize(text)
        for token in tokens:
            tokenizer._add_word(token)
            
    tokenizer.save_vocab(save_path)
    print(f"✅ Vocabulary generated ({tokenizer.vocab_size} tokens) and saved to {save_path}")
    return tokenizer

if __name__ == "__main__":
    sample_corpus = [
        "Genkit AI Chatbot is powered by custom Transformer neural networks.",
        "Retrieval Augmented Generation indexes documents using cosine similarity vector embeddings.",
        "FastAPI backend exposes user login, admin metrics, document management, and chat endpoints.",
        "React frontend provides glassmorphic theme with real-time text streaming and active session history."
    ]
    train_tokenizer_from_corpus(sample_corpus)
