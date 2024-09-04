---
description: How to set up Evidently Cloud account.
---

# 1. Create an Account

If not yet, [sign up for a free Evidently Cloud account](https://app.evidently.cloud/signup). 

# 2. Create an Organization

After logging in, create an **Organization** and name it.

# 3. Create a Team 

Go to the **Teams** icon in the left menu, create a Team, and name it. ([Team page](https://app.evidently.cloud/teams)).

{% hint style="info" %}
**Do I always need a Team?** Yes. Every Project must be within a Team. Teams act as "folders" to organize your work, and you can create multiple Teams. If you work alone, simply create a Team without external users. 
{% endhint %}

# 4. Connect from Python

You will need an access token to interact with Evidently Cloud from your Python environment.

{% hint style="info" %}
**Do I always need this?** No, you only for data uploads or evaluations in Python. You can view data, edit dashboards, upload CSVs and run no-code evaluations without the token.
{% endhint %}

## Get a Token

Click the **Key** icon in the left menu to open the ([Token page](https://app.evidently.cloud/token)). Generate and save the token securely. 

## Install Evidently

To connect to the Evidently Cloud from Python, first [install the Evidently Python library](install-evidently.md).

```python
pip install evidently
```

## Connect

Import the cloud workspace and pass your API token to connect: 

```python
from evidently.ui.workspace.cloud import CloudWorkspace

ws = CloudWorkspace(
token="YOUR_TOKEN_HERE",
url="https://app.evidently.cloud")
```

Now, you are all set to start using Evidently Cloud! Choose your [next step](../get-started/quickstart-cloud.md).
