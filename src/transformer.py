from src.constants import DEVICE
from src.constants import BASE_PATH
from src.constants import FFN_MODEL_NAME
from src.constants import TRANSFORMER_MODEL_NAME
from src.dataset import Dataset
from torch import tensor
from torch.nn import BCELoss
from torch.nn import Module
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AdamW
from transformers import BertModel
from transformers import BertTokenizer
import numpy as np
import os
import pudb
import time
import torch
import sklearn

class FeedForwardModel(Module):
    def __init__(self, max_length):
        super().__init__()
        self.dense_1 = torch.nn.Linear(768, 1)
        self.sigmoid_1 = torch.nn.Sigmoid()

    def forward(self, x):
        output_1 = self.dense_1(x)
        output_2 = self.sigmoid_1(output_1)
        return output_2

class Bert:
    def __init__(self):
        self.max_length = 30
        self.batch_size = 32
        self.pad_token = "<pad>"
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', max_length=self.max_length)
        self.ffn_model = FeedForwardModel(self.max_length)
        self.bert = BertModel.from_pretrained('bert-base-uncased')

    def tokenize(self, batch_strings:list):
        batch_list = []
        for string in batch_strings:
            input_ids = torch.tensor(self.tokenizer.encode(string, max_length=self.max_length, add_special_tokens=True))
            batch_list.append(input_ids)
        batch = torch.stack(batch_list)
        return batch

    def forward_bert(self, x, attention_mask):
        batch_size = x.shape[0]
        bert_output = self.bert(x, attention_mask=attention_mask)
        bert_output = bert_output[0]
        output_1 = torch.zeros((batch_size, 768)).to(DEVICE)
        for i in range(batch_size):
            output_1[i] = bert_output[i][0]
        return output_1


    def forward(self, x, attention_mask):
        output_1 = self.forward_bert(x, attention_mask)
        output_2 = self.ffn_model(output_1)
        return output_2

    def train(self, dataset):
        print("starting training")

        parameters = [{"params": self.ffn_model.parameters(), "lr":0.001},
                      {"params": self.bert.parameters(), "lr": 0.00001}]


        optimizer = AdamW(self.ffn_model.parameters())
        loss_function = BCELoss(reduce="sum")

        self.ffn_model.train()
        self.bert.train()

        dataloader = DataLoader(dataset, batch_size=self.batch_size, collate_fn=self.collate_fn, drop_last=False)

        epochs = 10
        batches = int(len(dataset) / self.batch_size)
        self.ffn_model = self.ffn_model.to(DEVICE)
        self.bert = self.bert.to(DEVICE)


        previous_running_loss = 1.0
        for epoch in range(epochs):
            running_loss = 0
            progress_bar = tqdm(total=batches)

            for encoded_abstracts, targets, attention_mask in dataloader:
                encoded_abstracts = encoded_abstracts.to(DEVICE)
                targets = targets.to(DEVICE)


                # # zero the parameter gradients
                optimizer.zero_grad()

                with torch.set_grad_enabled(True):
                    output = self.forward(encoded_abstracts, attention_mask)
                    loss = loss_function(output, targets)
                    loss.backward()
                    optimizer.step()

                running_loss += loss.item()
                progress_bar.update(1)

            progress_bar.set_description(f"Loss: {running_loss}")

            if  abs(running_loss - previous_running_loss) < 0.01:
                break

            previous_running_loss = running_loss

        threshold = self.optimize_threshold(dataset)
        print(threshold)

    def optimize_threshold(self, dataset):
        classifications = self.__classify(dataset)

        y_true = [y for x,y in dataset]
        scores = []
        for threshold in np.arange(0.0, 1.0, 0.01):
            y_pred = [(1 if threshold < score[0] else 0) for score in classifications]
            f1_score = sklearn.metrics.f1_score(y_true, y_pred)
            scores.append( (f1_score, threshold) )
        scores = sorted(scores)
        return scores[0][1]

    def collate_fn(self, elems):
        link_tags = list(map(lambda x: x[0], elems))
        texts = list(map(lambda x: x[1], elems))
        targets = list(map(lambda x: x[2], elems))

        sentences = [ f"{link_tag} {self.tokenizer.sep_token} {title}" for link_tag, title in zip(link_tags, texts)]

        tokenized_sentences = [self.tokenizer.tokenize(sentence) for sentence in sentences]
        safe_tokenized_sentences = [self.cut_sentences(tokenized_sentence) for tokenized_sentence in tokenized_sentences]

        encoded_sentences = [self.tokenizer.convert_tokens_to_ids(tokenized_sentence) for tokenized_sentence in safe_tokenized_sentences]
        encoded_sentences = [self.tokenizer.build_inputs_with_special_tokens(encoded_sentence) for encoded_sentence in encoded_sentences]

        padded_encoded_sentences = [self.pad_token_ids(encoded_sentence) for encoded_sentence in encoded_sentences]

        attention_mask = self.create_attention_mask(safe_tokenized_sentences)

        return tensor(padded_encoded_sentences), tensor([targets]).t(), attention_mask 

    def cut_sentences(self, tokenized_sentence):
        sentence_length = len(tokenized_sentence)
        if sentence_length  == 0:
            return [self.tokenizer.unk_token]
        elif self.max_length <= sentence_length + 2:
            # -2 Offset is because <\s> and <\s> will be added
            return tokenized_sentence[:self.max_length - 2]
        else:
            return tokenized_sentence

    def pad_token_ids(self, token_ids):
        if len(token_ids) < self.max_length:
            pad_tokens = self.max_length - len(token_ids)
            padding = [self.tokenizer.pad_token_id] * pad_tokens
            padded_tokenized_sentence = token_ids + padding
            return padded_tokenized_sentence
        else:
            return token_ids

    def create_attention_mask(self, safe_tokenized_sentences):
        sentence_lengths = list(map(lambda x: min(len(x), self.max_length), safe_tokenized_sentences))
        batch_size = len(sentence_lengths)
        attention_mask = torch.zeros(batch_size, self.max_length)
        for i in range(batch_size):
            length = sentence_lengths[i]
            attention_mask[i][0:length] = 1
        return attention_mask

    def classify(self, dataset):

        self.ffn_model = self.ffn_model.to(DEVICE)
        self.bert = self.bert.to(DEVICE)

        return self.__classify(dataset)

    def __classify(self, dataset):
        dataloader = DataLoader(dataset, batch_size=self.batch_size, collate_fn=self.collate_fn, drop_last=False)

        outputs = []
        for encoded_abstracts, targets, attention_mask in tqdm(dataloader, desc="classifying"):
            encoded_abstracts = encoded_abstracts.to(DEVICE)

            output = self.forward(encoded_abstracts, attention_mask)
            outputs.extend(output.tolist())

        return outputs

    def pad(self, abstract):
        if len(abstract) < self.max_length:
            pads = self.max_length - len(abstract)
            padded_abstract = abstract + [self.pad_token]*pads
        else:
            padded_abstract = abstract[0:self.max_length]
        return padded_abstract

    def __make_paths(self, source):
        ffn = f"{BASE_PATH}/{source}/{FFN_MODEL_NAME}"
        transformer= f"{BASE_PATH}/{source}/{TRANSFORMER_MODEL_NAME}"
        return transformer, ffn

    def save(self, source):
        transformer_path, ffn_path = self.__make_paths(source)
        torch.save(self.ffn_model, ffn_path)
        torch.save(self.bert, transformer_path)

    def load(self, source):
        transformer_path, ffn_path = self.__make_paths(source)
        self.ffn_model = torch.load(ffn_path, map_location=torch.device(DEVICE))
        self.bert = torch.load(transformer_path, map_location=torch.device(DEVICE))


