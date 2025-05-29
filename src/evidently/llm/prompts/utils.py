import ast
import re
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence

from evidently.legacy.utils.llm.prompts import PromptBlock


def _parse_function_call(call_string):
    try:
        node = ast.parse(call_string, mode="eval").body
    except SyntaxError:
        raise ValueError("Invalid function call syntax")

    if not isinstance(node, ast.Call):
        raise ValueError("The string is not a valid function call")

    if isinstance(node.func, ast.Name):
        func_name = node.func.id
    else:
        raise ValueError("Unsupported function call format")

    args = [arg.id for arg in node.args]
    kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in node.keywords}

    return func_name, args, kwargs


def prompt_block_input(
    placeholder_name: str = "input", anchors: bool = False, start: str = "__start__", end: str = "__end__"
):
    res = PromptBlock.input(placeholder_name)
    if anchors:
        res = res.anchored(start, end)
    return res


def _parse_cmd_to_block(cmd: str):
    cmd_mapping = {
        "input": prompt_block_input,
        "output_json": PromptBlock.json_output,
        "output_string_list": PromptBlock.string_list_output,
        "output_string": PromptBlock.string_output,
    }
    func_name, args, kwargs = _parse_function_call(cmd)
    return cmd_mapping[func_name](*args, **kwargs)


def _parse_prompt(prompt_template: str) -> Sequence["PromptBlock"]:
    res = []
    for part in re.split(r"({%\s.*?\s%})", prompt_template):
        if not part.startswith("{%"):
            res.append(PromptBlock.simple(part))
            continue
        cmd = part.strip("{}% ")
        res.append(_parse_cmd_to_block(cmd))

    return res


class PartialFormatter(dict):
    def __missing__(self, key):
        return f"{{{key}}}"


def partial_format(template: str, values: Optional[Dict[str, Any]]) -> str:
    if values is None:
        return template
    return template.format_map(PartialFormatter(values))
