---
description: Using Evidently in Colab and other notebook environments.
---

# Jupyter notebooks

You can generate the dashboards in **Jupyter notebooks**. 

{% hint style="info" %}
If you want to display the dashboards in Jupyter notebook, make sure you [installed](../installation/install-evidently.md) the Jupyter **nbextension**.
{% endhint %}

# Hosted notebooks

You can also use **Google Colab**, **Kaggle Kernel**, **Databricks** or **Deepnote** notebooks.  

To install `evidently` in these environments, run the following command in the notebook cell:

```
!pip install evidently
```

You should then follow the steps described in the User Guide to [../tests-and-reports/get-reports.md](generate reports) and [../tests-and-reports/run-tests.md](run test suites).

**Troubleshooting**: 

Sometimes, you might need to explicitly add an argument to display the report inline: 

```
iris_data_drift_report.show(mode='inline'). 
```

The `show()` method has the argument `mode` which can take the following options:

* **auto** - the default option. Ideally, you will not need to specify the value for `mode` and can use the default. But if it does not work (in case we failed to determine the environment automatically), consider setting the correct value explicitly.
* **nbextention** - to show the UI using nbextension. Use this option to display dashboards in Jupyter notebooks (it should work automatically).
* **inline** - to insert the UI directly into the cell. Use this option for Google Colab, Kaggle Kernels, and Deepnote. 


## Jupyter Lab

If you use **Jupyter Lab**, you won't be able to explore the reports inside a Jupyter notebook. However, the report generation in a separate HTML file will work correctly.
