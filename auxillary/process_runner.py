from pathlib import Path
import subprocess
import time
from typing import Optional, Dict


def run_command(cmd: list[str], timeout: int = 900, output_file: Optional[Path] = None) -> Dict:
    """Run an external command and optionally write stdout to `output_file`.

    Returns a dict with keys: exit_code, stdout, stderr, duration, or timeout=True on timeout.
    """
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
    except subprocess.TimeoutExpired as e:
        duration = round(time.time() - start_time, 2)
        return {"timeout": True, "duration": duration, "error": str(e)}

    duration = round(time.time() - start_time, 2)

    if output_file is not None:
        try:
            output_file.write_text(stdout or "", encoding="utf-8", errors="ignore")
        except Exception as e:
            stderr = (stderr or "") + f"\nFailed to write output file: {e}"

    return {
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "duration": duration,
    }
