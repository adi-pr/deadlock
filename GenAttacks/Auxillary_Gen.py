from pathlib import Path

from . import Agent


def _read_output(source) -> str:
    if isinstance(source, Path):
        path = source
    else:
        try:
            path = Path(str(source))
        except Exception:
            return str(source)

    if path.exists() and path.is_file():
        try:
            return path.read_text(errors="ignore")
        except Exception as e:
            return f"Failed to read {path}: {e}"
    return str(source)


def _normalize_module_name(name: str) -> str:
    cleaned = name.strip().strip("'\"")
    if cleaned.startswith("auxiliary/"):
        cleaned = cleaned[len("auxiliary/"):]
    return cleaned


def _parse_module_list(raw: str) -> list[str]:
    if not raw:
        return []
    parts = [p.strip() for p in raw.replace("\n", ",").split(",")]
    cleaned: list[str] = []
    seen: set[str] = set()
    for part in parts:
        name = _normalize_module_name(part)
        if name and name not in seen:
            cleaned.append(name)
            seen.add(name)
    return cleaned


def generate_auxillary(auxillary_modules, nmap_output, nikto_output) -> list[str]:
    nmap_text = _read_output(nmap_output)
    nikto_text = _read_output(nikto_output)

    available = [_normalize_module_name(m) for m in auxillary_modules or []]
    available = [m for m in available if m]
    available_set = set(available)

    message = (
        "You are a security automation assistant. "
        "Return only a comma-separated list of Metasploit auxiliary module paths "
        "relative to auxiliary/. Example: scanner/ssh/ssh_version. "
        "Rules: no extra text, no numbering, no explanations, no markup. "
        "Only choose from the provided available modules list."
    )

    prompt = (
        "Select the most relevant auxiliary modules based on these scan outputs. "
        f"Available modules: {', '.join(available)}\n\n"
        f"Nmap output:\n{nmap_text}\n\nNikto output:\n{nikto_text}"
    )

    raw_modules = Agent.instanciate_agent(message, prompt, strip_markup=True)
    selected = _parse_module_list(raw_modules)

    if available_set:
        selected = [m for m in selected if m in available_set]

    return selected