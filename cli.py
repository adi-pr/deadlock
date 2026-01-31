from pathlib import Path
import typer
from scanners import nikto


def call_nikto(args: dict):
    """Calls nikto CLI and generates output based on tgt paramaters

    Args:
        args (dict): dictionary from main flags are parsed from main()
    """
    nikto.run_nikto(
        target=args["target"],
        timeout=args["timeout"],
    )

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
    ):
    
    print("Deadlock CLI is running.")
    call_nikto(locals()) # be careful to keep locals the same name


    
if __name__ == "__main__":
    typer.run(main)