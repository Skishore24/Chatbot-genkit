import json
import torch

from torch.utils.data import Dataset


class ChatDataset(Dataset):

    def __init__(
        self,
        json_path,
        tokenizer,
        max_length=128
    ):

        self.tokenizer = tokenizer
        self.max_length = max_length
        self.samples = []

        with open(
            json_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        for item in data:

            instruction = item.get(
                "instruction",
                ""
            )

            output = item.get(
                "output",
                ""
            )

            text = instruction + " " + output

            ids = tokenizer.encode(text)

            ids = tokenizer.pad_sequence(
                ids,
                self.max_length
            )

            self.samples.append(ids)

    def __len__(self):

        return len(self.samples)

    def __getitem__(self, index):

        x = torch.tensor(
            self.samples[index][:-1],
            dtype=torch.long
        )

        y = torch.tensor(
            self.samples[index][1:],
            dtype=torch.long
        )

        return x, y