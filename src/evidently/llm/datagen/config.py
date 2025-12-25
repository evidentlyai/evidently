import random
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from evidently.llm.utils.blocks import PromptBlock


class UserProfile(PromptBlock):
    """User profile block for dataset generation prompts.

    Defines the characteristics of the user persona for generating
    contextually appropriate examples (e.g., intent, role, tone).

    Args:
    * `intent`: Optional user intent or goal.
    * `role`: Optional user role or persona.
    * `tone`: Communication tone (default: "neutral").
    """

    intent: Optional[str] = None
    """Optional user intent or goal."""
    role: Optional[str] = None
    """Optional user role or persona."""
    tone: str = "neutral"
    """Communication tone."""

    def render(self) -> str:
        """Render the user profile as a formatted string.

        Returns:
        * Formatted string describing the user profile.
        """
        messages = ["Assume the user profile is:"]
        if self.intent is not None:
            messages.append(f"- Intent: {self.intent}")
        if self.role is not None:
            messages.append(f"- Role: {self.role}")
        messages.append(f"- Tone: {self.tone}")
        return "\n".join(messages)


class Examples(PromptBlock):
    """Examples block for providing stylistic guidance in prompts.

    Contains example strings that guide the LLM to generate similar
    content in style, format, or structure.

    Args:
    * `examples`: List of example strings to use as guidance.
    """

    examples: List[str] = []
    """List of example strings to use as guidance."""

    def render(self) -> str:
        """Render examples as a formatted string.

        Returns:
        * Formatted string listing all examples.
        """
        res = ["Use these examples as stylistic guidance:"]
        for ex in self.examples:
            res.append(f"- {ex}")
        return "\n".join(res)

    def choice(self):
        """Get a random example from the list.

        Returns:
        * Randomly selected example string.
        """
        return random.choice(self.examples)


class ServiceSpec(PromptBlock):
    """Service specification block for describing the system context.

    Provides context about the service or system being evaluated,
    helping the LLM generate more relevant examples.

    Args:
    * `kind`: Type of service (e.g., "RAG", "chatbot").
    * `purpose`: Description of the service's purpose.
    """

    kind: str
    """Type of service (e.g., "RAG", "chatbot")."""
    purpose: str = ""
    """Description of the service's purpose."""

    def __init__(self, kind: str, purpose: str = "", **data: Any):
        self.kind = kind
        self.purpose = purpose
        super().__init__(**data)


class GenerationSpec(PromptBlock):
    """Generation specification block for defining what to generate.

    Specifies the type, complexity, and examples for content generation.
    Used in dataset generation prompts to guide the LLM.

    Args:
    * `kind`: Type of content to generate (e.g., "questions", "responses").
    * `complexity`: Complexity level ("low", "medium", "high").
    * `examples`: Optional examples to guide generation (can be `Examples` object, list of strings, or single string).
    """

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
        """Check if examples are available.

        Returns:
        * `True` if examples are set and non-empty, `False` otherwise.
        """
        return self.examples is not None and len(self.examples.examples) > 0
