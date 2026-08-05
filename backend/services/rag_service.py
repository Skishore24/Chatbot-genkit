from ai.rag.retriever import Retriever
from ai.rag.prompt_builder import PromptBuilder
from services.ai_service import AIService



class RAGService:

    def __init__(self):

        self.retriever = Retriever()

        self.ai = AIService()

    def ask(

        self,

        question

    ):

        chunks = self.retriever.retrieve(

            question,

            top_k=5

        )

        prompt = PromptBuilder.build(

            question,

            chunks

        )

        answer = self.ai.generate_response(

            question,

            prompt

        )

        return answer