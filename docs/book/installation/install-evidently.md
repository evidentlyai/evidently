Looking for old Evidently Dashboards? Read the [migration guide](../support/migration.md).

# MAC OS and Linux

`Evidently` is available as a PyPI package. To install it using the **pip package manager**, run:

```bash
$ pip install evidently
```

To install `evidently` using **conda installer**, run:

```sh
conda install -c conda-forge evidently
```

To display dashboards **in a Jupyter notebook**, `evidently` uses `jupyter nbextension`. To enable it, run the **two following commands** in the terminal from the Evidently directory after installing `evidently`. 

To install `jupyter nbextension`, run:

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
**Note**: if you **use other notebook environments, e.g. Jupyter Lab**, Evidently might work differently. See more details below. 
{% endhint %}

# Cloud notebooks

## Google Colab

You can run `evidently` in Google Colab. 

To install `evidently`, run the following command in the notebook cell:

```
!pip install evidently
```
There is no need to enable nbextension for this case. `Evidently` uses an alternative way to display visuals.

## Other cloud notebooks

You can run `evidently` in Kaggle Notebook, Jupyter Lab, Deepnote, Databricks or other notebook environments. Note that **only Google Colab** is currently officially supported.

To install `evidently`, run the following command in the notebook cell:

```
!pip install evidently
```

There is no need to enable nbextension for this case. `Evidently` uses an alternative way to display visuals. 

{% hint style="info" %}
**Visualizations in cloud notebooks other than Colab**. When displaying Evidently Reports and Test Suites, you will need to **explicitly specify the inline show method**. Consult [this section](../integrations/notebook-environments.md) for help. If you face issues, you can get the output as a separate HTML file and view it in a browser.
{% endhint %}

# Windows

`Evidently` is available as a PyPI package.

To install it using the **pip package manager**, run:

```bash
$ pip install evidently
```

To install `evidently` using **conda installer**, run:

```sh
conda install -c conda-forge evidently
```

**Note**: Nbextension does not work on Windows. `Evidently` uses an alternative way to display visuals.

{% hint style="info" %}
**Visualizations on Windows**. When displaying Evidently Reports and Test Suites in Jupyter notebook, you will need to **explicitly specify the inline show method**. Consult [this section](../integrations/notebook-environments.md) for help. This is a new functionality with limited testing. If you face issues, you can get the output as a separate HTML file and view it in a browser.
{% endhint %}
