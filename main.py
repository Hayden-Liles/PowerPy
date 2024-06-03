import clr
import os
import json

clr.AddReference('mscorlib')
clr.AddReference('System')
clr.AddReference('System.Security')

from System.IO import File, DirectoryInfo
from System.Security.AccessControl import (
    FileSystemAccessRule, FileSystemRights, AccessControlType,
    AuditRule, AuditFlags
)
from System.Security.AccessControl import RegistryAccessRule, RegistryRights
from Microsoft.Win32 import Registry
from System import Type

def process_rules(rules, rights_type):
    rules_list = []
    for rule in rules:
        rule_dict = {
            "IdentityReference": rule.IdentityReference.Value,
            rights_type: rule.FileSystemRights.ToString() if rights_type == "FileSystemRights" else rule.RegistryRights.ToString(),
            "AccessControlType": rule.AccessControlType.ToString(),
            "InheritanceFlags": rule.InheritanceFlags.ToString(),
            "PropagationFlags": rule.PropagationFlags.ToString()
        }
        rules_list.append(rule_dict)
    return rules_list

def get_acl(path: str, include_audit: bool = False) -> str:
    security_info = {
        "Owner": "",
        "Group": "",
        "AccessRules": [],
        "AuditRules": [] if include_audit else None
    }

    try:
        if os.path.exists(path):
            info = DirectoryInfo(path) if os.path.isdir(path) else File(path)
            acl = info.GetAccessControl()
            rights_type = "FileSystemRights"
        else:
            subkey_path = path.replace("HKEY_LOCAL_MACHINE\\", "")
            key = Registry.LocalMachine.OpenSubKey(subkey_path, False)
            if key is None:
                raise Exception("Registry key does not exist")
            acl = key.GetAccessControl()
            rights_type = "RegistryRights"

        security_info["Owner"] = str(acl.GetOwner(Type.GetType("System.Security.Principal.NTAccount")))
        security_info["Group"] = str(acl.GetGroup(Type.GetType("System.Security.Principal.NTAccount")))
        security_info["AccessRules"] = process_rules(acl.GetAccessRules(True, True, Type.GetType("System.Security.Principal.NTAccount")), rights_type)

        if include_audit:
            security_info["AuditRules"] = process_rules(acl.GetAuditRules(True, True, Type.GetType("System.Security.Principal.NTAccount")), rights_type)

    except Exception as e:
        print(f"Failed to retrieve or process ACL: {e}")
        return json.dumps({})

    return json.dumps(security_info)

# Example usage of get_acl
path = r"C:/"  # Change this path to a file, directory, or registry
acl_info = get_acl(path, include_audit=True)
print(acl_info)
