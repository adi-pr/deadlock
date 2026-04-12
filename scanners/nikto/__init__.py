from pathlib import Path
from typing import Optional

from auxillary.process_runner import run_command

def run_nikto(
    target: str,
    output_dir: Optional[Path],
    timeout: int = 900,
    flag: str = "recon",
    ):

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        log_file = (output_dir / "nikto.txt").resolve()

    cmd = nikto_cmd_builder(target=target, output_dir=output_dir, flag=flag)

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
        "exit_code": result.get("exit_code"),
        "duration": result.get("duration"),
        "error": (result.get("stderr") or "").strip() if result.get("exit_code") not in (None, 0) else None,
    }

    print(summary)

from pathlib import Path

''' Function to build nikto command based on type of scan (recon vs scan) '''
def nikto_cmd_builder(target: str, output_dir: Path | None = None, flag: str = "recon") -> list[str]:

    flag_map = {
        "recon": ["-Display", "V"],
        "scan": ["-Tuning", "123b"],
    }

    flags = flag_map.get(flag, [])

    cmd = ["nikto", "-h", target] + flags

    if output_dir:
        cmd += ["-o", str(output_dir / "nikto.txt"), "-Format", "txt"]

    return cmd