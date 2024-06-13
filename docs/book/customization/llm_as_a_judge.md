---
description: How to use external LLMs to score text data. 
---
# Pre-requisites:
* You know how to generate Reports or Test Suites for text data using Descriptors.
* You know how to pass custom parameters for Reports or Test Suites.
* You know how to specify text data in column mapping.

You can use external LLMs to score your text data. This method lets you evaluate texts based on any custom criteria that you define in a prompt.

The LLM “judge” must return a numerical score or a category for each text in a column. You will then be able to view scores, analyze their distribution or run conditional tests through the usual Descriptor interface.

Evidently currently supports scoring data using Open AI LLMs. Use the `OpenAIPrompting()` descriptor to define your prompt and criteria.

# Code example

You can refer to an end-to-end example with different Descriptors:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_evaluate_llm_with_text_descriptors.ipynb" %}

To import the Descriptor:

```python
from evidently.descriptors import OpenAIPrompting
```

{% hint style="info" %}
**OpenAI key.** To run the descriptor, you must the environment variable with the OpenAI token: [see docs](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety). You will incur costs when running this eval.
{% endhint %}

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
        OpenAIPrompting(prompt=pii_prompt, prompt_replace_string="REPLACE", model="gpt-3.5-turbo-instruct", feature_type="cat", display_name="PII for response (by gpt3.5)"),       
    ])
])
```
You can do the same for Test Suites. 

# Descriptor parameters 

| Parameter               | Description                                                                                                                                                                            |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `prompt: str`           | The text of the evaluation prompt that will be sent to the LLM. Include at least one placeholder string.                                                                                           |
| `prompt_replace_string: str` | A placeholder string within the prompt that will be replaced by the evaluated text. The default string name is "REPLACE". You can set another name using this parameter.        |
| `context_replace_string: str` | An optional placeholder string within the prompt that will be replaced by the additional context. The default string name is "CONTEXT". You can set another name using this parameter. |
| `context: Optional[str]` | You can include additional context in the evaluation prompt, such as a reference document or a set of positive and negative examples. Pass this context as a string.                          |
| `context_column: Optional[str]` | Alternatively, you can include the evaluation context that is specific to each row, such as a chunk of text retrieved from reference documents.                                      |
| `model: str`            | The name of the OpenAI model to be used for the LLM prompting, e.g., `gpt-3.5-turbo-instruct`.                                                                                          |
| `openai_params: Optional[dict]` | A dictionary with additional parameters for the OpenAI API call, such as temperature, max tokens, etc., based on the parameters OpenAI API accepts for a specific model.            |
| `feature_type: str`     | The type of Descriptor the prompt will return, either `num` (numerical) or `cat` (categorical). This affects the statistics and default visualizations.                               |
| `possible_values: Optional[List[str]]` | A list of possible values that the LLM can return. This helps validate the output from the LLM and ensure it matches the expected categories.                                |
| `display_name: Optional[str]` | Display name visible in Reports. Use it to name your Descriptor.                                                                                                                       |
