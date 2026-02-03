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
        pass
    def _gen(self, stdout="") -> bool:
        # make sure filename is not empty
        """
        Docstring for generate_exploit
        
        :param cve_id: Identifying value for database of common vulnerability and exposure (CVE)
        :param target: Target IPv4 address
        :param maxRetries: Limit for how many times the AI can fail to attack (do not increase unless you want to lose money)
        :param filename: DO NOT CHANGE
        :param generate_type: you can change this to scanner or exploit or whatever your heart desires 
        :return: bool
        :rtype: bool
        """
        
        #region AI-Guardrails
        message = """You are a robot that takes a input stream from a terminal and returns a list of discovered vulnerabilities using CVE ids e.g. CVE-012-4243, CVE-015-2342
        If you output anything other than comma separated variables, the response is invalid.
        if you are given a vulnerability without a cve labeled you are to discover the matching CVE and add it to the list of comma separated variables to return
        Rules:
        - Never include <think>, </think>, or any reasoning text.
        - return comma separated variables e.g. CVE-012-4243, CVE-015-4234
        - return comma separated variables only in your response"""
        #endregion
        
        # fill out our prompty
        prompt = f"""Generate a list of comma separated variables of CVE identifiers for the output stream {stdout}"""
        clean_code = Agent.instanciate_agent(message, prompt, strip_markup=True) # check strip markup
        
        print(clean_code.split(','))
        return clean_code.split(',')
        
    def _test_functionality() -> bool:
        testcase = """"""
