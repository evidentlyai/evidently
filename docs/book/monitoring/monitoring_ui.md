---
description: How to work with the monitoring UI. 
---   

The Monitoring UI lets you visualize metrics over time and search and view individual Reports and Test Suites that you logged as snapshots. 

## Launching the UI

`Snapshots` are stored on the same machine where the UI runs. The Evidently service directly interfaces with the local filesystem.

In the simple scenario, both computation and storage of snapshots happen locally. In a more complex scenario with a remote workspace, you can compute the snapshots locally and send them to a remote server where both snapshots are stored, and the UI runs.
 
To launch the Evidently service, run the following command in the Terminal.

**Option 1**. If you log snapshots to a local workspace directory, you run evidently ui over it. Run the following command from the directory where the workspace folder is located.

```
evidently ui
```

**Option 2**. If you have your project in a different workspace, specify the path:

```
evidently ui --workspace . /workspace 
```

**Option 3**. If you have your project in a specified workspace and run the UI service at the specific port (if the default port 8000 is occupied).  

```
evidently ui --workspace ./workspace --port 8080
```

To view the Evidently interface, go to URL http://localhost:8000 or a different specified port in your web browser.

# Working with the UI

![](../.gitbook/assets/main/evidently_ml_monitoring_main.png)

The UI contains the following key features:
* Allows browsing through different projects.
* Displays the defined dashboard panels for each project. 
* Allows exploring visualizations for different periods within a project.
* Allows viewing and downloading individual Reports and Test Suites in JSON and HTML format.

