### **I found a bug. Where to report it?**

Check if there is already an open issue on the topic on [GitHub](https://github.com/evidentlyai/evidently). If there is none, create a new issue.

### **I have a question about the tool. Where to ask it?**

Open an issue on [GitHub](https://github.com/evidentlyai/evidently), or ask in our [Discord community](https://discord.gg/xZjKRaNp8b).

### **Can you add {insert a plot type} to one of your Reports or Test Suites?**

We probably can! However, we might choose not to since we try to have a good-enough and maintainable set of Metrics and Tests. That is a delicate balance!

If you want to change the Report or Test Suite composition, you can add custom metric on your own. Explore the [Customization section](../customization) for more details.

### **Can I export the report to display it elsewhere / integrate it into the prediction pipeline?**

You can self-host an Evidently ML Monitoring dashboard to track the model performance over time. Explore the [Monitoring](../monitoring/monitoring_overview.md) section for details. You can also export the report summary as a JSON or Python dictionary and integrate it with external tools. Refer to the [Integration section](../integrations) to see examples.

### **The HTML report size is too large. Can I decrease it?**

You might be using an older Evidently version. Starting from version 0.3.2, all visualizations in Reports are aggregated by default. This helps reduce the size of the resulting HTML. You can choose to include [raw data](../customization/report-data-aggregation.md) if you prefer this. In this case, you might want to use a sampling strategy for your dataset, for instance, random sampling or stratified sampling.

### **Does it work for large datasets and distributed computation?**

If your dataset is too large, you can define a sampling strategy. 

We plan to add support for distributed computation in the later version.

### **Do you have a Slack chat?**

We have a [Discord community](https://discord.gg/xZjKRaNp8b)!

