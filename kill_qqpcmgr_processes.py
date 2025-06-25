import subprocess

def safe_run(cmd, ignore_errors=True):
    """Safely run a command and handle errors"""
    try:
        subprocess.run(cmd, stderr=subprocess.DEVNULL if ignore_errors else None)
        return True
    except Exception as e:
        print(f"Error running command {cmd}: {e}")
        return False

def kill_processes():
    print("Step 1: Stopping services...")
    services = [
        'com.tencent.QQPCMgr',
        'com.tencent.QQPCMgrDaemon',
        'com.tencent.QQPCPolicyMgr'
    ]
    
    for service in services:
        safe_run(['sudo', 'launchctl', 'unload', '-w', f'/Library/LaunchDaemons/{service}.plist'])
        safe_run(['sudo', 'launchctl', 'unload', '-w', f'/Library/LaunchAgents/{service}.plist'])
    
    print("Step 2: Terminating processes...")
    processes = [
        'QQPCWatermark',
        'QQPCMgr',
        'QQPCMgrDaemon',
        'QQPCPolicyMgr',
        'NetworkServiceMgr',
        'tav',
        'runmgr'
    ]
    
    try:
        ps_output = subprocess.check_output(['ps', '-ef']).decode()
        for process in processes:
            for line in ps_output.split('\n'):
                if process in line and not 'grep' in line:
                    try:
                        pid = line.split()[1]
                        print(f"Killing process {process} with PID {pid}")
                        safe_run(['sudo', 'kill', '-9', pid])
                    except:
                        continue
    except Exception as e:
        print(f"Error getting process list: {e}")

if __name__ == '__main__':
    kill_processes()
    print("Process termination completed.")