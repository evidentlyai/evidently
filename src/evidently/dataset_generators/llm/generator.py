from pathlib import Path

import pandas as pd

from evidently.dataset_generators.llm.aaa import QuestionPairGenerator
from evidently.dataset_generators.llm.index import IndexExtractorFromFile
from evidently.dataset_generators.llm.prompts import BaselineAnswerPrompt
from evidently.dataset_generators.llm.prompts import NaiveQuestionsPrompt
from evidently.options.base import Options


def generate_dataset_from_docs(file_path: Path, num_questions: 2) -> pd.DataFrame:
    documents = IndexExtractorFromFile(path=file_path)
    generator = QuestionPairGenerator(
        index=documents,
        questions=NaiveQuestionsPrompt(),
        answers=BaselineAnswerPrompt(),
        num_questions=num_questions,
        provider="openai",
        model="gpt-4o-mini",
        options=Options.from_any_options(None),
    )
    generated = generator.generate()
    return generated
