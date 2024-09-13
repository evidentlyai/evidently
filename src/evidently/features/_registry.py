from evidently.features.generated_features import GeneratedFeatures
from evidently.pydantic_utils import register_type_alias

register_type_alias(
    GeneratedFeatures,
    "evidently.features.OOV_words_percentage_feature.OOVWordsPercentage",
    "evidently:feature:OOVWordsPercentage",
)
register_type_alias(
    GeneratedFeatures, "evidently.features.custom_feature.CustomFeature", "evidently:feature:CustomFeature"
)
register_type_alias(
    GeneratedFeatures,
    "evidently.features.custom_feature.CustomPairColumnFeature",
    "evidently:feature:CustomPairColumnFeature",
)
register_type_alias(
    GeneratedFeatures,
    "evidently.features.custom_feature.CustomSingleColumnFeature",
    "evidently:feature:CustomSingleColumnFeature",
)
register_type_alias(
    GeneratedFeatures, "evidently.features.hf_feature.HuggingFaceFeature", "evidently:feature:HuggingFaceFeature"
)
register_type_alias(
    GeneratedFeatures,
    "evidently.features.hf_feature.HuggingFaceToxicityFeature",
    "evidently:feature:HuggingFaceToxicityFeature",
)
register_type_alias(GeneratedFeatures, "evidently.features.llm_judge.LLMJudge", "evidently:feature:LLMJudge")
register_type_alias(
    GeneratedFeatures,
    "evidently.features.non_letter_character_percentage_feature.NonLetterCharacterPercentage",
    "evidently:feature:NonLetterCharacterPercentage",
)
register_type_alias(
    GeneratedFeatures, "evidently.features.openai_feature.OpenAIFeature", "evidently:feature:OpenAIFeature"
)
register_type_alias(GeneratedFeatures, "evidently.features.regexp_feature.RegExp", "evidently:feature:RegExp")
register_type_alias(
    GeneratedFeatures,
    "evidently.features.semantic_similarity_feature.SemanticSimilarityFeature",
    "evidently:feature:SemanticSimilarityFeature",
)
register_type_alias(
    GeneratedFeatures, "evidently.features.sentence_count_feature.SentenceCount", "evidently:feature:SentenceCount"
)
register_type_alias(GeneratedFeatures, "evidently.features.sentiment_feature.Sentiment", "evidently:feature:Sentiment")
register_type_alias(
    GeneratedFeatures, "evidently.features.text_contains_feature.Contains", "evidently:feature:Contains"
)
register_type_alias(
    GeneratedFeatures, "evidently.features.text_contains_feature.DoesNotContain", "evidently:feature:DoesNotContain"
)
register_type_alias(
    GeneratedFeatures, "evidently.features.text_length_feature.TextLength", "evidently:feature:TextLength"
)
register_type_alias(
    GeneratedFeatures, "evidently.features.text_part_feature.BeginsWith", "evidently:feature:BeginsWith"
)
register_type_alias(GeneratedFeatures, "evidently.features.text_part_feature.EndsWith", "evidently:feature:EndsWith")
register_type_alias(
    GeneratedFeatures,
    "evidently.features.trigger_words_presence_feature.TriggerWordsPresent",
    "evidently:feature:TriggerWordsPresent",
)
register_type_alias(GeneratedFeatures, "evidently.features.word_count_feature.WordCount", "evidently:feature:WordCount")
register_type_alias(
    GeneratedFeatures, "evidently.features.words_feature.ExcludesWords", "evidently:feature:ExcludesWords"
)
register_type_alias(
    GeneratedFeatures, "evidently.features.words_feature.IncludesWords", "evidently:feature:IncludesWords"
)
register_type_alias(
    GeneratedFeatures, "evidently.features.words_feature.WordsPresence", "evidently:feature:WordsPresence"
)
