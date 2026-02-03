#!/usr/bin/env python3
# Developer credits: Aditiya (Ruben) Prasad & Casrepoclone
from pathlib import Path 
import typer
from scanners import * 
from GenAttacks import Exploit_Gen
from GenAttacks import Summary_Gen # for testmode
from fun import menuanimation
from time import sleep
from pathlib import Path

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

def call_nmap(args: dict):
    """Calls nmap CLI and generates output based on tgt paramaters

    Args:
        args (dict): dictionary from main flags are parsed from main()
    """
    from scanners import Nmap
    Nmap.run_nmap(
        target=args["target"],
        timeout=args["timeout"],
        output_dir=args["output"],
    )

def call_exploitgen(cve_id, target,maxRetries = 5, generate_type = "scanner"):
    menuanimation.run()
    try:
        Exploit_Gen.generate_exploit(cve_id, target, maxRetries=maxRetries, generate_type=generate_type)
    except:
        print("Unhandled exception please log on the github repo")

def check_file(FilePath) -> bool:
    my_file = Path(FilePath)
    if my_file.is_file(): 
        return True
    else:
        return False    

# python cli.py --help to list flags
def main(
    # so far used chars
    # -o -g -t -r 
        target: str, 
        web: bool = False,
        exploit: bool = False,
        timeout: int = 900,
        testmode: bool | None = typer.Option(
            False,
            "--testmode",
            "-7",
            help="True/False to start tests"
        ),
        output: Path | None = typer.Option(
            None,
            "--output",
            "-o",
            help="Output directory e.g. -o ./Ishouldntseethis.txt",
        ),
        cve_id: str | None = typer.Option(
            None,
            "--generate",
            "-g",
            help="CVE ID e.g. -g CVE-2025-67420",
        ),
        attack_type: str | None = typer.Option(
            "exploit",
            "--type",
            "-t",
            help="exploit or scanner e.g. -t scanner",
        ),
        maxRetries: int | None = typer.Option(
            "5",
            "--retries",
            "-r",
            help="for developers set this to 2 only e.g. -r 2",
        ),
        list: Path | None = typer.Option(
            None,
            "--list",
            "-l",
            help="target list location e.g. --list ./targets.txt",
        ),
    ):
 
    print("Deadlock CLI is running.")
    
    if testmode:
        test_summary = Summary_Gen.test_functionality()
    else:pass
        
        
    if list:
        print("I see you are using a list are you sure you know what you're doing")
        sleep(2)
        if check_file(list):
            print("file validated as existing... nice work")
        else:
            print("please check your filepath it doesn't exist are you sure you have it in the right directory")
    # if we know the CVE start attack
    if cve_id: 
        print(f"calling exploit for {cve_id} with {maxRetries} retries")
        call_exploitgen(cve_id, attack_type, maxRetries)
    
    # otherwise find vulns to exploit 
    else:
        pass
        #nikto_result = call_nikto(locals()) # be careful to keep locals the same name
        #nmap_result = call_nmap(locals())
        # check this line it needs testing on kali
        #Summary_Gen.generate_summary(stdout=f" ## Nikto output ## {nikto_result} ## Nmap output ## {nmap_result}")


    
if __name__ == "__main__":
    typer.run(main)