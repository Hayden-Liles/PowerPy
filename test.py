import subprocess
import os
import sys
import ctypes
from typing import Union
import time

import subprocess
import os
import sys
import ctypes
from typing import Union
import time

# SECTION Custom Variable for Intellisense

file_path = Union[str, os.PathLike]

# SECTION Functions

def run_powershell_command(command: str):
    """
    Executes a PowerShell command and prints the output or error.

    Args:
        command (str): The PowerShell command to be executed.

    Returns:
        None
    """
    completed_process = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    if completed_process.returncode != 0:
        print("An error occurred:", completed_process.stderr)
    else:
        print("Command executed successfully:", completed_process.stdout)

def is_admin() -> bool:
    """
    Checks if the script is running with administrative privileges.

    Returns:
        bool: True if the script has administrative privileges, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """
    Attempts to relaunch the script with administrative privileges and exits the current script.

    Returns:
        None
    """
    if not is_admin():
        print("Requesting administrative privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def check_for_admin():
    """
    Checks for administrative privileges and attempts to restart the script with them if not already an admin.

    Returns:
        None
    """
    if not is_admin():
        run_as_admin()

def parse_acl_output(output: str) -> dict[str, Union[str, list[str]]]:
    """
    Parses the output from the Get-Acl command into a structured dictionary.

    Args:
        output (str): The raw string output from the Get-Acl command.

    Returns:
        Dict[str, Union[str, List[str]]]: A dictionary containing the parsed ACL data.
    """
    lines = output.split('\n')
    acl_dict = {}
    current_key = None
    current_values = []

    for line in lines:
        if ':' in line:
            if current_key is not None:
                acl_dict[current_key] = current_values if len(current_values) > 1 else current_values[0]
            split_line = line.split(':', 1)
            current_key = split_line[0].strip()
            current_values = [split_line[1].strip()]
        else:
            current_values.append(line.strip())

    if current_key is not None:
        acl_dict[current_key] = current_values if len(current_values) > 1 else current_values[0]

    return acl_dict

def get_permissions(path: file_path, filter: str = None, include: str = None, exclude: str = None, audit: bool = False, use_transaction: bool = False) -> dict[str, Union[str, list[str]]]:
    command = f"Get-Acl -Path '{path}'"
    if filter:
        command += f" -Filter '{filter}'"
    if include:
        command += f" -Include '{include}'"
    if exclude:
        command += f" -Exclude '{exclude}'"
    if audit:
        command += " -Audit"
    if use_transaction:
        command = f"Start-Transaction; {command} -UseTransaction; Commit-Transaction"
    
    result = subprocess.run(["powershell.exe", "-Command", command + " | Format-List"], capture_output=True, text=True)
    if result.returncode != 0:
        if "PrivilegeNotHeldException" in result.stderr:
            check_for_admin()
            raise Exception("The script requires additional privileges to access audit information. Please run as Administrator.")
        else:
            raise Exception(f"PowerShell Command Failed: {result.stderr}")
    return parse_acl_output(result.stdout)



check_for_admin()

print(get_permissions("./.ve", None, None, None, False))
while(1 == 1):
    time.sleep(10)
    print()