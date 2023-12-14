from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from fastapi import Depends
from fastapi import FastAPI
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_param_sub_dependant
from fastapi.routing import APIRoute

from evidently.ui.config import SecurityConfig
from evidently.ui.type_aliases import OrgID
from evidently.ui.type_aliases import UserID


async def get_user_id() -> UserID:
    pass


async def get_org_id() -> Optional[OrgID]:
    return None


async def is_authorized() -> bool:
    return True


_security_deps: Dict[Callable, List[Tuple[Dependant, int]]] = {}


def _collect_security_dependencies(
    dependant: Dependant, dependency_callable: Callable
) -> Iterable[Tuple[Dependant, int]]:
    for i, dep in enumerate(dependant.dependencies):
        if dep.call == dependency_callable:
            yield dependant, i
            continue
        yield from _collect_security_dependencies(dep, dependency_callable)


def collect_security_dependencies(app: FastAPI, dependency_callable: Callable):
    result: List[Tuple[Dependant, int]] = []
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        result.extend(_collect_security_dependencies(route.dependant, dependency_callable))
    _security_deps[dependency_callable] = result


def replace_dependency(app: FastAPI, dependency: Callable, new_dependency: Callable):
    if dependency not in _security_deps:
        collect_security_dependencies(app, dependency)

    for dep, i in _security_deps[dependency]:
        old_dep = dep.dependencies[i]
        dep.dependencies[i] = get_param_sub_dependant(
            param_name=old_dep.name or "",
            depends=Depends(new_dependency, use_cache=old_dep.use_cache),
            path=old_dep.path or "",
            security_scopes=old_dep.security_scopes,
        )


def setup_security(app: FastAPI, security: SecurityConfig):
    replace_dependency(app, get_user_id, security.get_user_id_dependency())
    replace_dependency(app, get_org_id, security.get_org_id_dependency())
    replace_dependency(app, is_authorized, security.get_is_authorized_dependency())
