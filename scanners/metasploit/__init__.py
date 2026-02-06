from pymetasploit3.msfrpc import MsfRpcClient
from GenAttacks import Auxillary_Gen
from auxillary.get_output import get_output_file as get_output

from pathlib import Path
from typing import Optional
from typer import prompt
from time import sleep
import re

def run_metasploit(
    target: str,
    output_dir: Optional[Path],
    timeout: int = 900,
): 
    if output_dir is None:
        output_dir = Path.cwd() / "metasploit_output"
    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = (output_dir / "metasploit.txt").resolve()

    print(f"Running Metasploit scan on target: {target}")
    
    nmap_output = get_output("nmap")
    nikto_output = get_output("nikto")
    
    password = prompt("Enter Metasploit RPC password", hide_input=True)
    client = MsfRpcClient(password)
    
    available_modules = client.modules.auxiliary
    
    selected_modules = Auxillary_Gen.generate_auxillary(
        available_modules,
        nmap_output,
        nikto_output,
    )
    
    with log_file.open("w") as f:
        for module_name in selected_modules:
            print(f"Running module: {module_name}")

            output = run_auxiliary_module(
                client,
                module_name,
                target,
                timeout
            )

            f.write(f"\n===== {module_name} =====\n")
            f.write(output)
            f.write("\n")
            
    print(f"Metasploit scan completed. Results saved to {log_file}")

def clean_metasploit_output(output: str) -> str:
    """Remove ASCII art and banner text from Metasploit output."""
    lines = output.split('\n')
    cleaned_lines = []
    skip_banner = False
    
    for line in lines:
        # Skip ASCII art characters and banner sections
        if any(char in line for char in ['│', '┌', '└', '├', '─', '╔', '╚', '║', '═']):
            continue
        if any(pattern in line for pattern in [
            '=[ metasploit',
            '+ -- --=[',
            'Metasploit Documentation:',
            'Metasploit Framework is a',
            '       .',
            '      .',
            '     .',
            '    .',
            '   .',
            '  .',
            ' .',
        ]):
            continue
        # Skip lines that are mostly ASCII art (contain lots of special chars)
        if re.match(r'^[\s\.\,\(\)\_\-\;\'\"\@\#\*\|\\/\+\=\:\[\]]+$', line):
            continue
        # Keep lines with actual data
        if line.strip():
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def run_auxiliary_module(
    client: MsfRpcClient,
    module_name: str,
    target: str,
    timeout: int,
) -> str:
    console = client.consoles.console()

    command = (
        f"use auxiliary/{module_name}\n"
        f"set RHOSTS {target}\n"
        f"run\n"
    )

    console.write(command)

    output = ""
    for _ in range(timeout):
        sleep(1)
        res = console.read()
        data = res.get("data", "")
        output += data

        # Metasploit usually prints this when done
        if "Auxiliary module execution completed" in data:
            break

    console.destroy()
    return clean_metasploit_output(output)
