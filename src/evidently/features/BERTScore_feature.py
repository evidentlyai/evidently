from collections import defaultdict
from typing import ClassVar
from typing import List

import numpy as np
import pandas as pd
import torch
from torch.nn.functional import cosine_similarity
from transformers import BertModel
from transformers import BertTokenizer

from evidently.base_metric import ColumnName
from evidently.core import ColumnType
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class BERTScoreFeature(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:BERTScoreFeature"

    __feature_type__: ClassVar = ColumnType.Numerical
    columns: List[str]
    model: str = "bert-base-uncased"  # Pretrained BERT model
    tfidf_weighted: bool = False  # Whether to weight embeddings with IDF

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        # Load BERT model and tokenizer
        tokenizer = BertTokenizer.from_pretrained(self.model)
        model = BertModel.from_pretrained(self.model)

        # Tokenize sentences
        tokens_first = tokenizer(
            data[self.columns[0]].fillna("").tolist(), return_tensors="pt", padding=True, truncation=True
        )
        tokens_second = tokenizer(
            data[self.columns[1]].fillna("").tolist(), return_tensors="pt", padding=True, truncation=True
        )

        # Get embeddings
        with torch.no_grad():
            embeddings_first = model(**tokens_first).last_hidden_state
            embeddings_second = model(**tokens_second).last_hidden_state

        # Obtain IDF scores
        idf_scores = self.compute_idf_scores(data[self.columns[0]], data[self.columns[1]], tokenizer)

        scores = []
        for i, (emb1, emb2) in enumerate(zip(embeddings_first, embeddings_second)):
            recall, precision = self.calculate_scores(emb1, emb2, idf_scores, i)
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            scores.append(f1_score)

        # Return as a DataFrame
        return pd.DataFrame(
            {
                self._feature_name(): pd.Series(scores, index=data.index),
            }
        )

    def compute_idf_scores(self, col1: pd.Series, col2: pd.Series, tokenizer) -> tuple:
        # Combine reference sentences
        reference_sentences = pd.concat([col1, col2]).dropna().tolist()
        M = len(reference_sentences)

        # Compute IDF for each unique token
        token_counts = defaultdict(int)
        for sentence in reference_sentences:
            tokens = [tokenizer.cls_token] + tokenizer.tokenize(sentence) + [tokenizer.sep_token]
            unique_tokens = set(tokens)
            for token in unique_tokens:
                token_counts[token] += 1

        idf_scores = {token: -np.log(count / M) for token, count in token_counts.items()}

        # Convert IDF scores to tensors
        def convert_to_idf_tensors(sentences):
            idf_tensors = []
            for sentence in sentences:
                tokens = tokenizer.tokenize(sentence)

                # Add special tokens
                tokens = [tokenizer.cls_token] + tokens + [tokenizer.sep_token]
                # Compute IDF scores for each token including plus one smoothing
                idf_tensor = torch.tensor([idf_scores.get(token, 0) + 1 for token in tokens])
                idf_tensors.append(idf_tensor)
            # Pad sequences to the same length
            return torch.nn.utils.rnn.pad_sequence(idf_tensors, batch_first=True)

        idf_tensors1 = convert_to_idf_tensors(col1.fillna("").tolist())
        idf_tensors2 = convert_to_idf_tensors(col2.fillna("").tolist())
        return idf_tensors1, idf_tensors2

    def max_similarity(self, embeddings1, embeddings2):
        # Compute max cosine similarity for each token in embeddings1 with respect to embeddings2
        similarity_matrix = cosine_similarity(embeddings1.unsqueeze(1), embeddings2.unsqueeze(0), dim=-1)
        return similarity_matrix.max(dim=1).values

    def calculate_scores(self, emb1, emb2, idf_scores, index):
        if self.tfidf_weighted:
            weighted_scores = np.multiply(self.max_similarity(emb1, emb2), idf_scores[0][index])
            recall = weighted_scores.sum().item() / idf_scores[0][index].sum().item()

            weighted_scores = np.multiply(self.max_similarity(emb2, emb1), idf_scores[1][index])
            precision = weighted_scores.sum().item() / idf_scores[1][index].sum().item()
        else:
            recall = self.max_similarity(emb1, emb2).mean().item()
            precision = self.max_similarity(emb2, emb1).mean().item()
        return recall, precision

    def _feature_name(self):
        return "|".join(self.columns)

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_name(),
            default_display_name=f"BERTScore for {' '.join(self.columns)}.",
        )
