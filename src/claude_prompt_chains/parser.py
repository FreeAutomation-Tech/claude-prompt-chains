import re
import yaml


class ChainParseError(Exception):
    pass


def parse_chain(filepath):
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ChainParseError("Chain file must contain a YAML mapping")

    name = data.get("name", "")
    description = data.get("description", "")
    raw_steps = data.get("steps", [])

    if not raw_steps:
        raise ChainParseError("Chain must have at least one step")

    steps = []
    for i, raw in enumerate(raw_steps):
        if not isinstance(raw, dict):
            raise ChainParseError(f"Step {i} must be a mapping")
        step_name = raw.get("name", f"step_{i}")
        prompt = raw.get("prompt", "")
        if not prompt:
            raise ChainParseError(f"Step '{step_name}' has no prompt")
        steps.append({
            "name": step_name,
            "prompt": prompt,
        })

    return {
        "name": name,
        "description": description,
        "steps": steps,
    }


def render_prompt(template, context):
    def replacer(match):
        key = match.group(1).strip()
        parts = key.split(".")
        value = context
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part, "")
            else:
                return ""
        if value is None:
            return ""
        return str(value)

    return re.sub(r"\{\{(.+?)\}\}", replacer, template)
