import datetime
import uuid
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from evidently.base_metric import Metric
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestStatus

BlobID = str
UserID = uuid.UUID
TeamID = uuid.UUID
OrgID = uuid.UUID
RoleID = int
ProjectID = uuid.UUID
SnapshotID = uuid.UUID
STR_UUID = Union[str, uuid.UUID]
ZERO_UUID = uuid.UUID(int=0)

DataPoints = List[Dict[Metric, List[Tuple[datetime.datetime, Any]]]]
TestResultPoints = Dict[datetime.datetime, Dict[Test, TestStatus]]
