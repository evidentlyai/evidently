# Project Template Directory

The Project Template Directory is a template for a new project you may want to add to `evidently-streamlit` app to visualize model metrics and reports.


### Directory structure

Expected structure of the monitoring project directory 
```yaml
project-name/
    reports/                                
        period/                       # add .html reports here! 
```

Example: 
```yaml
project-name/
    reports/                                
        2011-01-29_2011-02-04/        # reports for a period
            target_drift.html         # .html report to visualize
            model_performance.html
            ...
```

