import clr
import os
import json

clr.AddReference('mscorlib')
clr.AddReference('System')
clr.AddReference('System.Security')

from System import Type, ArgumentException, Enum
from System.IO import File, DirectoryInfo
from System.Security.AccessControl import (
    FileSystemAccessRule, FileSystemRights, AccessControlType,
    RegistryAccessRule, RegistryRights, AuditRule, AuditFlags,
    InheritanceFlags, PropagationFlags
)
from Microsoft.Win32 import Registry

def parse_enum(enum_type, value):
    try:
        return Enum.Parse(enum_type, value)
    except ArgumentException:
        raise ValueError(f"Invalid value '{value}' for enum type '{enum_type}'")

def process_rules(rules, rights_type):
    return [
        {
            "IdentityReference": rule.IdentityReference.Value,
            rights_type: rule.FileSystemRights.ToString() if rights_type == "FileSystemRights" else rule.RegistryRights.ToString(),
            "AccessControlType": rule.AccessControlType.ToString(),
            "InheritanceFlags": rule.InheritanceFlags.ToString(),
            "PropagationFlags": rule.PropagationFlags.ToString()
        }
        for rule in rules
    ]

def get_acl(path: str, include_audit: bool = False) -> dict:
    security_info = {"Owner": "", "Group": "", "AccessRules": [], "AuditRules": [] if include_audit else None}
    try:
        info = DirectoryInfo(path) if os.path.isdir(path) else File(path)
        acl = info.GetAccessControl()
        rights_type = "FileSystemRights" if os.path.exists(path) else "RegistryRights"
        security_info.update({
            "Owner": str(acl.GetOwner(Type.GetType("System.Security.Principal.NTAccount"))),
            "Group": str(acl.GetGroup(Type.GetType("System.Security.Principal.NTAccount"))),
            "AccessRules": process_rules(acl.GetAccessRules(True, True, Type.GetType("System.Security.Principal.NTAccount")), rights_type),
            "AuditRules": process_rules(acl.GetAuditRules(True, True, Type.GetType("System.Security.Principal.NTAccount")), rights_type) if include_audit else None
        })
    except Exception as e:
        raise Exception(f"Failed to retrieve or process ACL: {e}")

    return security_info

def set_acl(path: str, acl_data: dict):
    try:
        info = DirectoryInfo(path) if os.path.isdir(path) else File(path)
        acl = info.GetAccessControl()
        for rule in acl_data.get("AccessRules", []):
            rights_type = FileSystemRights if 'FileSystemRights' in rule else RegistryRights
            access_rule = FileSystemAccessRule(
                rule['IdentityReference'],
                parse_enum(rights_type, rule['FileSystemRights'] if 'FileSystemRights' in rule else rule['RegistryRights']),
                parse_enum(InheritanceFlags, rule['InheritanceFlags']),
                parse_enum(PropagationFlags, rule['PropagationFlags']),
                parse_enum(AccessControlType, rule['AccessControlType'])
            )
            acl.AddAccessRule(access_rule)
        if acl_data.get("AuditRules"):
            for rule in acl_data["AuditRules"]:
                rights_type = FileSystemRights if 'FileSystemRights' in rule else RegistryRights
                audit_rule = AuditRule(
                    rule['IdentityReference'],
                    parse_enum(rights_type, rule['FileSystemRights'] if 'FileSystemRights' in rule else rule['RegistryRights']),
                    parse_enum(AuditFlags, rule['AuditFlags'])
                )
                acl.AddAuditRule(audit_rule)
        info.SetAccessControl(acl)
    except ArgumentException as e:
        raise ArgumentException(f"Argument error: {e}")
    except Exception as e:
        raise Exception(f"Failed to set ACL: {e}")

path = r"C:/Users/liles/OneDrive/Desktop/acltest"
acl_info = get_acl(path, include_audit=True)
print(acl_info)
set_acl(path, acl_info)

