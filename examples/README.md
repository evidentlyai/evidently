# Examples

This folder contains examples of how to use Evidently to evaluate, test, and monitor different types of AI systems: agentic workflows, LLM applications, and traditional ML models.

## Start here

If you are new to Evidently, start with these three top-level tutorials:

**1. [Agentic Systems: Tracing and Evaluation](./agentic_systems_tracing.ipynb)**
Learn how to trace multi-step agentic workflows, inspect intermediate steps, and evaluate agent behavior end to end.

**2. [LLM Validation: Input and Output Quality](./llm_input_output_validation.ipynb)**
Learn how to evaluate the quality of LLM application inputs and outputs, inspect results, and build validation workflows for LLM-powered systems.

**3. [Classic ML Validation: Data Quality and Drift](./classic_ml_validation.ipynb)**
Learn how to validate datasets for traditional ML workflows, detect data quality issues, and analyze data drift between reference and current data.

## Folder structure

**[`cookbook`](./cookbook/)**
Short, focused examples that demonstrate specific Evidently functionality or implementation patterns.

**[`tutorials`](./tutorials/)**
Longer end-to-end examples that combine multiple Evidently capabilities for realistic use cases.

**[`service`](./service/)**
An example of how to run and serve the full Evidently system locally.

**[`grafana`](./grafana/)**
Examples of using Evidently with Grafana dashboards.
These examples show how to export Evidently metrics and visualize them in Grafana using a local setup.

**[`datasets`](./datasets/)**
Sample datasets used in the examples.

## How to use these examples

- Start with the three top-level tutorials for the quickest introduction.
- Use the `cookbook` for focused implementation snippets and feature-specific examples.
- Explore `tutorials` for more complete workflows and extended use cases.
- Use `service` if you want to run Evidently locally as a full system.
- Use `grafana` if you want to visualize Evidently metrics in external dashboards.

## Notes

Some examples may depend on local datasets, external services, or optional Python dependencies. Please check the instructions inside each notebook or folder README for setup details.