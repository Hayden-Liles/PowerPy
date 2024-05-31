import clr

clr.AddReference('System')
clr.AddReference('System.Security')

from System.Security.AccessControl import FileSystemAccessRule, FileSystemRights, AccessControlType
from System.IO import File
from System import Type  # Import Type from System namespace

def get_file_permissions(file_path):
    # Initialize an empty dictionary to hold the security information
    security_info = {
        "Owner": "",
        "Group": "",
        "AccessRules": []
    }

    # Get the current security settings
    file_security = File.GetAccessControl(file_path)

    # Retrieve and set the owner and group
    try:
        owner = file_security.GetOwner(Type.GetType("System.Security.Principal.NTAccount"))
        security_info["Owner"] = str(owner)
    except Exception as e:
        print(f"Failed to get owner: {e}")

    try:
        group = file_security.GetGroup(Type.GetType("System.Security.Principal.NTAccount"))
        security_info["Group"] = str(group)
    except Exception as e:
        print(f"Failed to get group: {e}")

    # Retrieve and append access rules to the dictionary
    try:
        for rule in file_security.GetAccessRules(True, True, Type.GetType("System.Security.Principal.NTAccount")):
            rule_dict = {
                "IdentityReference": rule.IdentityReference.Value,
                "FileSystemRights": rule.FileSystemRights.ToString(),
                "AccessControlType": rule.AccessControlType.ToString(),
                "InheritanceFlags": rule.InheritanceFlags.ToString(),
                "PropagationFlags": rule.PropagationFlags.ToString()
            }
            security_info["AccessRules"].append(rule_dict)
    except Exception as e:
        print(f"Failed to get access rules: {e}")

    return security_info

# Example usage
file_path = r"./main.py"
security_info = add_file_security(file_path)

print(security_info)
