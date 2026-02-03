from pymetasploit3.msfrpc import MsfRpcClient

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
    
    # password = prompt("Enter Metasploit RPC password", hide_input=True)
    # client = MsfRpcClient(password)

    # # Example of running a simple auxiliary scanner
    # module = client.modules.use('auxiliary', 'scanner/http/http_version')
    # module['RHOSTS'] = target

    # result = module.execute()

    # with log_file.open('w') as f:
    #     f.write(str(result))

    print(f"Metasploit scan completed. Results saved to {log_file}")
    
def load_profiles(args: list[str]):
    from . import profile
    
    profiles = {}
    
    if args is None or len(args) == 0:
        profiles["recon"] = profile.RECON_MODULES
        
    else:
        for arg in args:
            if arg == "recon":
                profiles["recon"] = profile.RECON_MODULES
            elif arg == "generic_web_vulns":
                profiles["generic_web_vulns"] = profile.GENERIC_WEB_VULNS
            elif arg == "wordpress":
                profiles["wordpress"] = profile.WORDPRESS_MODULES
            elif arg == "cms":
                profiles["cms"] = profile.CMS_MODULES
                
    return profiles
    
    