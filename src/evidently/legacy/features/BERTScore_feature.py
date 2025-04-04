from collections import defaultdict
from typing import ClassVar
from typing import Dict
from typing import List

import numpy as np
import pandas as pd

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


class BERTScoreFeature(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:BERTScoreFeature"

    __feature_type__: ClassVar = ColumnType.Numerical
    columns: List[str]
    model: str = "bert-base-uncased"  # Pretrained BERT model
    tfidf_weighted: bool = False  # Whether to weight embeddings with IDF

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        # Load BERT model and tokenizer
        from transformers import BertModel
        from transformers import BertTokenizer

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
        embeddings_first = model(**tokens_first).last_hidden_state.detach().numpy()
        embeddings_second = model(**tokens_second).last_hidden_state.detach().numpy()
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
        token_counts: Dict[str, int] = defaultdict(int)
        for sentence in reference_sentences:
            tokens = [tokenizer.cls_token] + tokenizer.tokenize(sentence) + [tokenizer.sep_token]
            unique_tokens = set(tokens)
            for token in unique_tokens:
                token_counts[token] += 1

        idf_scores = {token: -np.log(count / M) for token, count in token_counts.items()}

        # Convert IDF scores to numpy arrays
        def convert_to_idf_arrays(sentences):
            idf_arrays = []
            for sentence in sentences:
                tokens = tokenizer.tokenize(sentence)

                # Add special tokens
                tokens = [tokenizer.cls_token] + tokens + [tokenizer.sep_token]
                # Compute IDF scores for each token including plus one smoothing
                idf_array = np.array([idf_scores.get(token, 0) + 1 for token in tokens])
                idf_arrays.append(idf_array)
            # Pad sequences to the same length
            max_len = max(len(arr) for arr in idf_arrays)
            idf_arrays = np.array([np.pad(arr, (0, max_len - len(arr)), "constant") for arr in idf_arrays])
            return idf_arrays

        idf_arrays1 = convert_to_idf_arrays(col1.fillna("").tolist())
        idf_arrays2 = convert_to_idf_arrays(col2.fillna("").tolist())
        return idf_arrays1, idf_arrays2

    def max_similarity(self, embeddings1, embeddings2):
        # Compute max cosine similarity for each token in embeddings1 with respect to embeddings2
        similarity_matrix = np.dot(embeddings1, embeddings2.T) / (
            np.linalg.norm(embeddings1, axis=1, keepdims=True) * np.linalg.norm(embeddings2, axis=1, keepdims=True).T
        )
        return similarity_matrix.max(axis=1)

    def calculate_scores(self, emb1, emb2, idf_scores, index):
        if self.tfidf_weighted:
            weighted_scores = np.multiply(self.max_similarity(emb1, emb2), idf_scores[0][index])
            recall = weighted_scores.sum() / idf_scores[0][index].sum()

            weighted_scores = np.multiply(self.max_similarity(emb2, emb1), idf_scores[1][index])
            precision = weighted_scores.sum() / idf_scores[1][index].sum()
        else:
            recall = self.max_similarity(emb1, emb2).mean()
            precision = self.max_similarity(emb2, emb1).mean()
        return recall, precision

    def _feature_name(self):
        return "|".join(self.columns)

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_name(),
            default_display_name=f"BERTScore for {' '.join(self.columns)}.",
        )
