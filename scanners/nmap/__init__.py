from pathlib import Path
from typing import Optional

from auxillary.process_runner import run_command

def run_nmap(
    target: str,
    output_dir: Optional[Path],
    timeout: int = 900,
    flag: str = "recon",
    ):

    if output_dir is None: # CHANGE REQUIRED -  delete output as we just store stdout live unless output is requested by user
        output_dir = Path.cwd() / "output" / "nmap_output"

    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = (output_dir / "nmap.txt").resolve()

    cmd = nmap_cmd_builder(target, output_dir, flag)
    print(f"Running Nmap scan on target: {target}")
    print(f"Command: {' '.join(cmd)}")

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

    print(summary)

''' Function to build nmap command based on the type of scan (recon vs exploit) '''
def nmap_cmd_builder(target: str, output_dir: Path, flag: str = "recon") -> list[str]:
    
    recon_flags = ["-sC", "-sV", "-O", "T4"]
    exploit_flags = ["-sV", "--script=vuln", "T4"]
    
    cmd = [
        "sudo",
        "nmap",
        str(output_dir / "nmap.txt"),
        target,
    ]

    if flag == "recon":
        cmd[2:2] = recon_flags
    elif flag == "exploit":
        cmd[2:2] = exploit_flags
    
    return cmd