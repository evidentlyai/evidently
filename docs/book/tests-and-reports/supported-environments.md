---
description: Using Evidently in Colab and other notebook environments.
---

You can generate the dashboards in **Jupyter notebooks**. 

{% hint style="info" %}
If you want to display the dashboards in Jupyter notebook, make sure you [installed](../get-started/install-evidently.md) the Jupyter **nbextension**.
{% endhint %}

You can also use **Google Colab**, **Kaggle Kernel**, or **Deepnote**.  

To install `evidently` in these environments, run the following command in the notebook cell:

```
!pip install evidently
```

If you use **Jupyter Lab**, you won't be able to explore the reports inside a Jupyter notebook. However, the report generation in a separate HTML file will work correctly.
