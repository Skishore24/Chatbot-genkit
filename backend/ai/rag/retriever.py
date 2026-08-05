from ai.rag.vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.store = VectorStore()
        try:
            self.store.load("ai/index")
        except Exception:
            pass


    def embed_query(self, question):

        """
        Temporary embedding.

        Later this will be replaced by
        our real embedding model.
        """

        vector = [0.0] * 128

        words = question.lower().split()

        for word in words:

            index = hash(word) % 128

            vector[index] += 1

        return vector

    def retrieve(

        self,

        question,

        top_k=5

    ):

        query_vector = self.embed_query(

            question

        )

        results = self.store.search(

            query_vector,

            top_k

        )

        return results