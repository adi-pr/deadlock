from pathlib import Path

def cleanup_output_dir(output_dir: Path) -> None:
    """Cleans up the output directory by removing temporary files."""
    if output_dir.exists() and output_dir.is_dir():
        for item in output_dir.iterdir():
            if item.is_file() and item.suffix == ".tmp":
                item.unlink()
        print(f"Cleaned up temporary files in {output_dir}")