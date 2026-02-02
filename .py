import socket
import subprocess
import sys

def scan_target(target_ip, cve_id):
    if cve_id == "CVE-2014-0160":
        try:
            result = subprocess.run(['sslscan', target_ip], capture_output=True, text=True, timeout=30)
            return "heartbleed" in result.stdout.lower()
        except:
            return False
    elif cve_id == "CVE-2017-0144":
        try:
            result = subprocess.run(['smbclient', '-L', target_ip, '-N'], capture_output=True, text=True, timeout=30)
            return "SMB1" in result.stdout
        except:
            return False
    else:
        return False

if __name__ == "__main__":
    target_ip = sys.argv[1]
    cve_id = sys.argv[2]
    print(scan_target(target_ip, cve_id))
