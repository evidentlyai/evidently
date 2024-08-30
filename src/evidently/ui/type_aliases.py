import datetime
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import TypeVar
from typing import Union

import uuid6

from evidently.base_metric import Metric
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestStatus

BlobID = str
UserID = uuid6.UUID
TeamID = uuid6.UUID
OrgID = uuid6.UUID
RoleID = int
ProjectID = uuid6.UUID
EntityID = uuid6.UUID
SnapshotID = uuid6.UUID
STR_UUID = Union[str, uuid6.UUID]
PanelID = uuid6.UUID
TabID = uuid6.UUID
DatasetID = uuid6.UUID
ZERO_UUID = uuid6.UUID(int=0, version=7)


class TestInfo(NamedTuple):
    status: TestStatus
    description: str


TestResultPoints = Dict[datetime.datetime, Dict[Test, TestInfo]]
PointType = TypeVar("PointType")
DataPointsAsType = List[Dict[Metric, List[Tuple[datetime.datetime, PointType]]]]
DataPoints = DataPointsAsType[float]
