import glob
import os
import time
from importlib import import_module
from inspect import isabstract
from typing import Dict, Union
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type

import dataclasses
import gspread
from gspread import Worksheet

import evidently
from evidently.base_metric import Metric
from evidently.core import IncludeTags

KEY_FIELDS = ["metric_group", "metric_id", "field_path"]
UPDATE_FIELDS = ["field_type", "tags"]
EXCLUDE_TAGS = [IncludeTags.Render, IncludeTags.Reference, IncludeTags.Extra, IncludeTags.TypeField, IncludeTags.Parameter]
TAG_COLUMNS = ["current", "reference", "extra", "parameter"]


@dataclasses.dataclass
class MetricField:
    metric_group: str
    metric_id: str
    field_path: str
    field_type: str
    tags: str

    additional_data: Dict[str, str]

    @classmethod
    def from_metric(cls, metric_type: Type[Metric]) -> List["MetricField"]:
        result = []
        for path, tags in metric_type.fields.list_nested_fields_with_tags():
            result.append(MetricField(
                metric_group=metric_type.get_group(),
                metric_id=metric_type.get_id(),
                field_path=path,
                field_type="",
                tags=",".join(sorted(v.value for v in tags)),
                additional_data={}
            ))
        return result

    def __hash__(self):
        return hash(tuple(getattr(self, f) for f in KEY_FIELDS))

    def __eq__(self, other):
        if not isinstance(other, MetricField):
            return False
        return all(getattr(self, f) == getattr(other, f) for f in KEY_FIELDS)

    def get(self, column):
        return getattr(self, column, self.additional_data.get(column))

    def upload(self, ws: Worksheet, header: List[str]):
        print(f"new {self}")
        values = [self.get(c) for c in header]
        ws.append_row(values)

    def check_and_update(self, ws: Worksheet, header: List[str], existing: "MetricField", row: int):
        changed = False
        for f in UPDATE_FIELDS:
            value = getattr(self, f)
            if value != getattr(existing, f):
                print(f"updating {f} with new value {value}")
                changed = True
                ws.update_cell(row + 1, header.index(f) + 1, value)
                try:
                    setattr(existing, f, value)
                except AttributeError:
                    print(existing, f, value, self)
                    raise
                time.sleep(1)
        return changed

    @property
    def keep(self) -> Optional[bool]:
        if self.additional_data.get("keep"):
            return self.additional_data["keep"] == "1"
        if self.additional_data.get("drop"):
            return self.additional_data["drop"] == "0"
        return None

    @property
    def drop(self) -> Optional[bool]:
        if self.additional_data.get("drop"):
            return self.additional_data["drop"] == "1"
        if self.additional_data.get("keep"):
            return self.additional_data["keep"] == "0"
        return None

    @property
    def tags_parsed(self):
        if self.tags == "":
            return []
        return [IncludeTags(v) for v in self.tags.split(",")]

    def has_tag(self, tag: Union[str, IncludeTags]):
        if isinstance(tag, str):
            return tag in self.tags
        return tag in self.tags_parsed

    def tag_column_set(self, tag: str):
        return self.additional_data.get(tag) == "1"

    def repr(self):
        return f"{self.metric_group}.{self.metric_id}.{self.field_path} [{self.tags}]"


def all_metrics() -> Set[Type[Metric]]:
    path = os.path.dirname(evidently.__file__)

    metrics = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = "evidently." + mod_path.replace("/", ".").replace("\\", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not Metric and issubclass(value, Metric):
                metrics.add(value)
    return metrics


def collect_metric_fields() -> List[MetricField]:
    print("loading code metrics")
    metric_fields = []
    for metric_type in all_metrics():
        if isabstract(metric_type):
            continue
        metric_field = MetricField.from_metric(metric_type)
        metric_fields.extend(metric_field)
    print("loading code metrics: done")
    return metric_fields


def parse_row(header: List[str], row: List[str]) -> MetricField:
    data = dict(zip(header, row))

    fields = ("metric_group", "metric_id", "field_path", "field_type", "tags")
    additional_data = {k: v for k, v in data.items() if k not in fields}
    data = {k: v for k, v in data.items() if k in fields}
    return MetricField(
        **data,
        additional_data=additional_data
    )


def parse_worksheet(worksheet: Worksheet) -> Tuple[List[str], List[MetricField]]:
    print("parsing worksheet")
    result = []
    header = None
    for row in worksheet.get_all_values():
        if header is None:
            header = row
            continue
        result.append(parse_row(header, row))
    print("parsing worksheet: done")
    return header, result


def check_additional(mf: MetricField) -> float:
    tags = mf.tags_parsed
    # print(mf.keep, mf.drop, tags,)
    if mf.keep:
        # print(mf)
        if any(t in EXCLUDE_TAGS for t in tags):
            print(mf.repr(), "should be kept but is dropped")
            return 0

    if mf.drop:
        # print(mf)
        if all(t not in EXCLUDE_TAGS for t in tags):
            print(mf.repr(), "should be dropped but is kept")
            return 0

    for tag in TAG_COLUMNS:
        if mf.tag_column_set(tag) and not mf.has_tag(tag) or mf.has_tag(tag) and not mf.tag_column_set(tag):
            print(mf.repr(), f"has incosistent tags: {mf.tags} vs {mf.additional_data}")
            return 0.5

    if mf.keep is None:
        return -1
    return 1


COLORING = True


def recolor_row(check_result: float, row_num: int):
    if not COLORING:
        return
    color_map = {
        0: {
            "red": 0.9,
            "green": 0.7,
            "blue": 0.7
        },
        1: {
            "red": 0.7,
            "green": 0.9,
            "blue": 0.7
        },
        0.5: {
            "red": 0.6,
            "green": 0.9,
            "blue": 0.8
        },
        -1: {
            "red": 1,
            "green": 1,
            "blue": 1
        },
    }
    return {"range": str(row_num + 1), "format": {"backgroundColor": color_map[check_result]}}


def open_spreadsheet(name="Metric Fields v1"):
    # gc = gspread.authorize(credentials)
    # gc = gspread.oauth(credentials_filename="credentials.json")
    gc = gspread.service_account("credentials.json")

    sh = gc.open(name)

    ws = sh.sheet1
    header, doc_mf = parse_worksheet(ws)
    code_mf = collect_metric_fields()

    # wtf am i doin
    doc_mf_dict = {mf: (mf, i + 1) for i, mf in enumerate(doc_mf)}

    changed = set()

    to_upload = []
    for mf in code_mf:
        if mf in doc_mf_dict:
            # print(f"existing {doc_mf_dict[mf]}")
            if mf.check_and_update(ws, header, *doc_mf_dict[mf]):
                changed.add(mf)
            continue
        to_upload.append(mf)

    for i, mf in enumerate(to_upload):
        mf.upload(ws, header)
        time.sleep(1)

    format_batch = []
    for mf, row_num in doc_mf_dict.values():
        check_result = check_additional(mf)

        recolor = recolor_row(check_result, row_num)
        if recolor is not None:
            format_batch.append(recolor)
    ws.batch_format(format_batch)


def main():
    # pprint(collect_metric_fields())
    open_spreadsheet()

    # from evidently.metrics.data_drift.text_descriptors_drift_metric import TextDescriptorsDriftMetricResults
    # pprint(TextDescriptorsDriftMetricResults.fields.drift_by_columns.list_nested_fields_with_tags())


if __name__ == '__main__':
    main()
