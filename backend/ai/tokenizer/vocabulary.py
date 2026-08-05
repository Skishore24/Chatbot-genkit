import json
from collections import Counter


class Vocabulary:

    PAD_TOKEN = "<PAD>"
    UNK_TOKEN = "<UNK>"
    BOS_TOKEN = "<BOS>"
    EOS_TOKEN = "<EOS>"

    def __init__(self):

        self.word2id = {}

        self.id2word = {}

        self.counter = Counter()

        self.special_tokens = [
            self.PAD_TOKEN,
            self.UNK_TOKEN,
            self.BOS_TOKEN,
            self.EOS_TOKEN,
        ]

    def add_text(self, text: str):

        words = text.lower().split()

        self.counter.update(words)

    def build(self, min_freq=1):

        self.word2id = {}

        self.id2word = {}

        index = 0

        for token in self.special_tokens:

            self.word2id[token] = index

            self.id2word[index] = token

            index += 1

        for word, freq in self.counter.items():

            if freq >= min_freq:

                self.word2id[word] = index

                self.id2word[index] = word

                index += 1

    def encode(self, text):

        words = text.lower().split()

        ids = []

        ids.append(self.word2id[self.BOS_TOKEN])

        for word in words:

            ids.append(

                self.word2id.get(
                    word,
                    self.word2id[self.UNK_TOKEN]
                )
            )

        ids.append(self.word2id[self.EOS_TOKEN])

        return ids

    def decode(self, ids):

        words = []

        for i in ids:

            words.append(

                self.id2word.get(
                    i,
                    self.UNK_TOKEN
                )

            )

        return " ".join(words)

    def save(self, path):

        with open(path, "w", encoding="utf-8") as f:

            json.dump(self.word2id, f, indent=4)

    def load(self, path):

        with open(path, "r", encoding="utf-8") as f:

            self.word2id = json.load(f)

        self.id2word = {

            int(v): k

            for k, v in self.word2id.items()

        }

    def __len__(self):

        return len(self.word2id)