"""Guardrails for validating and filtering LLM outputs.

Guardrails provide runtime checks to ensure LLM outputs meet specific criteria
before they are used. They can block, filter, or transform outputs based on
custom rules.

Available guards:
- `PIICheck`: Detect personally identifiable information
- `IncludesWords`: Check if output contains specific words
- `WordsPresence`: Check for presence/absence of word lists
- `PythonFunction`: Custom validation using Python functions

Use the `@guard` decorator to apply guards to LLM functions.

Example:
```python
from evidently.guardrails import guard, PIICheck

@guard(PIICheck())
def generate_response(prompt: str) -> str:
    # LLM generation code
    pass
```
"""

from .core import GuardException
from .decorators import guard
from .guards import IncludesWords
from .guards import PIICheck
from .guards import PythonFunction
from .guards import WordsPresence

__all__ = ["guard", "PIICheck", "PythonFunction", "IncludesWords", "WordsPresence", "GuardException"]
