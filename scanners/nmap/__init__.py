from pathlib import Path
from typing import Optional

from auxillary.process_runner import run_command

def run_nmap(
    target: str,
    output_dir: Optional[Path],
    timeout: int = 900,
    scan_type: str = "SYN",
    extra_args: Optional[list[str]] = None,
    ):

    if output_dir is None:
        output_dir = Path.cwd() / "nmap_output"

    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = (output_dir / "nmap.txt").resolve()

    scan_flag = "-sS" if scan_type.upper() == "SYN" else "-sT"

    cmd = [
        "sudo",
        "nmap",
        scan_flag,
        "-oN",
        str(log_file),
        target,
    ]
    
    print(f"Running Nmap scan on target: {target} with scan type: {scan_flag}")
    print(f"Command: {' '.join(cmd)}")

    if extra_args:
        cmd.extend(extra_args)

    result = run_command(cmd, timeout=timeout, output_file=log_file)

    if result.get("timeout"):
        print(f"Nmap scan timed out after {result.get('duration')} seconds")
        return

    # Prefer Nmap's log file as ground truth
    if log_file.exists():
        try:
            raw_output = log_file.read_text(errors="ignore")
        except Exception as e:
            raw_output = f"Failed to read nmap.log: {e}"
    else:
        raw_output = result.get("stdout") or result.get("stderr") or ""

    # Provide a minimal run summary
    summary = {
        "tool": "nmap",
        "target": target,
        "raw_output": raw_output,
        "exit_code": result.get("exit_code"),
        "duration": result.get("duration"),
        "error": (result.get("stderr") or "").strip() if result.get("exit_code") not in (None, 0) else None,
    }

    print(summary
)