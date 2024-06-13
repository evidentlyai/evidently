---
description: How to use models available on HuggingFace as text Descriptors.
---

**Pre-requisites**:
* You know how to generate Reports or Test Suites for text data using Descriptors.
* You know how to pass custom parameters for Reports or Test Suites.
* You know to specify text data in column mapping.

You can use an external machine learning model to score text data. This method lets you evaluate texts based on any criteria from the source model, e.g. classify it into a set number of labels.

The model you use must return a numerical score or a category for each text in a column. You will then be able to view scores, analyze their distribution or run conditional tests through the usual Descriptor interface.

Evidently supports scoring text data using HuggingFace models. Use the general `HuggingFaceModel()` descriptor to select models on your own or simplified interfaces for pre-selected models like `HuggingFaceToxicityModel()`.

# Code example

You can refer to an end-to-end example with different Descriptors:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_evaluate_llm_with_text_descriptors.ipynb" %}

To import the Descriptor:

```python
from evidently.descriptors import HuggingFaceModel, HuggingFaceToxicityModel
```
To get a Report with a Toxicity score for the `response` column:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        HuggingFaceToxicityModel(toxic_label="hate"),
    ])
])
```

{% hint style="info" %}
**Which descriptors are there?** See the list of available built-in descriptors in the [All Metrics](../reference/all-metrics.md) page. 
{% endhint %}

To get a Report with with several different scores using the general `HuggingFaceModel()` descriptor:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        HuggingFaceModel(model="DaNLP/da-electra-hatespeech-detection", display_name="Response Toxicity"),
        HuggingFaceModel(model="SamLowe/roberta-base-go_emotions", params={"label": "disappointment"}, 
                         display_name="Disappointments in Response"), 
        HuggingFaceModel(model="SamLowe/roberta-base-go_emotions", params={"label": "optimism"}, 
                         display_name="Optimism in Response"),     
    ])
])
```

You can do the same for Test Suites. 

# Sample models

Here are some example models you can call using the  HuggingFaceModel() descriptor.

| Model | Parameters |                                                                                                              
|----|----|
| `SamLowe/roberta-base-go_emotions` <ul><li> Scores texts by 28 emotions. </li><li> Returns the predicted probability for the chosen emotion label. </li><li> Scale: 0 to 1. </li><li> `toxic_label="hate"` (default) </li><li> `display_name="display name"` </li></ul> **Example use**:<br> `HuggingFaceModel(model="SamLowe/roberta-base-go_emotions", params={"label": "disappointment"})` <br><br> **Source**: [HuggingFace Model](https://huggingface.co/SamLowe/roberta-base-go_emotions) | **Required**:<ul><li> `params={"label":"label"}`</li></ul>**Available labels**:<ul><li>admiration</li><li>amusement</li><li>anger</li><li>annoyance</li><li>approval</li><li>caring</li><li>confusion</li><li>curiosity</li><li>desire</li><li>disappointment</li><li>disapproval</li><li>disgust</li><li>embarrassment</li><li>excitement</li><li>fear</li><li>gratitude</li><li>grief</li><li>joy</li><li>love</li><li>nervousness</li><li>optimism</li><li>pride</li><li>realization</li><li>relief</li><li>remorse</li><li>sadness</li><li>surprise</li><li>neutral</li></ul></li>**Optional**:<ul><li>`display_name="display name"`</li></ul> |
| `facebook/roberta-hate-speech-dynabench-r4-target` <ul><li> Detects hate speech. </li><li> Returns predicted probability for the “hate” label. </li><li> Scale: 0 to 1. </li></ul> **Example use**:<br> `HuggingFaceModel(model="facebook/roberta-hate-speech-dynabench-r4-target", display_name="Toxicity")` <br><br> **Source**: [HuggingFace Model](https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target) | **Optional**: <ul><li>`toxic_label="hate"` (default)</li><li> `display_name="display name"`</li></ul> |
| `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` <ul><li>A natural language inference model. </li><li>Use it for zero-shot classification by user-provided topics.</li><li> List candidate topics as `labels`. You can provide one or several topics. </li><li> You can set a classification threshold: if the predicted probability is below, an "unknown" label will be assigned. </li><li> Returns a label. </li></ul> **Example use**: <br>`HuggingFaceModel(model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli", params={"labels": ["HR", "finance"], "threshold":0.5}, display_name="Topic")` <br><br> **Source**: [HuggingFace Model](https://huggingface.co/MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli) | **Required**: <ul><li>`params={"labels": ["label"]}`</li></ul> **Optional**:<ul><li> `params={"score_threshold": 0.7}` (default: 0.5)</li><li> `display_name="display name"`</li></ul> |
| `openai-community/roberta-base-openai-detector` <ul><li> Predicts if a text is Real or Fake (generated by a GPT-2 model). </li><li> You can set a classification threshold: if the predicted probability is below, an "unknown" label will be assigned. </li><li> Note that it is not usable as a detector for more advanced models like ChatGPT.  </li><li> Returns a label. </li></ul>  **Example use**:<br> `HuggingFaceModel(model="openai-community/roberta-base-openai-detector", params={"score_threshold": 0.7})` <br><br> **Source**: [HuggingFace Model](https://huggingface.co/openai-community/roberta-base-openai-detector) | **Optional**:<ul><li>`params={"score_threshold": 0.7}` (default: 0.5)</li><li> `display_name="display name"`</li></ul> |

This list is not exhaustive, and the Descriptor may support other models published on Hugging Face. The implemented interface generally works for models that:
* Output a single number (e.g., predicted score for a label) or a label, **not** an array of values.
* Can process raw text input directly.
* Name labels using `label` or `labels` fields.
* Use methods named `predict` or `predict_proba` for scoring.

However, since each model is implemented differently, we cannot provide a complete list of models with a compatible interface. We suggest testing the implementation on your own using trial and error. If you discover useful models, feel free to share them with the community in Discord. You can also open an issue on GitHub to request support for a specific model.
