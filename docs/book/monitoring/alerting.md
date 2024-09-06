---
description: Get notifications in Slack or email. 
---   

{% hint style="success" %} 
Built-in alerting is a Pro feature available in the Evidently Cloud and Enterprise. 
{% endhint %}

To enable alerts, open the Project and navigate to the "Alerts" section in the left menu. You must set:
* A notification channel.
* An alert condition. 

# Notification channels

You can choose between the following options:
* **Email**. Add email addresses to send alerts to. 
* **Slack**. Add a Slack webhook. 
* **Discord**. Add a Discord webhook.

# Alert conditions

## Failed tests

If you use Test Suites, you can tie alerting to the failed Tests in a Test Suite. Toggle this option on the Alerts page. Evidently will set an alert to the defined channel if any of the Tests fail.

{% hint style="info" %} 
**How to avoid alert fatigue?** When you create a Test Suite, you can [mark certain conditions as Warnings](../tests-and-reports/custom-test-suite.md) using the `is_critical` parameter. Set is `False` for non-critical checks to avoid triggering alerts.
{% endhint %}

## Custom conditions 

You can also set alerts on individual Metric values for both Reports and Test Suites. For example, you can generate Alerts when the share of drifting features is above a certain threshold. 

Click on the plus sign below the “Add new Metric alert” and follow the prompts to set an alert condition. 

![](../.gitbook/assets/cloud/alerts.png)
