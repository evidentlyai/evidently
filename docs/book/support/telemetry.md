# Telemetry

### **What is Telemetry?**

Telemetry refers to the collection of usage data. We do it to understand how many users we have, how they interact with our tool and help us improve it.&#x20;

Below we describe what is collected and how to opt-out.

### **What data is collected?**

Telemetry is collected in Evidently starting from **version 0.1.21.dev0**

Our telemetry is intentionally limited in scope. We **DO NOT collect any sensitive information** and never see the data, its structure, or column names. &#x20;

We **only** collect telemetry when you use the tool **using the command-line interface**. We DO NOT collect any telemetry when you use the tool as a library, for instance, run in a Jupyter notebook or in a Python script.

Telemetry data is sent to us when you run Evidently to generate HTML reports or JSON profiles.&#x20;

Here is an example of the data that is shared. It includes:

* basic information about the environment (Python version, operating system, etc.)
* usage data that shows what report or profile was generated

```
{
    "environment": {
      "os": "macOS-11.4-x86_64-i386-64bit",
      "python": {
        "version": "3.8.2",
        "interpreter": "CPython",
        "conda": false,
        "venv": true
      }
    },
    "evidently": {
      "version": "0.1.19.dev0"
    },
    "usage": {
      "type": "profile",
      "parts": [
        "data_drift"
      ],
      "tabs": [],
      "sampling": {
        "reference": {
          "type": "none",
          "ratio": "0.1",
          "n": "1",
          "random_seed": null
        },
        "current": {
          "type": "nth",
          "ratio": "0.1",
          "n": "2",
          "random_seed": null
        }
      }
    }
  }
```

### **Can I opt-out?**

You can opt-out from telemetry collection by setting the  environment variable EVIDENTLY\_DISABLE\_TELEMETRY to 1, e.g.:

```
$export EVIDENTLY_DISABLE_TELEMETRY=1
```

Here is an example of how to use Evidently from CLI without telemetry:

```
EVIDENTLY_DISABLE_TELEMETRY=1 python evidently calculate profile
 --reference ~/Downloads/Bike-Sharing-Dataset/day.csv 
 --current ~/Downloads/Bike-Sharing-Dataset/day.csv 
 --output_path . --config config.json
```

You can also set the EVIDENTLY\_DISABLE\_TELEMETRY environment variable globally. This way, you won’t need to set it up for every run:

**Windows:**

```
` SETX EVIDENTLY_DISABLE_TELEMETRY 1`
```

**Linux:**

```
`echo "export EVIDENTLY_DISABLE_TELEMETRY=1" >> ~/.profile`
```

**MacOS:**

```
`launchctl setenv EVIDENTLY_DISABLE_TELEMETRY 1`
```

### **Should I opt out?**

Being open-source, we have no visibility into the tool usage unless someone actively reaches out to us or opens a GitHub issue.&#x20;

We’d be grateful if you keep the telemetry on since it helps us answer questions like:

* How many people are actively using the tool?
* Do you use it to generate JSON profiles, reports, or both?
* What are the more popular types of reports?
* What is the environment you run Evidently in?

It helps us prioritize the development of new features and make sure we test the performance in the most popular environments.

**We understand that you might still prefer not to share any telemetry data, and we respect this wish. Follow the steps above to disable the data collection.** 
