from torch.utils.data import DataLoader

from ai.training.dataset import ChatDataset


def create_dataloader(

    dataset_path,

    tokenizer,

    batch_size=8,

    max_length=128,

    shuffle=True

):

    dataset = ChatDataset(

        dataset_path,

        tokenizer,

        max_length

    )

    loader = DataLoader(

        dataset,

        batch_size=batch_size,

        shuffle=shuffle

    )

    return loader