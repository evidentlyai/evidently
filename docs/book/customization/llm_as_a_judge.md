---
description: How to use external LLMs to score text data. 
---
**Pre-requisites**:
* You know how to generate Reports or Test Suites for text data using Descriptors.
* You know how to pass custom parameters for Reports or Test Suites.
* You know how to specify text data in column mapping.

You can use external LLMs to score your text data. This method lets you evaluate texts by any custom criteria you define in a prompt.

The LLM “judge” will return a numerical score or a category for each text in a column. It works like any other Evidently `descriptor`: you can view and analyze scores, run conditional Tests, and monitor evaluation results in time.

Evidently currently supports scoring data using Open AI LLMs (more LLMs coming soon). Use the `LLMEval` descriptor to create an evaluator with any custom criteria, or choose any of the built-in evaluators (like detection of Denials, Personally identifiable information, etc.).

# LLM Eval

## Code example

Refer to a How-to example:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_use_llm_judge_template.ipynb" %}

{% hint style="info" %}
**OpenAI key.** Add the token as the environment variable: [see docs](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety). You will incur costs when running this eval.
{% endhint %}

## Built-in evaluators

You can use built-in evaluators that include pre-written prompts for specific criteria. These descriptors default to returning a binary category label with reasoning and using `gpt-4o-mini` model from OpenAI.

**Imports**. Import the `LLMEval` and built-in evaluators you want to use:

```python
from evidently.descriptors import LLMEval, NegativityLLMEval, PIILLMEval, DeclineLLMEval
```

**Get a Report**. To create a Report, simply list them like any other descriptor:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        NegativityLLMEval(),
        PIILLMEval(),
        DeclineLLMEval()
    ])
])
```

**Parametrize evaluators**. You can switch the output format from `category` to `score` (0 to 1) or exclude the reasoning:

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

You can also create a custom LLM evaluator using the provided templates. You specify the parameters and evaluation criteria, and Evidently will generate the complete evaluation prompt to send to the LLM together with the evaluation data.

**Imports**. To import the template for the Binary Classification evaluator prompt:

```python
from evidently.features.llm_judge import BinaryClassificationPromptTemplate
```

**Fill in the template**. Include the definition of your `criteria`, names of categories, etc. For example, to define the prompt for "conciseness" evaluation:

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
    model = "gpt-4o-mini",
    display_name="Conciseness",
)
```

See the explanation of each parameter below.

You do not need to explicitly ask the LLM to classify your input into two classes, ask for reasoning, or format it specially. This is already part of the template.

**Using text from multiple columns**. You can use this template to run evals that use data from multiple columns. 

For example, you can evaluate the output in the `response` column, simultaneously including data from the `context` or `question` column. This applies to scenarios like classifying the relevance of the response in relation to the question or its factuality based on context, etc.

Pass the names of the `additional_columns` in your dataset and reference the `{column}` when you write the `criteria`. When you run the eval, Evidently will insert the contents of each text in the corresponding column in the evaluation prompt.

```python
multi_column_judge = LLMEval(
        subcolumn="category",
        additional_columns={"question": "question"},
        template=BinaryClassificationPromptTemplate(
            criteria=""""Relevance" refers to the response directly addresses the question and effectively meets the user's intent.  
Relevant answer is an answer that directly addresses the question and effectively meets the user's intent.

=====
{question}
=====
            """,
            target_category="Relevant",
            non_target_category="Irrelevant",
            include_reasoning=True,
            pre_messages=[("system",
                           "You are an expert evaluator assessing the quality of a Q&A system. Your goal is to determine if the provided answer is relevant to the question based on the criteria below.")],
        ),
        provider="openai",
        model="gpt-4o-mini",
        display_name="Relevancy"
    )
```

You do not need to explicitly include the name of your primary column in the evaluation prompt. Since you include it as `column_name` in the `TextEvals` preset, it will be automatically passed to the template. 

```
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        multi_column_judge
    ])
])
```

## Parameters

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
| `non_target_category` | Name of the undesired or negative category.                                                          |
| `uncertainty`      | Category to return when the provided information is not sufficient to make a clear determination. Available: `unknown` (Default), `target`, `non_target`.
| `include_reasoning`| Specifies whether to include reasoning in the classification. Available: `True` (Default), `False`. It will be included with the result. |
| `pre_messages`     | List of system messages that set context or instructions before the evaluation task. For example, you can explain the evaluator role ("you are an expert..") or context ("your goal is to grade the work of an intern..") |
| `additional_columns`| A dictionary of additional columns present in your dataset to include in the evaluation prompt. Use it to map the column name to the placeholder name you reference in the `criteria`. For example: `({"mycol": "question"}`. |

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
