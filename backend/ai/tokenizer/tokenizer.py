import re
import json

from ai.tokenizer.vocabulary import Vocabulary


class Tokenizer:

    def __init__(self):

        self.vocab = Vocabulary()

    def clean_text(self, text: str):

        text = text.lower()

        text = re.sub(r"\n", " ", text)

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"[^a-zA-Z0-9.,!? ]", "", text)

        return text.strip()

    def fit(self, texts):

        for text in texts:

            text = self.clean_text(text)

            self.vocab.add_text(text)

        self.vocab.build()

    def encode(self, text):

        text = self.clean_text(text)

        return self.vocab.encode(text)

    def decode(self, ids):

        return self.vocab.decode(ids)

    def batch_encode(self, texts):

        output = []

        for text in texts:

            output.append(self.encode(text))

        return output

    def pad_sequence(

        self,

        sequence,

        max_length

    ):

        pad_id = self.vocab.word2id[

            Vocabulary.PAD_TOKEN

        ]

        if len(sequence) > max_length:

            return sequence[:max_length]

        return sequence + [

            pad_id

        ] * (

            max_length - len(sequence)

        )

    def batch_pad(

        self,

        sequences,

        max_length

    ):

        padded = []

        for seq in sequences:

            padded.append(

                self.pad_sequence(

                    seq,

                    max_length

                )

            )

        return padded

    def save(self, folder):

        self.vocab.save(

            f"{folder}/vocab.json"

        )

    def load(self, folder):

        self.vocab.load(

            f"{folder}/vocab.json"

        )