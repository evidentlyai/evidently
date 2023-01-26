# Installing from PyPI

## MAC OS and Linux

Evidently is available as a PyPI package.

To install it using the pip package manager, run:

```bash
$ pip install evidently
```

To display dashboards **in a Jupyter notebook**, we use jupyter nbextension. If you want to display reports inside a Jupyter notebook, then after installing `evidently` you should run the **two following commands** in the terminal from the Evidently directory. 

To install jupyter nbextension, run:

```
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```

To enable it, run:

```
$ jupyter nbextension enable evidently --py --sys-prefix
```

That's it! A single run after the installation is enough. 

{% hint style="info" %}
**Note**: if you **do not install nbextension**, you can still use Evidently. You can get the outputs as JSON, Python dictionary, or generate standalone HTML files to view in the browser.
{% endhint %}

{% hint style="info" %}
**Note**: if you use **Jupyter Lab**, you may experience difficulties with exploring reports inside a Jupyter notebook. However, the report generation in a separate HTML file will work correctly.
{% endhint %}

## Hosted notebooks

You can run `evidently` in [Google Colab](https://colab.research.google.com), [Kaggle Notebook](https://www.kaggle.com/code), [Deepnote](https://deepnote.com) or Databricks notebooks.

To install `evidently`, run the following command in the notebook cell:

```
!pip install evidently
```

There is no need to enable nbextension for this case. `Evidently` uses an alternative way to display visuals in the hosted notebooks. Consult [this section](../integrations/notebook-environments.md) for help.

## Windows

Evidently is available as a PyPI package.

To install it using the pip package manager, run:

```bash
$ pip install evidently
```

**Note**: Nbextension does not work on Windows. If you want to generate visual reports in Jupyter notebook on Windows, you will need to use a different visulization method when calling the report. Consult [this section](../integrations/notebook-environments.md) for help. This is a new functionality with limited testing. If you face issues, you can get the output as a separate HTML file and view it in a browser.
