from evidently.pydantic_utils import register_type_alias
from evidently.sdk.configs import ConfigContent

register_type_alias(
    ConfigContent, "evidently.sdk.configs.DescriptorContent", "evidently:config_content:DescriptorContent"
)
