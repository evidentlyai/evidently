from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneralDescriptor
from evidently.pydantic_utils import register_type_alias

register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.custom_descriptor.CustomColumnEval",
    "evidently:descriptor:CustomColumnEval",
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.hf_descriptor.HuggingFaceModel", "evidently:descriptor:HuggingFaceModel"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.hf_descriptor.HuggingFaceToxicityModel",
    "evidently:descriptor:HuggingFaceToxicityModel",
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.llm_judges.BiasLLMEval", "evidently:descriptor:BiasLLMEval"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.llm_judges.BinaryClassificationLLMEval",
    "evidently:descriptor:BinaryClassificationLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.llm_judges.ContextQualityLLMEval",
    "evidently:descriptor:ContextQualityLLMEval",
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.llm_judges.DeclineLLMEval", "evidently:descriptor:DeclineLLMEval"
)
register_type_alias(FeatureDescriptor, "evidently.descriptors.llm_judges.LLMEval", "evidently:descriptor:LLMEval")
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.llm_judges.NegativityLLMEval", "evidently:descriptor:NegativityLLMEval"
)
register_type_alias(FeatureDescriptor, "evidently.descriptors.llm_judges.PIILLMEval", "evidently:descriptor:PIILLMEval")
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.llm_judges.ToxicityLLMEval", "evidently:descriptor:ToxicityLLMEval"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.non_letter_character_percentage_descriptor.NonLetterCharacterPercentage",
    "evidently:descriptor:NonLetterCharacterPercentage",
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.oov_words_percentage_descriptor.OOV", "evidently:descriptor:OOV"
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.openai_descriptor.OpenAIPrompting", "evidently:descriptor:OpenAIPrompting"
)
register_type_alias(FeatureDescriptor, "evidently.descriptors.regexp_descriptor.RegExp", "evidently:descriptor:RegExp")
register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.semantic_similarity.SemanticSimilarity",
    "evidently:descriptor:SemanticSimilarity",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.sentence_count_descriptor.SentenceCount",
    "evidently:descriptor:SentenceCount",
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.sentiment_descriptor.Sentiment", "evidently:descriptor:Sentiment"
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.text_contains_descriptor.Contains", "evidently:descriptor:Contains"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.text_contains_descriptor.DoesNotContain",
    "evidently:descriptor:DoesNotContain",
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.text_length_descriptor.TextLength", "evidently:descriptor:TextLength"
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.text_part_descriptor.BeginsWith", "evidently:descriptor:BeginsWith"
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.text_part_descriptor.EndsWith", "evidently:descriptor:EndsWith"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.descriptors.trigger_words_presence_descriptor.TriggerWordsPresence",
    "evidently:descriptor:TriggerWordsPresence",
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.word_count_descriptor.WordCount", "evidently:descriptor:WordCount"
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.words_descriptor.ExcludesWords", "evidently:descriptor:ExcludesWords"
)
register_type_alias(
    FeatureDescriptor, "evidently.descriptors.words_descriptor.IncludesWords", "evidently:descriptor:IncludesWords"
)
register_type_alias(
    GeneralDescriptor,
    "evidently.descriptors.custom_descriptor.CustomPairColumnEval",
    "evidently:descriptor:CustomPairColumnEval",
)
