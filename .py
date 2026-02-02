import socket
import struct

def check_cve_2024_6387(target_ip):
    try:
        with socket.create_connection((target_ip, 22), timeout=5) as sock:
            packet = b'\x53\x53\x48\x2d\x32\x2e\x30\x2d\x4f\x70\x65\x6e\x53\x53\x48\x5f\x38\x2e\x39\x70\x31\x0d\x0a'
            sock.send(packet)
            response = sock.recv(1024)
            return b'SSH-2.0-OpenSSH_8.9p1' in response
    except:
        return False

def main(target_ip, cve_id):
    if cve_id == "CVE-2024-6387":
        return check_cve_2024_6387(target_ip)
    return False