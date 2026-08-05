import json
from ai.rag.parser import DocumentParser
from ai.rag.chunker import TextChunker
from ai.rag.vector_store import VectorStore


class IndexingService:

    def __init__(self):
        self.chunker = TextChunker()
        self.store = VectorStore()
        try:
            self.store.load("ai/index")
        except Exception:
            pass

    def fake_embedding(self, text):
        words = text.lower().split()
        vector = [0.0] * 128
        for word in words:
            index = hash(word) % 128
            vector[index] += 1.0
        return vector

    def index_text(self, text):
        chunks = self.chunker.chunk(text)
        for chunk in chunks:
            embedding = self.fake_embedding(chunk)
            self.store.add_document(chunk, embedding)
        self.store.save("ai/index")
        return len(chunks)

    def index_document(self, file_path):
        text = DocumentParser.parse(file_path)
        return self.index_text(text)

    def index_json_dataset(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        total_chunks = 0
        for item in data:
            title = item.get("title", "")
            category = item.get("category", "")
            content = item.get("content", "")
            combined_text = f"[{category}] {title}: {content}"
            total_chunks += self.index_text(combined_text)

        return total_chunks

