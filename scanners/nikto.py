
from pathlib import Path
import subprocess
import time
from typing import Optional


NIKTO_IMAGE = "cirt/nikto"

def run_nikto(
    target: str,
    output_dir: Path,
    timeout: int = 900,
    ssl: bool = True,
    extra_args: Optional[list[str]] = None,
):
    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = (output_dir / "nikto.txt").resolve()
    cmd = [
        "nikto",
        "-host", target,
        "-output", str(log_file),
    ]

    if not ssl:
        cmd.append("-nossl")

    if extra_args:
        cmd.extend(extra_args)

    start_time = time.time()

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        exit_code = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr

    except subprocess.TimeoutExpired:
        duration = round(time.time() - start_time, 2)
        print(f"Nikto scan timed out after {duration} seconds")
        return

    duration = round(time.time() - start_time, 2)

    # Prefer Nikto's log file as ground truth
    if log_file.exists():
        try:
            raw_output = log_file.read_text(errors="ignore")
        except Exception as e:
            raw_output = f"Failed to read nikto.log: {e}"
    else:
        raw_output = stdout or stderr or ""
        print({
            "tool": "nikto",
            "target": target,
            "raw_output": raw_output,
            "exit_code": exit_code,
            "duration": duration,
            "error": stderr.strip() if exit_code != 0 else None,
        })
