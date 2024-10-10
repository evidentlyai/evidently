from evidently.dataset_generators.llm.questions import QADatasetFromSeedGenerator, QADatasetGenerator
from evidently.dataset_generators.llm.index import DataCollectionProvider
from evidently.options.base import Options


def generate_from_file():
    file_path = "../cloud_quickstart_tracing.pdf"
    data = DataCollectionProvider.from_files(file_path, chunk_size=50, chunk_overlap=20)

    generator = QADatasetGenerator(
        data_collection=data,
        provider="openai",
        model="gpt-4o-mini",
        num_questions=5,
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


def main():
    data = DataCollectionProvider.from_chunks(chunks=["I am a banana", "My spoon is too big"])
    generator = QADatasetGenerator(
        data_collection=data,
        provider="openai",
        model="gpt-4o-mini",
        num_questions=5,
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


if __name__ == '__main__':
    main()
    # generate_from_file()
