import clr
import os
import json
import fnmatch

clr.AddReference('mscorlib')
clr.AddReference('System')
clr.AddReference('System.Security')

from System.IO import File, DirectoryInfo
from System.Security.AccessControl import FileSystemAccessRule, FileSystemRights, AccessControlType
from System.Security.AccessControl import RegistryAccessRule, RegistryRights
from Microsoft.Win32 import Registry
from System import Type

def get_acl(path: str) -> str:
    """
    Retrieves the Access Control List (ACL) information for a given file, directory, or registry key.

    Args:
    path (str): The path to the file, directory, or registry key.

    Returns:
    str: A JSON string containing the ACL information, including owner, group, and access rules.
    """

    security_info = {
        "Owner": "",
        "Group": "",
        "AccessRules": []
    }

    if os.path.exists(path):  # Check if it's a file or directory
        try:
            if os.path.isdir(path):
                info = DirectoryInfo(path)  # type: DirectoryInfo
            else:
                info = File(path)  # type: File
            acl = info.GetAccessControl()  # type: AccessControl
            type = "FileSystemRights"
        except Exception as e:
            print(f"Failed to get ACL for file or directory: {e}")
            return json.dumps({})
    else:  # Assume it's a registry key
        try:
            subkey_path = path.replace("HKEY_LOCAL_MACHINE\\", "")
            key = Registry.LocalMachine.OpenSubKey(subkey_path, False)  # type: RegistryKey
            if key is None:
                raise Exception("Registry key does not exist")
            acl = key.GetAccessControl()  # type: AccessControl
            type = "RegistryRights"
        except Exception as e:
            print(f"Failed to get ACL for registry key: {e}")
            return json.dumps({})

    try:
        owner = acl.GetOwner(Type.GetType("System.Security.Principal.NTAccount"))  # type: NTAccount
        security_info["Owner"] = str(owner)
        group = acl.GetGroup(Type.GetType("System.Security.Principal.NTAccount"))  # type: NTAccount
        security_info["Group"] = str(group)

        for rule in acl.GetAccessRules(True, True, Type.GetType("System.Security.Principal.NTAccount")):
            rule_dict = {
                "IdentityReference": rule.IdentityReference.Value,
                type: rule.FileSystemRights.ToString() if type == "FileSystemRights" else rule.RegistryRights.ToString(),
                "AccessControlType": rule.AccessControlType.ToString(),
                "InheritanceFlags": rule.InheritanceFlags.ToString(),
                "PropagationFlags": rule.PropagationFlags.ToString()
            }
            security_info["AccessRules"].append(rule_dict)
    except Exception as e:
        print(f"Failed to process ACL: {e}")

    return security_info

# Example usage of get_acl
path = r"C:/"  # Change this path to a file, directory, or registry key
acl_info = get_acl(path)
print(acl_info)

