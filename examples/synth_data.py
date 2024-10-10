import json
import os

from evidently.dataset_generators.llm.aaa import QADatasetFromSeedGenerator, QADatasetGenerator
from evidently.dataset_generators.llm.index import DataCollection, DataCollectionProvider
from evidently.dataset_generators.llm.prompts import BaselineAnswerPrompt, NaiveQuestionsFromContext
from evidently.options.base import Options
from evidently.ui.workspace import CloudWorkspace


def main():
    data = DataCollectionProvider.from_chunks(chunks=["I am a banana", "My spoon is too big"])
    generator = QADatasetGenerator(
        data_collection=data,
        provider="openai",
        model="gpt-4o-mini",
        num_questions=5,
        options=Options.from_any_options(None)
    )
    # print(generator.questions.get_template())
    # json.dumps(generator.dict())
    generated = generator.generate()
    for _, a in generated.iterrows():
        print("Q", a["questions"])
        if "answers" in a:
            print("A", a["answers"])
        if "context" in a:
            print("C", a["context"])
        print()

    generator = QADatasetFromSeedGenerator(
        seed_question="What is 'kek'?",
        num_questions=5,
        provider="openai",
        model="gpt-4o-mini",
        options=Options.from_any_options(None)
    )

    generated = generator.generate()
    for _, a in generated.iterrows():
        print("Q", a["questions"])
        if "answers" in a:
            print("A", a["answers"])
        if "context" in a:
            print("C", a["context"])
        print()

    # client = CloudWorkspace(token=os.environ["EVIDENTLY_TOKEN"], url="https://app.evidently.dev")
    #
    # client.add_dataset(generated, "synth data", project_id="019270f6-6dda-7516-854b-aea2d84a4671")


if __name__ == '__main__':
    main()