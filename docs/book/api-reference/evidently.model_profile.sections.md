# evidently.model_profile.sections package

## Submodules

## evidently.model_profile.sections.base_profile_section module


### _class_ evidently.model_profile.sections.base_profile_section.ProfileSection()
Bases: [`PipelineStage`](api-reference/evidently.pipeline.md#evidently.pipeline.stage.PipelineStage)


#### _abstract_ analyzers()

#### _abstract_ calculate(reference_data: DataFrame, current_data: Optional[DataFrame], column_mapping: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), analyzers_results: Dict[Type[Analyzer], Any])

#### _abstract_ get_results()

#### _abstract_ part_id()
## evidently.model_profile.sections.cat_target_drift_profile_section module


### _class_ evidently.model_profile.sections.cat_target_drift_profile_section.CatTargetDriftProfileSection()
Bases: `ProfileSection`


#### analyzers()

#### calculate(reference_data, current_data, column_mapping, analyzers_results)

#### get_results()

#### part_id()
## evidently.model_profile.sections.classification_performance_profile_section module


### _class_ evidently.model_profile.sections.classification_performance_profile_section.ClassificationPerformanceProfileSection()
Bases: `ProfileSection`


#### analyzers()

#### calculate(reference_data, current_data, column_mapping, analyzers_results)

#### get_results()

#### part_id()
## evidently.model_profile.sections.data_drift_profile_section module


### _class_ evidently.model_profile.sections.data_drift_profile_section.DataDriftProfileSection()
Bases: `ProfileSection`


#### analyzers()

#### calculate(reference_data, current_data, column_mapping, analyzers_results)

#### get_results()

#### part_id()
## evidently.model_profile.sections.data_quality_profile_section module


### _class_ evidently.model_profile.sections.data_quality_profile_section.DataQualityProfileSection()
Bases: `ProfileSection`


#### analyzers()

#### calculate(reference_data, current_data, column_mapping, analyzers_results)

#### get_results()

#### part_id()
## evidently.model_profile.sections.num_target_drift_profile_section module


### _class_ evidently.model_profile.sections.num_target_drift_profile_section.NumTargetDriftProfileSection()
Bases: `ProfileSection`


#### analyzers()

#### calculate(reference_data, current_data, column_mapping, analyzers_results)

#### get_results()

#### part_id()
## evidently.model_profile.sections.prob_classification_performance_profile_section module


### _class_ evidently.model_profile.sections.prob_classification_performance_profile_section.ProbClassificationPerformanceProfileSection()
Bases: `ProfileSection`


#### analyzers()

#### calculate(reference_data, current_data, column_mapping, analyzers_results)

#### get_results()

#### part_id()
## evidently.model_profile.sections.regression_performance_profile_section module


### _class_ evidently.model_profile.sections.regression_performance_profile_section.RegressionPerformanceProfileSection()
Bases: `ProfileSection`


#### analyzers()

#### calculate(reference_data, current_data, column_mapping, analyzers_results)

#### get_results()

#### part_id()
## Module contents
