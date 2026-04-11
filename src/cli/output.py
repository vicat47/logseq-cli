from __future__ import annotations

import json


def _format_plain_value(value: object) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def format_output(
    data: object,
    fields: list[str] | None = None,
    plain: bool = False,
) -> str:
    items = data if isinstance(data, list) else [data]

    if fields:
        items = [
            {k: item[k] for k in fields if k in item}
            if isinstance(item, dict)
            else item
            for item in items
        ]

    if plain:
        blocks = []
        for item in items:
            if isinstance(item, dict):
                lines = [f"{k}: {_format_plain_value(v)}" for k, v in item.items()]
                blocks.append("\n".join(lines))
            else:
                blocks.append(_format_plain_value(item))
        return "\n\n".join(blocks) + "\n"

    return "\n".join(json.dumps(item) for item in items) + "\n"
