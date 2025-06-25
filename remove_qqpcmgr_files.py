import subprocess
import os

def expand_path(path):
    """Expand ~ to user's home directory"""
    return os.path.expanduser(path)

def safe_run(cmd, ignore_errors=True):
    """Safely run a command and handle errors"""
    try:
        subprocess.run(cmd, stderr=subprocess.DEVNULL if ignore_errors else None)
        return True
    except Exception as e:
        print(f"Error running command {cmd}: {e}")
        return False

def remove_files():
    print("Removing QQPCMgr files...")
    files_to_remove = [
        '/Library/QQPCMgr.localized',
        '/Library/Application Support/QQPCiOA/',
        '/private/tmp/iOALog/QQPCMgr.log',
        '/Library/Application Support/QQPCiOA',
        '/private/tmp/qqpcmgr{81F340E1-5407-4807-BDEA-52C17CE1EEBA}',
        '/Applications/QQPCMgr.localized',
        '/Library/LaunchDaemons/com.tencent.QQPCMgr.plist',
        '/Library/LaunchAgents/com.tencent.QQPCMgr.plist',
        '~/Library/Preferences/com.tencent.QQPCMgr.plist',
        '~/Library/Caches/com.tencent.QQPCMgr',
        '~/Library/Saved Application State/com.tencent.QQPCMgr.savedState'
    ]

    for file in files_to_remove:
        expanded_path = expand_path(file)
        print(f"Removing {expanded_path}...")
        if safe_run(['sudo', 'rm', '-rf', expanded_path]):
            print(f"Successfully removed {expanded_path}")
        else:
            print(f"Failed to remove {expanded_path}")

    print("\nRemoving ports...")
    ports_to_remove = ['57399', '58827']
    for port in ports_to_remove:
        if safe_run(['sudo', 'pfctl', '-F', 'nat', '-a', f'com.apple/250.{port}']):
            print(f"Cleaned up port {port}")
        else:
            print(f"Failed to clean up port {port}")

if __name__ == '__main__':
    remove_files()
    print("\nFile removal completed.")