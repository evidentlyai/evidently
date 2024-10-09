import os

from evidently.dataset_generators.llm.aaa import PromptQuestionGenerator, QuestionPairGenerator, SimpleQuestionPrompt
from evidently.dataset_generators.llm.index import SimpleIndexExtractor
from evidently.options.base import Options
from evidently.ui.workspace import CloudWorkspace


def main():
    generator = QuestionPairGenerator(
        index=SimpleIndexExtractor(chunks=["I am a banana"]),
        questions=PromptQuestionGenerator(prompt=SimpleQuestionPrompt()),
        num_questions=2,
        provider="openai",
        model="gpt-4o-mini",
        options=Options.from_any_options(None)
    )
    generated = generator.generate()
    print(generated)

    # client = CloudWorkspace(token=os.environ["EVIDENTLY_TOKEN"], url="https://app.evidently.dev")
    #
    # client.add_dataset(generated, "synth data", project_id="019270f6-6dda-7516-854b-aea2d84a4671")


if __name__ == '__main__':
    main()