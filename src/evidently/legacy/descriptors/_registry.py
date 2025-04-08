from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneralDescriptor
from evidently.pydantic_utils import register_type_alias

register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.custom_descriptor.CustomColumnEval",
    "evidently:descriptor:CustomColumnEval",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.hf_descriptor.HuggingFaceModel",
    "evidently:descriptor:HuggingFaceModel",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.hf_descriptor.HuggingFaceToxicityModel",
    "evidently:descriptor:HuggingFaceToxicityModel",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.is_valid_python_descriptor.IsValidPython",
    "evidently:descriptor:IsValidPython",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.json_schema_match_descriptor.JSONSchemaMatch",
    "evidently:descriptor:JSONSchemaMatch",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.llm_judges.BiasLLMEval", "evidently:descriptor:BiasLLMEval"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.llm_judges.BinaryClassificationLLMEval",
    "evidently:descriptor:BinaryClassificationLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.llm_judges.ContextQualityLLMEval",
    "evidently:descriptor:ContextQualityLLMEval",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.llm_judges.DeclineLLMEval", "evidently:descriptor:DeclineLLMEval"
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.llm_judges.LLMEval", "evidently:descriptor:LLMEval"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.llm_judges.NegativityLLMEval",
    "evidently:descriptor:NegativityLLMEval",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.llm_judges.PIILLMEval", "evidently:descriptor:PIILLMEval"
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.llm_judges.ToxicityLLMEval", "evidently:descriptor:ToxicityLLMEval"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.llm_judges.CorrectnessLLMEval",
    "evidently:descriptor:CorrectnessLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.llm_judges.FaithfulnessLLMEval",
    "evidently:descriptor:FaithfulnessLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.llm_judges.CompletenessLLMEval",
    "evidently:descriptor:CompletenessLLMEval",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.non_letter_character_percentage_descriptor.NonLetterCharacterPercentage",
    "evidently:descriptor:NonLetterCharacterPercentage",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.oov_words_percentage_descriptor.OOV", "evidently:descriptor:OOV"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.openai_descriptor.OpenAIPrompting",
    "evidently:descriptor:OpenAIPrompting",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.regexp_descriptor.RegExp", "evidently:descriptor:RegExp"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.semantic_similarity.SemanticSimilarity",
    "evidently:descriptor:SemanticSimilarity",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.BERTScore_descriptor.BERTScore",
    "evidently:descriptor:BERTScore",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.sentence_count_descriptor.SentenceCount",
    "evidently:descriptor:SentenceCount",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.sentiment_descriptor.Sentiment", "evidently:descriptor:Sentiment"
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.text_contains_descriptor.Contains", "evidently:descriptor:Contains"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.text_contains_descriptor.DoesNotContain",
    "evidently:descriptor:DoesNotContain",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.text_contains_descriptor.ItemMatch",
    "evidently:descriptor:ItemMatch",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.text_contains_descriptor.ItemNoMatch",
    "evidently:descriptor:ItemNoMatch",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.text_length_descriptor.TextLength",
    "evidently:descriptor:TextLength",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.text_part_descriptor.BeginsWith", "evidently:descriptor:BeginsWith"
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.text_part_descriptor.EndsWith", "evidently:descriptor:EndsWith"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.trigger_words_presence_descriptor.TriggerWordsPresence",
    "evidently:descriptor:TriggerWordsPresence",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.word_count_descriptor.WordCount", "evidently:descriptor:WordCount"
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.words_descriptor.ExcludesWords",
    "evidently:descriptor:ExcludesWords",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.words_descriptor.IncludesWords",
    "evidently:descriptor:IncludesWords",
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.words_descriptor.WordMatch", "evidently:descriptor:WordMatch"
)
register_type_alias(
    FeatureDescriptor, "evidently.legacy.descriptors.words_descriptor.WordNoMatch", "evidently:descriptor:WordNoMatch"
)
register_type_alias(
    GeneralDescriptor,
    "evidently.legacy.descriptors.custom_descriptor.CustomPairColumnEval",
    "evidently:descriptor:CustomPairColumnEval",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.is_valid_sql_descriptor.IsValidSQL",
    "evidently:descriptor:IsValidSQL",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.json_match_descriptor.JSONMatch",
    "evidently:descriptor:JSONMatch",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.contains_link_descriptor.ContainsLink",
    "evidently:descriptor:ContainsLink",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.exact_match_descriptor.ExactMatch",
    "evidently:descriptor:ExactMatch",
)
register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.is_valid_json_descriptor.IsValidJSON",
    "evidently:descriptor:IsValidJSON",
)

register_type_alias(
    FeatureDescriptor,
    "evidently.legacy.descriptors.llm_judges.MulticlassClassificationLLMEval",
    "evidently:descriptor:MulticlassClassificationLLMEval",
)
