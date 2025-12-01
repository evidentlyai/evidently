from litestar.testing import TestClient

from evidently.legacy.features.llm_judge import BinaryClassificationPromptTemplate


def test_prompt_template(test_client: TestClient):
    """POST /api/llm_judges/prompt_template"""
    template = BinaryClassificationPromptTemplate(target_category="A", non_target_category="B")

    response = test_client.post("/api/llm_judges/prompt_template", json={"template": template.dict()})
    assert response.status_code in (200, 201)  # Accept both 200 and 201
    prompt_text = response.text.strip()
    assert "Classify text between ___text_starts_here___ and ___text_ends_here___ into" in prompt_text
    assert "two categories: A and B" in prompt_text
    assert "___text_starts_here___" in prompt_text
    assert "{input}" in prompt_text
    assert "___text_ends_here___" in prompt_text
    assert "A: if text is a" in prompt_text
    assert "B: if text is b" in prompt_text
    assert "UNKNOWN: use this category only if the information provided is not" in prompt_text
    assert "Think step by step" in prompt_text
    assert "Return category formatted as json" in prompt_text


def test_templates(test_client: TestClient):
    """GET /api/llm_judges/templates"""
    response = test_client.get("/api/llm_judges/templates")
    assert response.status_code == 200
    templates = response.json()
    assert isinstance(templates, list)
    assert len(templates) > 0

    # Check structure of first template
    template = templates[0]
    assert "name" in template
    assert "template" in template
    assert "prompt" in template
    assert "output_format" in template
    assert isinstance(template["name"], str)
    assert isinstance(template["prompt"], str)
    assert isinstance(template["output_format"], str)

    # Check that we have expected templates
    template_names = [t["name"] for t in templates]
    assert "Negativity" in template_names or any("negativity" in name.lower() for name in template_names)
    assert "Toxicity" in template_names or any("toxicity" in name.lower() for name in template_names)
