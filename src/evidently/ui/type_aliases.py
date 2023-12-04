import datetime
import uuid
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from evidently.base_metric import Metric

BlobID = str
UserID = uuid.UUID
TeamID = uuid.UUID
OrgID = uuid.UUID
ProjectID = uuid.UUID
SnapshotID = uuid.UUID
STR_UUID = Union[str, uuid.UUID]

DataPoints = List[Dict[Metric, List[Tuple[datetime.datetime, Any]]]]
