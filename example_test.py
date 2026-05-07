import os
import sys

excludes = [
    "nyc_taxi_data_drift_dashboard_customization.py",
    "historical_drift_visualization.py",
    "mlflow_integration.py",
    "ibm_hr_attrition_model_validation.py",
    "bicycle_demand_monitoring_setup.py",
    "data_and_ml_monitoring_tutorial.py",
    "how_to_run_drift_report_for_text_encoders.py",
    "comparing_custom_statest_with_classic_distributions.py",
    "how_to_evaluate_llm_with_text_descriptors.py",
    "how_to_run_drift_report_for_text_data.py",  # too slow & torch version conflict?
    "llm_evaluation_tutorial.py",  # cloud usage
    "llm_tracing_tutorial.py",  # cloud usage
]

# Scripts that require OpenAI API key
llm_dependent_scripts = [
    "llm_providers.py",
    "guardrails.py",
    "prompt_optimization_bookings_example.py",
    "prompt_optimization_tweet_generation_example.py",
    "prompt_optimization_code_review_example.py",
    "prompt_registry.py",
    "datagen.py",
]

# Scripts that require local services (database, server, etc.)
service_dependent_scripts = [
    "tracing_with_service.py",
    "workspace_tutorial.py",
    "docker_s3_tutorial.py",
    "cloud_sdk.py",
    "future_dashboads.py",
    "descriptors.py",
    "upload_snapshots.py",
    "list_metrics.py",
    "metric_workbench.py",
]


if __name__ == "__main__":
    failed_scripts = []
    skipped_scripts = []
    
    # Check if OpenAI API key is available
    has_openai_key = bool(os.environ.get("OPENAI_API_KEY"))
    
    for entry, _, files in os.walk("example_scripts"):
        for file in sorted(files):
            if file.endswith(".py"):
                if file in excludes:
                    continue
                
                # Skip LLM-dependent scripts if API key is missing
                if file in llm_dependent_scripts:
                    if not has_openai_key:
                        print(f"⏭️  Skipping {file} (requires OPENAI_API_KEY)", file=sys.stderr)
                        skipped_scripts.append(file)
                        continue
                
                # Skip service-dependent scripts (they require external services)
                if file in service_dependent_scripts:
                    print(f"⏭️  Skipping {file} (requires external services)", file=sys.stderr)
                    skipped_scripts.append(file)
                    continue
                
                print(f"▶️  Running {file}...", file=sys.stderr)
                result = os.system(f"ipython example_scripts/{file}")
                if result != 0:
                    failed_scripts.append((file, result))

    if skipped_scripts:
        print(f"\n⏭️  Skipped {len(skipped_scripts)} scripts", file=sys.stderr)
        
    if failed_scripts:
        print(f"\n❌ Failed scripts:", file=sys.stderr)
        for fail, errcode in failed_scripts:
            print(f"Script {fail} failed with error code {errcode}", file=sys.stderr)
        sys.exit(len(failed_scripts))
    else:
        print(f"\n✅ All example scripts passed!", file=sys.stderr)
