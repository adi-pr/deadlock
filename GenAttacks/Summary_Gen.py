## - This module is designed to summarise stdout from our scanners into a list of cves
import boto3
import json
import re
from time import sleep
import subprocess
from pathlib import Path
from . import Agent
def generate_summary(stdout="") -> bool:
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
    
def test_functionality() -> bool:
    testcase = """- Nikto v2.5.0
    ---------------------------------------------------------------------------
    + Target IP:          192.168.1.10
    + Target Hostname:    example.com
    + Target Port:        80
    + Start Time:         2026-02-03 14:12:45
    ---------------------------------------------------------------------------
    + Server: Apache/2.4.49 (Unix)
    + The anti-clickjacking X-Frame-Options header is not present.
    + The X-XSS-Protection header is not defined.
    + The X-Content-Type-Options header is not set.

    + Apache/2.4.49 appears to be vulnerable to CVE-2021-41773 (Path Traversal).
    + Apache/2.4.49 appears to be vulnerable to CVE-2021-42013 (Remote Code Execution).
    + OSVDB-3233: /icons/: Directory indexing is enabled.
    + /cgi-bin/test.cgi: CGI script found; possible command execution (CVE-2019-0232).

    + OpenSSL 1.0.2k-fips detected
    + OpenSSL 1.0.2k-fips is vulnerable to CVE-2016-2107
    + OpenSSL 1.0.2k-fips is vulnerable to CVE-2016-0800 (DROWN)

    + PHP/7.2.24 detected
    + PHP 7.2.24 is vulnerable to CVE-2019-11043 (NGINX + PHP-FPM RCE)

    + Uncommon header 'x-backend-server' found, with contents: web01
    + Retrieved server banner: Apache/2.4.49 (Unix)
    ---------------------------------------------------------------------------
    + End Time:           2026-02-03 14:14:02
    + 1 host(s) tested
    """
    if generate_summary(testcase) == ['CVE-2021-41773', 'CVE-2021-42013', 'CVE-2019-0232', 'CVE-2016-2107', 'CVE-2016-0800', 'CVE-2019-11043']:
        print("Testcase Passed. code is working perfectly")
        return True
    else:
        return False