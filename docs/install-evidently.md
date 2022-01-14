# Install Evidently

## Installing from PyPI

### MAC OS and Linux

Evidently is available as a PyPI package.&#x20;

To install it using the pip package manager, run:

```bash
$ pip install evidently
```

The tool helps build interactive reports in a Jupyter notebook or as a separate HTML file, and generate JSON profiles.&#x20;

If you only want to generate **interactive reports as HTML files or JSON profiles**, the installation is now complete.

To display dashboards **in a Jupyter notebook**, we use jupyter nbextension. If you want to see reports inside a Jupyter notebook, then after installing `evidently` you should run the **two following commands** in the terminal from the Evidently directory.

To install jupyter nbextension, run:

```
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```

To enable it, run:

```
$ jupyter nbextension enable evidently --py --sys-prefix
```

That's it!

{% hint style="info" %}
**Note**: a single run after the installation is enough. There is no need to repeat the last two commands every time.
{% endhint %}

{% hint style="info" %}
**Note**: if you use **Jupyter Lab**, you may experience difficulties with exploring reports inside a Jupyter notebook. However, the report generation in a separate HTML file will work correctly.
{% endhint %}

#### Google Colab, Kaggle Kernel, Deepnote

You can run `evidently` in [Google Colab](https://colab.research.google.com), [Kaggle Notebook](https://www.kaggle.com/code) and [Deepnote](https://deepnote.com).

To install `evidently`, run the following command in the notebook cell:

```
!pip install evidently
```

There is no need to enable nbextension for this case. `Evidently` uses an alternative way to display visuals in the hosted notebooks.

### Windows

Evidently is available as a PyPI package.&#x20;

To install it using the pip package manager, run:

```bash
$ pip install evidently
```

The tool helps build interactive reports in a Jupyter notebook or as a separate HTML file, and generate JSON profiles.&#x20;

Unfortunately, building reports inside a **Jupyter notebook** is **not yet possible** for Windows. The reason is Windows requires administrator privileges to create symlink. In later versions, we will address this issue.



###
