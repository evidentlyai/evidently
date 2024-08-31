---
description: How to create and evaluate an LLM judge. 
---

In this tutorial, we'll show you how to build an evaluator for a LLM system's outputs using another LLM as the judge. This lets you automatically assess the quality of your system's responses based on your custom criteria.

We'll explore two ways to use an LLM as a judge:
* **Reference-based**: Compare new responses against a reference. This is for regression testing workflows or whenever you have a "ground truth" or approved responses to compare against.
* **Open-ended**: Evaluate responses based on custom criteria, which helps evaluate new outputs when there's no reference available.
By the end, you'll know how to create custom LLM judges and apply them to your data. Our primary focus will be showing how to develop and tune the evaluator, which you can then apply in different contexts, like regression testing or prompt comparison.

# Tutorial scope

Here's what we'll do:
* **Create an evaluation dataset**. We'll create a toy Q&A dataset with two responses to each question. We'll add manual labels based on the criteria we want the LLM evaluator to follow later.
* **Create and run an LLM as a judge**. We'll design an LLM evaluator prompt to determine whether the new response is correct compared to the reference. 
* **Evaluate the judge**. Compare the LLM judge's evaluations with manual labels to see if they meet the expectations or need tweaking.
We'll start with the reference-based evaluator, which is more complex because it requires passing two columns to the prompt. Then, we'll create a simpler judge focused on verbosity.

To complete the tutorial, you will need:
* Basic Python knowledge. 
* An OpenAI API key to use for LLM evaluator.

To complete the tutorial, use the provided code snippets or run a sample notebook.

Jupyter notebook:
{% embed url="https://github.com/evidentlyai/community-examples/blob/main/tutorials/LLM_as_a_judge_tutorial.ipynb" %}

Or click to [open in Colab](https://colab.research.google.com/github/evidentlyai/community-examples/blob/main/tutorials/LLM_as_a_judge_tutorial.ipynb).

We recommend running this tutorial in Jupyter Notebook or Google Colab to render rich HTML objects with summary results directly in a notebook cell.

We will work with a toy dataset, which you can replace with your production data.

# 
