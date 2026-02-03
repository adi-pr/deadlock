#!/usr/bin/env python3
from pathlib import Path
import typer
from scanners import *
from GenAttacks import Exploit_Gen, Summary_Gen
from fun import menuanimation
from time import sleep
import socket, re
from time import sleep
app = typer.Typer(
    help="""
 Deadlock CLI
 example usage python cli.py scan 192.168.0.1 --type exploit -r 10 

Only target systems you own or are authorized to test on.
""",
    context_settings={"help_option_names": ["-h", "--help"], "max_content_width": 100}
)

#region hook function
def call_nikto(args: dict):
    Nikto.run_nikto(
        target=args["target"],
        timeout=args["timeout"],
        output_dir=args["output"],
    )

def call_nmap(args: dict):
    from scanners import Nmap
    Nmap.run_nmap(
        target=args["target"],
        timeout=args["timeout"],
        output_dir=args["output"],
    )

def call_exploitgen(cve_id, target, maxRetries=5, generate_type="scanner"):
    menuanimation.run()
    try:
        Exploit_Gen.generate_exploit(
            cve_id, target,
            maxRetries=maxRetries,
            generate_type=generate_type
        )
    except Exception as e:
        print("Unhandled exception:", e)

def check_file(path: Path) -> bool:
    return path.is_file()

def dns_to_ip(domain_name) -> str:
    if re.search(r"[a-zA-Z]", domain_name):
        ip = socket.gethostbyname(domain_name)
    else:
        print("ip has been given")
    return ip
#endregion
## Testing commands 


# refactored to app.commands to actually allow us to have different modules split up into comamnds rather than one set of flags for all
@app.command()
def test_functionality():
    """Run internal tests"""
    Summary_Gen.test_functionality()
    if "142.251" in dns_to_ip("google.com"): # only check part of the domain name not the exact device (not perfect validation but still)
        print("Dns to Ip working")
    else:
        print(dns_to_ip("google.com")) 
        print("testcase failed")

@app.command()
def scan(
    target: str,
    web: bool = False,
    exploit: bool = False,
    timeout: int = 900,
    output: Path | None = typer.Option(None, "-o", "--output"),
    cve_id: str | None = typer.Option(None, "-g", "--generate"),
    attack_type: str = typer.Option("exploit", "-t", "--type"),
    maxRetries: int = typer.Option(5, "-r", "--retries"),
    list: Path | None = typer.Option(None, "-l", "--list"),
):
    """Run scans and optionally exploit findings"""

    print("Deadlock CLI is running.")

    if list:
        print("Using target list — make sure you know what you're doing")
        sleep(2)
    if not check_file(list):
        typer.echo("Target list does not exist")
        raise typer.Exit(code=1)
    else:
        print("target list exists setting recursive mode")
        
    target = dns_to_ip(target) # automatically take either domain name or ipv4 and resolve it
    print(f"current target is {target}")
    sleep(2)
   
    if cve_id:
        print(f"Calling exploit for {cve_id} with {maxRetries} retries")
        call_exploitgen(cve_id, target, maxRetries, attack_type)
        return

    #nikto_result = call_nikto(locals())
    #nmap_result = call_nmap(locals())

    #Summary_Gen.generate_summary(
    #    stdout=f"## Nikto ## {nikto_result}\n## Nmap ## {nmap_result}"
    #)

@app.command()
def AutoMode():
    pass

if __name__ == "__main__":
    app()
