from pathlib import Path

def get_output_file(name: str) -> Path:
    """Get the output file path for a given scanner or exploit name."""
    output_dir = Path.cwd() / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{name}_output.txt"