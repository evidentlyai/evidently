# ruff: noqa: E501
# fmt: off
from evidently.core.datasets import Descriptor
from evidently.pydantic_utils import register_type_alias

register_type_alias(Descriptor, "evidently.core.datasets.FeatureDescriptor", "evidently:descriptor_v2:FeatureDescriptor")
register_type_alias(Descriptor, "evidently.descriptors._context_relevance.ContextRelevance", "evidently:descriptor_v2:ContextRelevance")
register_type_alias(Descriptor, "evidently.descriptors._custom_descriptors.CustomColumnDescriptor", "evidently:descriptor_v2:CustomColumnDescriptor")
register_type_alias(Descriptor, "evidently.descriptors._custom_descriptors.CustomDescriptor", "evidently:descriptor_v2:CustomDescriptor")
register_type_alias(Descriptor, "evidently.descriptors._text_length.TextLength", "evidently:descriptor_v2:TextLength")
