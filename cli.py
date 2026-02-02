from pathlib import Path
import typer
from scanners import Nikto
from GenAttacks import Exploit_Gen

def call_nikto(args: dict):
    """Calls nikto CLI and generates output based on tgt paramaters

    Args:
        args (dict): dictionary from main flags are parsed from main()
    """
    Nikto.run_nikto(
        target=args["target"],
        timeout=args["timeout"],
        output_dir=args["output"],
    )

def call_exploitgen(cve_id, target,maxRetries = 5, generate_type = "scanner"):
    try:
        Exploit_Gen.generate_exploit(cve_id, target, maxRetries,generate_type)
    except:
        print("Unhandled exception please log on the github repo")
    

# python cli.py --help to list flags
def main(
        target: str, 
        web: bool = False,
        exploit: bool = False,
        timeout: int = 900,
        output: Path | None = typer.Option(
            None,
            "--output",
            "-o",
            help="Output directory",
        ),
        cve_id: str | None = typer.Option(
            None,
            "--generate",
            "-g",
            help="CVE ID",
        ),
        attack_type: str | None = typer.Option(
            "exploit",
            "--type",
            "-t",
            help="exploit/scanner",
        ),
    ):
    print("Deadlock CLI is running.")
    if cve_id: 
        call_exploitgen(cve_id, attack_type)
    else:
    
        call_nikto(locals()) # be careful to keep locals the same name


    
if __name__ == "__main__":
    typer.run(main)