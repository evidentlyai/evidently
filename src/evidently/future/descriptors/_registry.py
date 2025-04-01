from evidently.future.datasets import Descriptor
from evidently.pydantic_utils import register_type_alias

register_type_alias(
    Descriptor, "evidently.future.datasets.FeatureDescriptor", "evidently:descriptor_v2:FeatureDescriptor"
)
register_type_alias(
    Descriptor,
    "evidently.future.descriptors._context_relevance.ContextRelevance",
    "evidently:descriptor_v2:ContextRelevance",
)
register_type_alias(
    Descriptor,
    "evidently.future.descriptors._custom_descriptors.CustomColumnDescriptor",
    "evidently:descriptor_v2:CustomColumnDescriptor",
)
register_type_alias(
    Descriptor,
    "evidently.future.descriptors._custom_descriptors.CustomDescriptor",
    "evidently:descriptor_v2:CustomDescriptor",
)
register_type_alias(
    Descriptor, "evidently.future.descriptors._text_length.TextLength", "evidently:descriptor_v2:TextLength"
)
