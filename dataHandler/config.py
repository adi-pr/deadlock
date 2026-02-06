#!/usr/bin/env python3
## This folder contains the dataclasses for the flags for all our modules
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from pathlib import Path

# - Target Info -
@dataclass
class Target:
    target: str = "0.0.0.0"                                     # Target IPv4
    open_ports: Dict[str, int] = field(default_factory=dict)    # e.g. {"SSH": 22}
    cve_list: List[str] = field(default_factory=list)           # List of discovered vulnerabilities
    export: bool = False                                        # Turns on export from flag
    output_dir: Optional[Path] = None                           # Output directory

    def __post_init__(self):                                    # Generate output directory (default if flag is called and no output set)
        if self.output_dir is None:
            # Automatically set output_dir based on target
            self.output_dir = Path(f"./target/{self.target}.txt")

# Container for multiple targets
@dataclass
class TargetList:
    targets: List[Target] = field(default_factory=list)

# == Scanners == 
##  - Nikto - 
@dataclass
class NiktoArgs:
    target: str = Target.target
    output_dir: Path
    timeout: int = 900
    ssl: bool = True
    extra_args: Optional[List[str]] = None

## - Nmap PLACEHOLDER - 
@dataclass
class NmapArgs:
    target: str = Target.target                     
    output_dir: Path                 
    ports: Optional[str] = None        
    scan_type: Optional[str] = None     
    extra_args: Optional[List[str]] = None
    
    cmd: List[str] = field(default_factory=lambda: [
        "sudo",
        "nmap",
        "-sS",
        "-sV",
        "-O",
        "-p-",
        "--open",
        "--script=http-title,http-headers,http-methods",
        "-oN",
        "{log_file}",
        "{target}",
    ])
