from typing import ClassVar
from typing import List

import pandas as pd

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

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        import torch
        from transformers import BertModel
        from transformers import BertTokenizer

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

        def cosine_similarity(embeddings1, embeddings2):
            return torch.nn.functional.cosine_similarity(embeddings1.unsqueeze(1), embeddings2.unsqueeze(0), dim=-1)

        def max_similarity(embeddings1, embeddings2):
            # Compute max cosine similarity for each token in embeddings1 with respect to embeddings2
            similarity_matrix = cosine_similarity(embeddings1, embeddings2)
            return similarity_matrix.max(dim=1).values

        scores = []
        for emb1, emb2 in zip(embeddings_first, embeddings_second):
            recall = max_similarity(emb1, emb2).mean().item()
            precision = max_similarity(emb2, emb1).mean().item()
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            scores.append(f1_score)

        # Return as a DataFrame
        return pd.DataFrame(
            {
                self._feature_name(): pd.Series(scores, index=data.index),
            }
        )

    def _feature_name(self):
        return "|".join(self.columns)

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_name(),
            default_display_name=f"BERTScore for {' '.join(self.columns)}.",
        )
