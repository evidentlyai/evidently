from evidently.pydantic_utils import register_type_alias
from evidently.sdk.artifacts import ArtifactContent
from evidently.sdk.configs import ConfigContent

register_type_alias(
    ConfigContent, "evidently.sdk.configs.DescriptorContent", "evidently:config_content:DescriptorContent"
)

register_type_alias(
    ArtifactContent,
    "evidently.llm.prompts.content.ArtifactPromptContent",
    "evidently:artifact_content:ArtifactPromptContent",
)
register_type_alias(
    ArtifactContent, "evidently.sdk.configs.DescriptorContent", "evidently:artifact_content:DescriptorContent"
)
