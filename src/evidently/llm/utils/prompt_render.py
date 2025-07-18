import ast
import re
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from evidently.legacy.core import new_id
from evidently.llm.utils.blocks import NoopOutputFormat
from evidently.llm.utils.blocks import OutputFormatBlock
from evidently.llm.utils.blocks import PromptBlock

placeholders_re = re.compile(r"\{([a-zA-Z0-9_. ]+)}")


def substitute_placeholders(template, mapping):
    pattern = r"{([^{}]+)}"

    def replacer(match):
        key = match.group(1)
        return str(mapping.get(key, match.group(0)))  # leave unchanged if not found

    return re.sub(pattern, replacer, template)


class PreparedTemplate:
    def __init__(
        self, template: str, placeholders: Optional[Set[str]] = None, output_format: Optional[OutputFormatBlock] = None
    ):
        self.template = template
        if placeholders is None:
            placeholders = set(placeholders_re.findall(template))
        self.placeholders = placeholders
        self._output_format = output_format

    @property
    def output_format(self) -> OutputFormatBlock:
        return self._output_format or NoopOutputFormat()

    @output_format.setter
    def output_format(self, output_format: OutputFormatBlock):
        self._output_format = output_format

    @property
    def has_output_format(self) -> bool:
        return self._output_format is not None

    def render(self, values: Dict[str, Any]) -> str:
        return self.template.format(**{p: values[p] for p in self.placeholders})

    def render_partial(self, values: Dict[str, Any]) -> "PreparedTemplate":
        ph = {p: values.get(p, f"{{{p}}}") for p in self.placeholders}
        return PreparedTemplate(
            template=substitute_placeholders(self.template, ph), placeholders=None, output_format=self.output_format
        )

    def __repr__(self) -> str:
        ph = ", ".join(self.placeholders)
        return f"PreparedTemplate[{ph}]\n```\n{self.template}\n```"


PromptCommandCallable = Callable[..., Union[PromptBlock, List[PromptBlock]]]

_prompt_command_registry: Dict[str, PromptCommandCallable] = {
    "output_json": PromptBlock.json_output,
    "output_string_list": PromptBlock.string_list_output,
    "output_string": PromptBlock.string_output,
}


def prompt_command(f: Union[str, PromptCommandCallable]):
    name = f if isinstance(f, str) else f.__name__

    def dec(func: PromptCommandCallable):
        _prompt_command_registry[name] = func
        return func

    return dec(f) if callable(f) else dec


def get_placeholder_var_values(variables: Dict[str, Any], placeholders: Iterable[str]) -> Dict[str, str]:
    res = {}

    def _get_value(o, path: List[str]):
        if len(path) == 0:
            return o
        key, *path = path
        return _get_value(getattr(o, key), path)

    def _render(o) -> str:
        if isinstance(o, list):
            return "\n".join(_render(o) for o in o)
        if isinstance(o, PromptBlock):
            return o.render()
        return str(o)

    for ph in placeholders:
        var_name, *var_path = ph.split(".")
        if var_name not in variables:
            continue
        var_value = _get_value(variables[var_name], var_path)
        res[ph] = _render(var_value)

    return res


class TemplateRenderer:
    def __init__(
        self,
        template: str,
        holder: Any,
        variables: Optional[Dict[str, Any]] = None,
        commands: Optional[Dict[str, PromptCommandCallable]] = None,
    ):
        self.template = template
        self.holder = holder
        self.vars = variables or {}
        self.vars["self"] = holder
        self.commands = commands or _prompt_command_registry

    def add_var(self, name: str, value: Any):
        self.vars[name] = value

    def add_command(self, name: str, command: PromptCommandCallable):
        self.commands[name] = command

    @staticmethod
    def extract_command_calls(template: str):
        pattern = r"{%\s*(.*?)\s*%}"
        mapping = {}

        def replacer(match):
            content = match.group(1)
            random_key = f"_command_{new_id().hex}"
            mapping[random_key] = content
            return f"{{{random_key}}}"

        replaced_string = re.sub(pattern, replacer, template)
        return replaced_string, mapping

    def prepare(self) -> PreparedTemplate:
        template, command_calls = self.extract_command_calls(self.template)
        prepared = PreparedTemplate(template)
        command_values = {}
        for name, command in command_calls.items():
            blocks = self._parse_command_to_blocks(command)
            command_values[name] = "\n".join(str(b) for b in blocks)
            for b in blocks:
                if isinstance(b, OutputFormatBlock):
                    prepared.output_format = b
        prepared = prepared.render_partial(command_values)

        var_values = get_placeholder_var_values(self.vars, prepared.placeholders)
        return prepared.render_partial(var_values)

    def _parse_command_to_blocks(self, cmd: str) -> List[PromptBlock]:
        func_name, args, kwargs, is_method = self._parse_function_call(cmd)
        if is_method:
            func = getattr(self.holder, func_name)
            result = func(*args, **kwargs)
            if not isinstance(result, list):
                result = [result]
            return result
        if func_name not in self.commands:
            raise ValueError(
                f"Unknown function call `{func_name}`. Available functions: {list(_prompt_command_registry.keys())}"
            )
        result = self.commands[func_name](*args, **kwargs)
        if not isinstance(result, list):
            result = [result]
        return result

    def _parse_function_call(self, call_string) -> Tuple[str, List[str], Dict, bool]:
        try:
            node = ast.parse(call_string, mode="eval").body
        except SyntaxError:
            raise ValueError("Invalid function call syntax")

        if not isinstance(node, ast.Call):
            raise ValueError("The string is not a valid function call")

        if isinstance(node.func, ast.Name):
            is_method = False
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            is_method = True
            func_name = node.func.attr
        else:
            raise ValueError("Unsupported function call format")

        args = [self._parse_function_call_arg(arg) for arg in node.args]
        kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in node.keywords}

        return func_name, args, kwargs, is_method

    def _parse_function_call_arg(self, arg_node: ast.expr) -> str:
        def rec(node: ast.AST) -> List[str]:
            if isinstance(node, ast.Attribute):
                return rec(node.value) + [node.attr]
            if isinstance(node, ast.Name):
                return [node.id]
            if isinstance(node, ast.Constant):
                return [node.value]
            raise NotImplementedError(f"Cannot parse {node}")

        first, *path = rec(arg_node)
        if first not in self.vars:
            if len(path) == 0:
                return first
            raise KeyError(f"Variable '{first}' is not defined")
        obj = self.vars[first]
        while path:
            obj = getattr(obj, path[0])
            path.pop(0)
        return obj
