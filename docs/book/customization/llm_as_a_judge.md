---
description: How to use external LLMs to score text data. 
---
**Pre-requisites**:
* You know how to generate Reports or Test Suites for text data using Descriptors.
* You know how to pass custom parameters for Reports or Test Suites.
* You know how to specify text data in column mapping.

You can use external LLMs to score your text data. This method lets you evaluate texts based on any custom criteria that you define in a prompt.

The LLM “judge” must return a numerical score or a category for each text in a column. You will then be able to view scores, analyze their distribution or run conditional tests through the usual Descriptor interface.

Evidently currently supports scoring data using Open AI LLMs. Use the `OpenAIPrompting()` descriptor to define your prompt and criteria.

# Code example

You can refer to an end-to-end example with different Descriptors:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_evaluate_llm_with_text_descriptors.ipynb" %}

{% hint style="info" %}
**OpenAI key.** Add the OpenAI token as the environment variable: [see docs](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety). You will incur costs when running this eval.
{% endhint %}

To import the Descriptor:

```python
from evidently.descriptors import OpenAIPrompting
```

Define a prompt. This is a simplified example:

```python
pii_prompt = """
Please identify whether the below text contains personally identifiable information, such as name, address, date of birth, or other.
Text: REPLACE 
Use the following categories for PII identification:
1 if text contains PII
0 if text does not contain PII
0 if the provided data is not sufficient to make a clear determination
Return only one category.
"""
```
The prompt has a REPLACE placeholder that will be filled with the texts you want to evaluate. Evidently will take the content of each row in the selected column, insert into the placeholder position in a prompt and pass it to the LLM for scoring. 

To compute the score for the column `response` and get a summary Report:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        OpenAIPrompting(
            prompt=pii_prompt,
            prompt_replace_string="REPLACE",
            model="gpt-3.5-turbo-instruct",
            feature_type="cat",
            display_name="PII for response (by gpt3.5)"
            ),       
    ])
])
```
You can do the same for Test Suites. 

# Descriptor parameters 

| Parameter               | Description                                                                                                                                                                            |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `prompt: str`           | <ul><li>The text of the evaluation prompt that will be sent to the LLM.</li><li>Include at least one placeholder string.</li></ul>|
| `prompt_replace_string: str` | <ul><li> A placeholder string within the prompt that will be replaced by the evaluated text. </li><li> The default string name is "REPLACE".</li></ul>|
| `feature_type: str`     | <ul><li> The type of Descriptor the prompt will return. </li><li> Available: `num` (numerical) or `cat` (categorical). </li><li> This affects the statistics and default visualizations.</li></ul>|
| `context_replace_string: str` |<ul><li> An optional placeholder string within the prompt that will be replaced by the additional context. </li><li> The default string name is "CONTEXT".</li></ul>|
| `context: Optional[str]` | <ul><li> Additional context that will be added to the evaluation prompt, that **does not change** between evaluations. </li><li> Examples: a reference document, a set of positive and negative examples etc. </li><li> Pass this context as a string. </li><li> You cannot use `context` and `context_column` simultaneously. </li></ul>|
| `context_column: Optional[str]` | <ul><li> Additional context that will be added to the evaluation prompt, that is **specific to each row**. </li><li> Examples: a chunk of text retrieved from reference documents for a specific query. </li><li>  Point to the column that contains the context. </li><li> You cannot use `context` and `context_column` simultaneously. </li></ul>|
| `model: str`            | <ul><li> The name of the OpenAI model to be used for the LLM prompting, e.g., `gpt-3.5-turbo-instruct`. </li></ul> |
| `openai_params: Optional[dict]` |  <ul><li> A dictionary with additional parameters for the OpenAI API call. </li><li> Examples: temperature, max tokens, etc. Use parameters that OpenAI API accepts for a specific model.</li></ul> |
| `possible_values: Optional[List[str]]` | <ul><li> A list of possible values that the LLM can return.</li><li> This helps validate the output from the LLM and ensure it matches the expected categories. </li><li> If the validation does not pass, you will get None as a response. </li></ul>|
| `display_name: Optional[str]` | <ul><li> A display name visible in Reports and as a column name in tabular export. </li><li>Use it to name your Descriptor.</li></ul>|
