class PromptBuilder:

    @staticmethod
    def build(question, retrieved_chunks):

        context = "\n\n".join(
            [chunk for _, chunk in retrieved_chunks]
        )

        prompt = f"""
You are GenKit AI Assistant.

Answer ONLY using the information provided below.

=========================
CONTEXT
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
ANSWER
=========================
"""

        return prompt.strip()