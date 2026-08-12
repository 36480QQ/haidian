"""Dependency-free parsing for the repository's Markdown front matter."""

BLOCK_SCALARS = {">", ">-", "|", "|-"}


def _block_value(lines: list[str], style: str) -> str:
    nonempty = [line for line in lines if line.strip()]
    indent = min((len(line) - len(line.lstrip()) for line in nonempty), default=0)
    values = [line[indent:] if line.strip() else "" for line in lines]
    if style.startswith("|"):
        value = "\n".join(values)
    else:
        parts: list[str] = []
        for line in values:
            if not parts:
                parts.append(line)
            elif line and parts[-1]:
                parts[-1] += " " + line
            else:
                parts.append(line)
        value = "\n".join(parts)
    return value if style.endswith("-") else value + "\n"


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Parse scalar front matter, including folded and literal block strings."""
    text = text.lstrip("\ufeff\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    lines = text[4:end].splitlines()
    body = text[end + len("\n---") :].lstrip("\n")
    metadata: dict[str, str] = {}
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        index += 1
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        value = value.strip()
        if value in BLOCK_SCALARS:
            block: list[str] = []
            while index < len(lines):
                candidate = lines[index]
                if candidate.strip() and not candidate[:1].isspace():
                    break
                block.append(candidate)
                index += 1
            metadata[key.strip()] = _block_value(block, value)
        else:
            metadata[key.strip()] = value.strip('"').strip("'")
    return metadata, body
