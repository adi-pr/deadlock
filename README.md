```text
██████╗ ███████╗ █████╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝
██║  ██║█████╗  ███████║██║  ██║██║     ██║   ██║██║     █████╔╝ 
██║  ██║██╔══╝  ██╔══██║██║  ██║██║     ██║   ██║██║     ██╔═██╗ 
██████╔╝███████╗██║  ██║██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗
╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
```
# DeadLock CLI
- Deadlock is an AI-targeting Autonomous threat actor designed to highlight the threat of AI in the cyberspace
- Deadlock takes a single ip address and a target and mutates its attacks to optimise successful attacks on targets
- Please use this responsibly for its intended purpose of research

### Setup
> This system is currently focused for Kali linux but can work on any linux distro if correct modules are installed

```python
python3 -m venv [EnvironmentName]
pip install -r requirements.txt
python cli.py (--help)
```

- you need to set AWS_BEARER_TOKEN_BEDROCK in your environmental vars to use the AI functionality 

### Future features
- Link to metasploit auxilary payloads to generate confirmation of vulnerabilities
- Nmap scanning for autonomous port scanning
- server connection ability to run on AWS, Digitalocean instances with minimal setup to replicate Kali Environment
- Windows support 

<h3>LEGAL NOTICE</h3>
This material is provided solely for educational, research, and defensive purposes. It is intended to support learning, academic discussion, and the improvement of security awareness and protective technologies.
Any use of this material to conduct real‑world attacks, exploit systems, access data without authorization, disrupt services, or otherwise violate applicable laws or regulations is strictly prohibited. The authors and distributors do not condone, support, or encourage >  illegal, unethical, or malicious activity.
Users are solely responsible for ensuring that their use of this material complies with all applicable laws, regulations, and organizational policies. The authors and distributors disclaim any liability for misuse or unlawful application of the information provided.

