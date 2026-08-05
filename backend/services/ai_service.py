class AIService:

    def __init__(self):

        pass

    def generate_response(

        self,

        question: str,

        context: str

    ):

        """
        Temporary response.

        This function will later call
        our language model.
        """

        answer = f"""

Question:
{question}

Context:
{context}

Response:
This is a temporary AI response generated
using the retrieved company context.
"""

        return answer.strip()