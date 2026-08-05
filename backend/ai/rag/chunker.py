import re
from typing import List


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 300,
        overlap: int = 50
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def clean_text(self, text: str) -> str:

        text = text.replace("\r", " ")

        text = re.sub(r"\n+", "\n", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def split_into_sentences(self, text: str):

        sentences = re.split(

            r'(?<=[.!?])\s+',

            text

        )

        return [s.strip() for s in sentences if s.strip()]

    def chunk(self, text: str):

        text = self.clean_text(text)

        sentences = self.split_into_sentences(text)

        chunks = []

        current_chunk = ""

        for sentence in sentences:

            if len(current_chunk) + len(sentence) <= self.chunk_size:

                current_chunk += " " + sentence

            else:

                chunks.append(current_chunk.strip())

                words = current_chunk.split()

                overlap_words = words[-self.overlap:]

                current_chunk = " ".join(overlap_words)

                current_chunk += " " + sentence

        if current_chunk.strip():

            chunks.append(current_chunk.strip())

        return chunks