# F.A.Q.

### **I found a bug. Where to report it?**

Check if there is already an open issue on the topic on [GitHub](https://github.com/evidentlyai/evidently). If there is none, create a new issue.&#x20;

### **I have a question about the tool. Where to ask it?**

Open an issue on [GitHub](https://github.com/evidentlyai/evidently), or ask in our [Discord community](https://discord.gg/xZjKRaNp8b). &#x20;

### **Can you add {insert a plot type} to one of your reports?**

We probably can! However, we might choose not to, since we try to have a good-enough default setup without unnecessarily increasing the size of the report. That is a delicate balance!&#x20;

That said, please do file an issue on [GitHub](https://github.com/evidentlyai/evidently) with your request. We already made some additions to our reports, and we plan to add the ability of custom configuration in the future. Your feedback will greatly help us to understand the most popular use cases.&#x20;

### **Can I export the report to display it elsewhere / integrate it into the prediction pipeline?**

You can export the report summary as a JSON profile and integrate it with external tools. This functionality is available both for Jupyter notebooks and in Terminal. See [Quick Start](../get-started/quick-start.md) guide or browse through [Tutorials](../step-by-step-guides/tutorials/) to see the implementations.&#x20;

### **The report size is too large. Can I decrease it?**

Unfortunately, not yet.&#x20;

It happens because we store all the data inside the HTML file itself. We will address this in the later versions of the tool when it will be available as a service.&#x20;

In the meantime, we suggest using some sampling strategy for your dataset, for instance, random sampling or stratified sampling.

### **Does it work for large datasets and distributed computation?**

If your dataset is too large, you can define a sampling strategy. See [Quick Start](../get-started/quick-start.md) guide to see the available options.&#x20;

We plan to add support for distributed computation in the later version.&#x20;

### **Do you have a Slack chat?**&#x20;

We have a [Discord community](https://discord.gg/xZjKRaNp8b)!

