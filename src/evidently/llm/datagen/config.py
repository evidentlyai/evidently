import random
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from evidently.llm.utils.blocks import PromptBlock


class UserProfile(PromptBlock):
    intent: Optional[str] = None
    role: Optional[str] = None
    tone: str = "neutral"

    def render(self) -> str:
        messages = ["Assume the user profile is:"]
        if self.intent is not None:
            messages.append(f"- Intent: {self.intent}")
        if self.role is not None:
            messages.append(f"- Role: {self.role}")
        messages.append(f"- Tone: {self.tone}")
        return "\n".join(messages)


class Examples(PromptBlock):
    examples: List[str] = []

    def render(self) -> str:
        res = ["Use these examples as stylistic guidance:"]
        for ex in self.examples:
            res.append(f"- {ex}")
        return "\n".join(res)

    def choice(self):
        return random.choice(self.examples)


class ServiceSpec(PromptBlock):
    """The {kind} system is built for the following purpose: {purpose}"""

    kind: str
    purpose: str = ""

    def __init__(self, kind: str, purpose: str = "", **data: Any):
        self.kind = kind
        self.purpose = purpose
        super().__init__(**data)


class GenerationSpec(PromptBlock):
    """
    Generate standalone {kind} with {complexity} complexity.
    {examples}
    """

    kind: str = "questions"
    complexity: str = "medium"
    examples: Optional[Examples] = None

    def __init__(
        self, kind: str, complexity: str = "medium", examples: Union[Examples, List[str], str, None] = None, **data: Any
    ):
        self.kind = kind
        self.complexity = complexity
        if isinstance(examples, str):
            examples = [examples]
        if isinstance(examples, list):
            examples = Examples(examples=examples)
        self.examples = examples
        super().__init__(**data)

    @property
    def has_examples(self) -> bool:
        return self.examples is not None and len(self.examples.examples) > 0
