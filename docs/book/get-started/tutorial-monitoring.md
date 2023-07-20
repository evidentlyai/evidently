In this tutorial, you'll learn how to get started with Evidently ML monitoring. You will launch a locally hosted ML monitoring dashboard to visualize the performance of a toy model.

![ML monitoring](../.gitbook/assets/main/evidently_ml_monitoring_main-min.png)

The steps below explain how to launch a pre-built demo.

**1. Create virtual environment**

This step is optional but highly recommended. Create a virtual environment and activate it.

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

**2. Install Evidently**

Evidently is available as a PyPi package. Run this command in the terminal to install Evidently locally:

```
pip install evidently
```

You can also install Evidently from Conda:
```
conda install -c conda-forge evidently
```

The rest of this guide assumes you are using Evidently locally.

**3. Run demo project**

To launch the Evidently service with the demo project, run: 

```
evidently ui --demo-project
```
 
**4. View the project**

To view the Evidently interface in your browse, go to **localhost:8000**.

You will see a pre-built demo project that visualizes the model quality and a few other metrics over 20 days. You can switch between tabs and view and download individual Reports and Test Suites. Each Report or Test Suite contains the information that was logged for a daily period. The monitoring dashboard aggregates this information and shows how metrics change over time.

{% hint style="info" %}
**What is a Test Suite and a Report?** If you are new to Evidently, go through the [Get Started tutorial](tutorial.md) for Tests and Reports.
{% endhint %}
