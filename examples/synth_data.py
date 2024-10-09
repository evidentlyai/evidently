import os

from evidently.dataset_generators.llm.aaa import QuestionPairGenerator
from evidently.dataset_generators.llm.index import SimpleIndexExtractor
from evidently.dataset_generators.llm.prompts import BaselineAnswerPrompt, NaiveQuestionsPrompt
from evidently.options.base import Options
from evidently.ui.workspace import CloudWorkspace


def main():
    generator = QuestionPairGenerator(
        index=SimpleIndexExtractor(chunks=["I am a banana", "My spoon is too big"]),
        questions=NaiveQuestionsPrompt(),
        answers=BaselineAnswerPrompt(),
        provider="openai",
        model="gpt-4o-mini",
        num_questions=5,
        options=Options.from_any_options(None)
    )
    print(generator.questions.get_template())
    generated = generator.generate()
    for _, a in generated.iterrows():
        print("Q", a["questions"])
        print("A", a["answers"])
        print("C", a["context"])
        print()

    # client = CloudWorkspace(token=os.environ["EVIDENTLY_TOKEN"], url="https://app.evidently.dev")
    #
    # client.add_dataset(generated, "synth data", project_id="019270f6-6dda-7516-854b-aea2d84a4671")


if __name__ == '__main__':
    main()