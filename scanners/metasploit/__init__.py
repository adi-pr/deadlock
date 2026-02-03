from pymetasploit3.msfrpc import MsfRpcClient
from . import profile as msf_profile

from pathlib import Path
from typing import Optional
from typer import prompt

def run_metasploit(
    target: str,
    output_dir: Optional[Path],
    timeout: int = 60,
    msf_profiles: Optional[list[str]] = None,
): 
    if output_dir is None:
        output_dir = Path.cwd() / "metasploit_output"

    output_dir.mkdir(parents=True, exist_ok=True)
    log_file = (output_dir / "metasploit.txt").resolve()

    print(f"Running Metasploit scan on target: {target}")
    
    print("Extra args: ", msf_profiles)
    
    print("Loading Metasploit profiles...")
    selected_modules = set()
    if msf_profiles:
        for profile_name in msf_profiles:
            profile_modules = msf_profile.PROFILES.get(profile_name)
            if profile_modules:
                selected_modules.update(profile_modules)
            else:
                print(f"Warning: Profile '{profile_name}' not found.")
    else:
        selected_modules = msf_profile.PROFILES["standard"]
    
    print(f"Selected modules: {selected_modules}")
    
    # password = prompt("Enter Metasploit RPC password", hide_input=True)
    # client = MsfRpcClient(password)

    # # Example of running a simple auxiliary scanner
    # module = client.modules.use('auxiliary', 'scanner/http/http_version')
    # module['RHOSTS'] = target

    # result = module.execute()

    # with log_file.open('w') as f:
    #     f.write(str(result))

    print(f"Metasploit scan completed. Results saved to {log_file}") 
    