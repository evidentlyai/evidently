import re
from typing import List
from typing import Optional


def get_tag(value, tag_name) -> Optional[str]:
    """Extract the content of a tag from a string value."""
    tag_name = re.escape(tag_name)
    match = re.search(rf"<{tag_name}>(.*?)</{tag_name}>", value, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def get_tags(value, tag_name) -> List[str]:
    """Extract list of tag contents from a string value."""
    tag_name = re.escape(tag_name)
    matches = re.findall(rf"<{tag_name}>(.*?)</{tag_name}>", value, re.DOTALL)
    return matches
