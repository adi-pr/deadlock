## -- THIS IS A VERY DANGEROUS MODE --
# -- THIS WILL ALLOW THE AI TO COLLECT RESULTS OF SCANS AND PROCESS THE DATA TO CONTINUE ATTACKS LIVE --
# -- EXPENSIVE FINANCIALLY TO RUN --
import boto3
import json
import re
from time import sleep
import subprocess
from pathlib import Path
import Agent # change to from . import Agent when implemented outside testing


class Artificial_penetrator():
    def __init__(self):
        self.log = []
        self.privilageLevel = ""
    def _gen(self, target="", stdout=""):  
        clean_response = ""
        while "DONE" not in clean_response:
                
            #region AI-Guardrails
            message = """You are a penetration tester that can run any scanners or exploits on kali linux using default packages. your job is to gather as much information as possible
            If you output anything other than commands such as nmap -sV example.com or install commands such as apt get, pip, the response is invalid.
            Rules:
            - Never include <think>, </think>, or any reasoning text.
            - once you have completed all scanning to find vulnerabilities you must place the keywork which is DONE somewhere in your response
            """
            #endregion
            
            # fill out our prompt
            out = self.log[-1]
            if "meow" in clean_response:
                """if the AI is slightly confused it can get its own log"""
                out = str(self.log)

            prompt = f"""your current target is still {target} your current last output was {out} if you want to see your full output logs put the word meow in your response""" # return last message with index -1
            clean_response = Agent.instanciate_agent(message, prompt, strip_markup=True) # check strip markup
            self.log.append(clean_response)
        print("scanning complete log available")
        
    def _get_log(self) -> list:
        return self.log
        
 