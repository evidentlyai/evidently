---
description: How to set up Evidently Cloud account.
---

# Evidently Cloud Account 

## 1. Create an Account

If not already, [sign up for an Evidently Cloud account](https://app.evidently.cloud/signup). 

## 2. Create an Organization

Once you log in to Evidently Cloud for the first time, create an **Organization** and give it a name. 

## 3. Create a Team 

Click on the **Teams** icon on the left menu. Create a Team and give it a name.

{% hint style="info" %}
**Do I always need a Team?** Yes. Every Project must exist inside a Team. Teams help organize your work on different use cases and serve as Project "folders". You can create multiple Teams inside the Organization and add other users to the Teams. If you work alone, simply create a "Personal" team. 
{% endhint %}

# Access Token

You will need an access token to interact with Evidently Cloud from your Python environment using the Evidently Python library.

Click the **Key** icon in the left menu to open the ([Token page](https://app.evidently.cloud/token)). Generate and save the token securely. 

{% hint style="info" %}
**Do I always need a token?** No. You only need the token if you want to send data or interact with Evidently Cloud from your Python environment. You can also run the evaluations using the no-code interface, or interact with Projects created by other Team members in the Web UI.
{% endhint %}

Now, you are all set to start using Evidently Cloud! You can create your first Project and run an evaluation.
