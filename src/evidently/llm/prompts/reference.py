import contextlib
import contextvars
from typing import Optional
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import SecretStr
from evidently.legacy.options.base import Options
from evidently.legacy.options.option import Option
from evidently.sdk.prompts import PromptID
from evidently.sdk.prompts import PromptVersion
from evidently.sdk.prompts import PromptVersionID
from evidently.sdk.prompts import RemotePromptManager
from evidently.sdk.prompts import VersionOrLatest
from evidently.ui.workspace import CloudWorkspace


class PromptRegistryOption(Option):
    token: SecretStr
    url: str = "https://app.evidently.cloud"

    def get_prompt_manager(self) -> RemotePromptManager:
        ws = CloudWorkspace(self.token.get_secret_value(), self.url)
        return ws.prompts


class PromptRenderContext:
    def __init__(self, options: Options) -> None:
        self.options = options
        self.refs_resolved = []
        self._manager: Optional[RemotePromptManager] = None

    @property
    def manager(self) -> RemotePromptManager:
        if self._manager is None:
            o = self.options.get(PromptRegistryOption)
            self._manager = o.get_prompt_manager()
        return self._manager

    def resolve_prompt_content(self, content: "PromptContent") -> str:
        if isinstance(content, PromptRef):
            self.refs_resolved.append(content)
            return content.resolve(self.manager).content
        return content


prompt_render_context = contextvars.ContextVar("prompt_render_context", default=PromptRenderContext(Options()))


class PromptRef(BaseModel):
    id: Optional[PromptVersionID] = None
    prompt_id: Optional[PromptID] = None
    version: VersionOrLatest = "latest"

    def resolve(self, pm: RemotePromptManager) -> PromptVersion:
        if self.id is not None:
            return pm.get_version_by_id(self.id)
        if self.prompt_id is not None:
            return pm.get_version(self.prompt_id, self.version)
        raise ValueError("cannot resolve prompt ref")


PromptContent = Union[PromptRef, str]


@contextlib.contextmanager
def set_prompt_render_context(context: PromptRenderContext):
    token = prompt_render_context.set(context)
    try:
        yield context
    finally:
        prompt_render_context.reset(token)
