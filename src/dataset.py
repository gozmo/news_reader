import json
import random
import random
import os
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from src.constants import Labels
from src import io_utils

class BaseDataset(Dataset):
    def __init__(self, papers):
        self.papers= papers

    def __len__(self):
        return len(self.papers)

    def get_paper(self, idx):
        return self.papers[idx]

class TrainingDataset(BaseDataset):
    def __init__(self, source):
        positives = io_utils.read_label(source, Labels.POSITIVE)
        positives = zip(positives, [1.0]*len(positives))

        negatives = io_utils.read_label(source, Labels.NEGATIVE)
        negatives = zip(negatives, [0.0]*len(negatives))

        papers = list(positives) + list(negatives)
        BaseDataset.__init__(self, papers)

    def __getitem__(self, idx):
        text = self.papers[idx][0].text
        source_page = self.papers[idx][0].source
        label = self.papers[idx][1]

        return source_page, text, label

class ClassificationDataset(BaseDataset):
    def __init__(self, papers):
        BaseDataset.__init__(self, papers)

    def __getitem__(self, idx):
        text = self.papers[idx].text
        source_page = self.papers[idx].source
        label = 0.0

        return source_page, text, label

