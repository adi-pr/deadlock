from pathlib import Path
from typing import Optional

from auxillary.process_runner import run_command

def run_nikto(
    target: str,
    output_dir: Optional[Path],
    timeout: int = 900,
    ssl: bool = True,
    extra_args: Optional[list[str]] = None,
    ):

    if output_dir is None:
        output_dir = Path.cwd() / "output" / "nikto_output"

    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = (output_dir / "nikto.txt").resolve()

    cmd = [
        "nikto",
        "-host",
        target,
        "-output",
        str(log_file),
    ]

    if not ssl:
        cmd.append("-nossl")

    if extra_args:
        cmd.extend(extra_args)

    result = run_command(cmd, timeout=timeout, output_file=log_file)

    if result.get("timeout"):
        print(f"Nikto scan timed out after {result.get('duration')} seconds")
        return

    # Prefer Nikto's log file as ground truth
    if log_file.exists():
        try:
            raw_output = log_file.read_text(errors="ignore")
        except Exception as e:
            raw_output = f"Failed to read nikto.log: {e}"
    else:
        raw_output = result.get("stdout") or result.get("stderr") or ""

    # Provide a minimal run summary
    summary = {
        "tool": "nikto",
        "target": target,
        "raw_output": raw_output,
        "exit_code": result.get("exit_code"),
        "duration": result.get("duration"),
        "error": (result.get("stderr") or "").strip() if result.get("exit_code") not in (None, 0) else None,
    }

    print(summary)

