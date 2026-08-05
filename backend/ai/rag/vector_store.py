import json
import math
from pathlib import Path


class VectorStore:

    def __init__(self):

        self.documents = []

        self.embeddings = []

    def add_document(self, text, embedding):

        self.documents.append(text)

        self.embeddings.append(embedding)

    def cosine_similarity(self, vec1, vec2):

        dot = sum(a * b for a, b in zip(vec1, vec2))

        norm1 = math.sqrt(sum(a * a for a in vec1))

        norm2 = math.sqrt(sum(a * a for a in vec2))

        if norm1 == 0 or norm2 == 0:

            return 0.0

        return dot / (norm1 * norm2)

    def search(self, query_embedding, top_k=5):

        scores = []

        for i, embedding in enumerate(self.embeddings):

            score = self.cosine_similarity(

                query_embedding,

                embedding

            )

            scores.append(

                (

                    score,

                    self.documents[i]

                )

            )

        scores.sort(

            reverse=True,

            key=lambda x: x[0]

        )

        return scores[:top_k]

    def save(self, folder):

        folder = Path(folder)

        folder.mkdir(

            parents=True,

            exist_ok=True

        )

        data = []

        for doc, emb in zip(

            self.documents,

            self.embeddings

        ):

            data.append(

                {

                    "text": doc,

                    "embedding": emb

                }

            )

        with open(

            folder / "vector_store.json",

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4

            )

    def load(self, folder):

        with open(

            Path(folder) / "vector_store.json",

            "r",

            encoding="utf-8"

        ) as f:

            data = json.load(f)

        self.documents = []

        self.embeddings = []

        for item in data:

            self.documents.append(

                item["text"]

            )

            self.embeddings.append(

                item["embedding"]

            )

    def __len__(self):

        return len(self.documents)