# evidently.runner package

## Submodules

## evidently.runner.dashboard_runner module


### _class_ evidently.runner.dashboard_runner.DashboardRunner(options: DashboardRunnerOptions)
Bases: `Runner`


#### run()

### _class_ evidently.runner.dashboard_runner.DashboardRunnerOptions(reference_data_path: str, reference_data_options: evidently.runner.loader.DataOptions, reference_data_sampling: Optional[evidently.runner.loader.SamplingOptions], current_data_path: Optional[str], current_data_options: Optional[evidently.runner.loader.DataOptions], current_data_sampling: Optional[evidently.runner.loader.SamplingOptions], column_mapping: [evidently.pipeline.column_mapping.ColumnMapping](./evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), options: List[object], output_path: str, dashboard_tabs: Dict[str, Dict[str, object]])
Bases: `RunnerOptions`


#### dashboard_tabs(_: Dict[str, Dict[str, object]_ )
## evidently.runner.loader module


### _class_ evidently.runner.loader.DataLoader()
Bases: `object`


#### load(filename: str, data_options: DataOptions, sampling_options: Optional[SamplingOptions] = None)

### _class_ evidently.runner.loader.DataOptions(date_column: str = 'datetime', separator=',', header=True, column_names=None)
Bases: `object`


#### column_names(_: Optional[List[str]_ )

#### date_column(_: st_ )

#### header(_: boo_ )

#### separator(_: st_ )

### _class_ evidently.runner.loader.RandomizedSkipRows(ratio: float, random_seed: int)
Bases: `object`


#### skiprows(row_index: int)

### _class_ evidently.runner.loader.SamplingOptions(type: str = 'none', random_seed: int = 1, ratio: float = 1.0, n: int = 1)
Bases: `object`


#### n(_: in_ _ = _ )

#### random_seed(_: in_ _ = _ )

#### ratio(_: floa_ _ = 1._ )

#### type(_: st_ _ = 'none_ )
## evidently.runner.profile_runner module


### _class_ evidently.runner.profile_runner.ProfileRunner(options: ProfileRunnerOptions)
Bases: `Runner`


#### run()

### _class_ evidently.runner.profile_runner.ProfileRunnerOptions(reference_data_path: str, reference_data_options: evidently.runner.loader.DataOptions, reference_data_sampling: Optional[evidently.runner.loader.SamplingOptions], current_data_path: Optional[str], current_data_options: Optional[evidently.runner.loader.DataOptions], current_data_sampling: Optional[evidently.runner.loader.SamplingOptions], column_mapping: [evidently.pipeline.column_mapping.ColumnMapping](./evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), options: List[object], output_path: str, profile_parts: Dict[str, Dict[str, str]], pretty_print: bool)
Bases: `RunnerOptions`


#### pretty_print(_: boo_ )

#### profile_parts(_: Dict[str, Dict[str, str]_ )
## evidently.runner.runner module


### _class_ evidently.runner.runner.Runner(options: RunnerOptions)
Bases: `object`


### _class_ evidently.runner.runner.RunnerOptions(reference_data_path: str, reference_data_options: evidently.runner.loader.DataOptions, reference_data_sampling: Optional[evidently.runner.loader.SamplingOptions], current_data_path: Optional[str], current_data_options: Optional[evidently.runner.loader.DataOptions], current_data_sampling: Optional[evidently.runner.loader.SamplingOptions], column_mapping: [evidently.pipeline.column_mapping.ColumnMapping](./evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping), options: List[object], output_path: str)
Bases: `object`


#### column_mapping(_: [ColumnMapping](./evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping_ )

#### current_data_options(_: Optional[DataOptions_ )

#### current_data_path(_: Optional[str_ )

#### current_data_sampling(_: Optional[SamplingOptions_ )

#### options(_: List[object_ )

#### output_path(_: st_ )

#### reference_data_options(_: DataOption_ )

#### reference_data_path(_: st_ )

#### reference_data_sampling(_: Optional[SamplingOptions_ )

### evidently.runner.runner.parse_options(raw_dict: Optional[Dict[str, Dict[str, object]]])
## Module contents
