import random
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from evidently.llm.utils.blocks import PromptBlock


class UserProfile(PromptBlock):
    """Assume the user profile is:
    - Intent: {intent}
    - Role: {role}
    - Tone: {tone}"""

    intent: Optional[str] = None
    """Optional user intent or goal."""
    role: Optional[str] = None
    """Optional user role or persona."""
    tone: str = "neutral"
    """Communication tone (default: "neutral")."""

    def render(self) -> str:
        messages = ["Assume the user profile is:"]
        if self.intent is not None:
            messages.append(f"- Intent: {self.intent}")
        if self.role is not None:
            messages.append(f"- Role: {self.role}")
        messages.append(f"- Tone: {self.tone}")
        return "\n".join(messages)


class Examples(PromptBlock):
    """Use these examples as stylistic guidance:
    {examples}"""

    examples: List[str] = []
    """List of example strings to use as stylistic guidance."""

    def render(self) -> str:
        res = ["Use these examples as stylistic guidance:"]
        for ex in self.examples:
            res.append(f"- {ex}")
        return "\n".join(res)

    def choice(self):
        return random.choice(self.examples)


class ServiceSpec(PromptBlock):
    """Service: {kind}
    Purpose: {purpose}"""

    kind: str
    """Type of service (e.g., "RAG", "chatbot")."""
    purpose: str = ""
    """Description of the service's purpose."""

    def __init__(self, kind: str, purpose: str = "", **data: Any):
        self.kind = kind
        self.purpose = purpose
        super().__init__(**data)


class GenerationSpec(PromptBlock):
    """Generate {kind} with {complexity} complexity.
    {examples}"""

    kind: str = "questions"
    """Type of content to generate (e.g., "questions", "responses")."""
    complexity: str = "medium"
    """Complexity level ("low", "medium", "high")."""
    examples: Optional[Examples] = None
    """Optional examples to guide generation."""

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
