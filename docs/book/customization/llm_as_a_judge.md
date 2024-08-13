---
description: How to use external LLMs to score text data. 
---
**Pre-requisites**:
* You know how to generate Reports or Test Suites for text data using Descriptors.
* You know how to pass custom parameters for Reports or Test Suites.
* You know how to specify text data in column mapping.

You can use external LLMs to score your text data. This method lets you evaluate texts based on any custom criteria that you define in a prompt.

The LLM “judge” must return a numerical score or a category for each text in a column. You will then be able to view scores, analyze their distribution or run conditional tests through the usual Descriptor interface.

Evidently currently supports scoring data using Open AI LLMs (more LLMs coming soon). Use the `LLMEval` descriptor to define your prompt and criteria, or one of the built-in evaluators.

# LLM Eval

## Code example

You can refer to a How-to example with different LLM judges:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_use_llm_judge_template.ipynb" %}

{% hint style="info" %}
**OpenAI key.** Add the OpenAI token as the environment variable: [see docs](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety). You will incur costs when running this eval.
{% endhint %}

## Built-in templates

You can use built-in evaluation templates. They default to returning a binary category label with reasoning and using `gpt-4o-mini` model from OpenAI.

Imports:

```python
from evidently.descriptors import LLMEval, NegativityLLMEval, PIILLMEval, DeclineLLMEval
```

To create a Report with these descriptors, simply list them:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        NegativityLLMEval(),
        PIILLMEval(),
        DeclineLLMEval()
    ])
])
```

You can also use parameters to modify the output to switch from `category` to `score` (0 to 1) in the output or to exclude the reasoning:

```python
report = Report(metrics=[
    TextEvals(column_name="question", descriptors=[
        NegativityLLMEval(include_category=False),   
        PIILLMEval(include_reasoning=False), 
        DeclineLLMEval(include_score=True)
    ])
])
```

{% hint style="info" %}
**Which descriptors are there?** See the list of available built-in descriptors in the [All Metrics](../reference/all-metrics.md) page. 
{% endhint %}

## Custom LLM judge

You can also create a custom LLM judge using the provided templates. You can specify the parameters, and Evidently will automatically generate the complete evaluation prompt to send to the LLM together with the evaluation data.

Imports:
```python
from evidently.features.llm_judge import BinaryClassificationPromptTemplate
```

**Binary Classification template**. Example of defining a "conciseness" prompt:

```python
custom_judge = LLMEval(
    subcolumn="category",
    template = BinaryClassificationPromptTemplate(      
        criteria = """Conciseness refers to the quality of being brief and to the point, while still providing all necessary information.
            A concise response should:
            - Provide the necessary information without unnecessary details or repetition.
            - Be brief yet comprehensive enough to address the query.
            - Use simple and direct language to convey the message effectively.
        """,
        target_category="concise",
        non_target_category="verbose",
        uncertainty="unknown",
        include_reasoning=True,
        pre_messages=[("system", "You are a judge which evaluates text.")],
        ),
    provider = "openai",
    model = "gpt-4o-mini"
)
```

### LLMEval Parameters

| Parameter    | Description                                                      |
|--------------|------------------------------------------------------------------|
| `subcolumn`  | Specifies the type of descriptor. Available values: `category`, `score`. |
| `template`   | Forces a specific template for evaluation. Available: `BinaryClassificationPromptTemplate`.|
| `provider`   | The provider of the LLM to be used for evaluation. Available: `openai`. |
| `model`      | Specifies the model used for evaluation within the provider, e.g., `gpt-3.5-turbo-instruct`. |

### BinaryClassificationPromptTemplate 

| Parameter          | Description                                                                                                             |
|--------------------|-------------------------------------------------------------------------------------------------------------------------|
| `criteria`         | Free-form text defining evaluation criteria.                       |
| `target_category`  | Name of the desired or positive category.                                                             |
| `non_target_category` | Name of the undesired or negative category.                                                           |
| `uncertainty`      | Name of the category to return when the provided information is not sufficient to make a clear determination            |
| `include_reasoning`| Specifies whether to include reasoning in the classification. Available: `True`, `False`. It will be included with the result. |
| `pre_messages`     | List of system messages that set context or instructions before the evaluation task. For example, you can explain the evaluator role ("you are an expert..") or context ("your goal is to grade the work of an intern.." |


# OpenAIPrompting

There is an earlier implementation of this approach with `OpenAIPrompting` descriptor. See the documentation below.

<details>

<summary>OpenAIPrompting Descriptor</summary>

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

## Descriptor parameters 

- **`prompt: str`**
  - The text of the evaluation prompt that will be sent to the LLM.
  - Include at least one placeholder string.

- **`prompt_replace_string: str`**
  - A placeholder string within the prompt that will be replaced by the evaluated text.
  - The default string name is "REPLACE".

- **`feature_type: str`**
  - The type of Descriptor the prompt will return.
  - Available types: `num` (numerical) or `cat` (categorical).
  - This affects the statistics and default visualizations.

- **`context_replace_string: str`**
  - An optional placeholder string within the prompt that will be replaced by the additional context.
  - The default string name is "CONTEXT".

- **`context: Optional[str]`**
  - Additional context that will be added to the evaluation prompt, which **does not change** between evaluations.
  - Examples: a reference document, a set of positive and negative examples, etc.
  - Pass this context as a string.
  - You cannot use `context` and `context_column` simultaneously.

- **`context_column: Optional[str]`**
  - Additional context that will be added to the evaluation prompt, which is **specific to each row**.
  - Examples: a chunk of text retrieved from reference documents for a specific query.
  - Point to the column that contains the context.
  - You cannot use `context` and `context_column` simultaneously.

- **`model: str`**
  - The name of the OpenAI model to be used for the LLM prompting, e.g., `gpt-3.5-turbo-instruct`.

- **`openai_params: Optional[dict]`**
  - A dictionary with additional parameters for the OpenAI API call.
  - Examples: temperature, max tokens, etc.
  - Use parameters that OpenAI API accepts for a specific model.

- **`possible_values: Optional[List[str]]`**
  - A list of possible values that the LLM can return.
  - This helps validate the output from the LLM and ensure it matches the expected categories.
  - If the validation does not pass, you will get `None` as a response label.

- **`display_name: Optional[str]`**
  - A display name visible in Reports and as a column name in tabular export.
  - Use it to name your Descriptor.

</details>
