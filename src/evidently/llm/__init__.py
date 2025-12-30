"""LLM-specific features for evaluating language model outputs.

This module provides tools for working with LLM evaluations, including:
- Prompt templates and rendering
- RAG (Retrieval-Augmented Generation) utilities
- LLM optimization tools
- Data generation for LLM testing

Most LLM evaluation functionality is available through `descriptors` (e.g.,
`LLMEval`, `LLMJudge`) and standard `Report` workflows. This module contains
lower-level utilities for advanced use cases.

For LLM evaluation workflows, see:
- `evidently.descriptors` for LLM-based descriptors
- `evidently.presets.TextEvals` for summarizing text evaluations
"""
