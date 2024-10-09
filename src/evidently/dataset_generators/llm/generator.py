from pathlib import Path

import pandas as pd

from evidently.dataset_generators.llm.aaa import FileContextGenerator
from evidently.dataset_generators.llm.aaa import PromptQuestionGenerator
from evidently.dataset_generators.llm.aaa import QuestionPairGenerator
from evidently.dataset_generators.llm.aaa import SimpleQuestionPrompt
from evidently.options.base import Options


def generate_dataset_from_docs(file_path: Path, num_questions: 2) -> pd.DataFrame:
    chunks = FileContextGenerator(path=file_path)
    generator = QuestionPairGenerator(
        chunks=chunks,
        questions=PromptQuestionGenerator(prompt=SimpleQuestionPrompt()),
        num_questions=num_questions,
        provider="openai",
        model="gpt-4o-mini",
        options=Options.from_any_options(None),
    )
    generated = generator.generate()
    return generated
