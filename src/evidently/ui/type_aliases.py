import datetime
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import TypeVar
from typing import Union

import uuid6

from evidently.base_metric import Metric
from evidently.pydantic_utils import UUID7
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestStatus

BlobID = str
UserID = UUID7
TeamID = UUID7
OrgID = UUID7
RoleID = int
ProjectID = UUID7
EntityID = UUID7
SnapshotID = UUID7
STR_UUID = Union[str, UUID7]
PanelID = UUID7
TabID = UUID7
DatasetID = UUID7
ZERO_UUID = uuid6.UUID(int=0, version=7)


class TestInfo(NamedTuple):
    status: TestStatus
    description: str


TestResultPoints = Dict[datetime.datetime, Dict[Test, TestInfo]]
PointType = TypeVar("PointType")
DataPointsAsType = List[Dict[Metric, List[Tuple[datetime.datetime, PointType]]]]
DataPoints = DataPointsAsType[float]
