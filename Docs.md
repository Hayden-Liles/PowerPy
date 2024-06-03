#
## `get_acl`

### Description
Retrieves the Access Control List (ACL) information for a specified file, directory, or registry key. This function can optionally include audit rules in the returned data.

### Parameters
- **path** (`str`): The file system path or registry key path for which to retrieve ACL information.
- **include_audit** (`bool`, optional): If set to `True`, the function will include audit rules in the returned data. Defaults to `False`.

### Returns
- **dict**: A dictionary containing detailed ACL information, including owner, group, access rules, and optionally audit rules. If an error occurs, it raises an exception with a descriptive message.

### Example Usage
python path = r"C:/Users/Hayden/OneDrive/Desktop/acltest" acl_info = get_acl(path, include_audit=True) print(acl_info)

#
## `set_acl`

### Description
Sets the Access Control List (ACL) for a specified file, directory, or registry key based on the provided ACL data. This function can modify both access and audit rules.

### Parameters
- **path** (`str`): The file system path or registry key path for which to set ACL information.
- **acl_data** (`dict`): A dictionary containing the ACL data to apply. This data should include details about access rules and optionally audit rules.

### Returns
- **None**: This function does not return a value. It directly modifies the ACL of the specified path. If an error occurs, it raises an exception with a descriptive message.

### Example Usage
python path = r"C:/Users/Hayden/OneDrive/Desktop/acltest" acl_info = get_acl(path, include_audit=True) set_acl(path, acl_info)


### Exceptions
- **ArgumentException**: Raised if there is an issue with the arguments provided to the .NET methods used within the function.
- **Exception**: General exceptions that may occur during the execution of the function, providing a message with the error details.

## Notes
- Ensure that the script is run with appropriate permissions, as modifying ACLs requires administrative privileges on most systems.
