from pathlib import Path
import typer
from scanners import nikto


def main(target: str, web: bool = False):
    print("Deadlock CLI is running.")
    nikto.run_nikto(target=target, output_dir=Path("output"))
    
    
if __name__ == "__main__":
    typer.run(main)