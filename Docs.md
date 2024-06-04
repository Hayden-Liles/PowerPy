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
```python
path = r"C:/Users/Hayden/OneDrive/Desktop/acltest"
acl_info = get_acl(path, include_audit=True)
print(acl_info)
```

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
```python
path = r"C:/Users/Hayden/OneDrive/Desktop/acltest"
acl_info = get_acl(path, include_audit=True)
set_acl(path, acl_info)
```


### Exceptions
- **ArgumentException**: Raised if there is an issue with the arguments provided to the .NET methods used within the function.
- **Exception**: General exceptions that may occur during the execution of the function, providing a message with the error details.

## Notes
- Ensure that the script is run with appropriate permissions, as modifying ACLs requires administrative privileges on most systems.

#
## `get_appv_packages`

### Description
Executes a PowerShell command to retrieve information about App-V client packages installed on the system. The function returns a list of dictionaries, each representing a package with its name, version, package ID, and version ID.

### Returns
- **list**: A list of dictionaries where each dictionary represents an App-V package with keys: `Name`, `Version`, `PackageId`, and `VersionId`. If an error occurs during the execution of the PowerShell command, an empty list is returned.

### Example Usage
```python 
appv_packages = get_appv_packages()
for package in appv_packages: 
    print(package['Name'], package['Version'])
```

#
## `get_appx_packages`

### Description
Executes a PowerShell command to retrieve information about AppX packages installed on the system. The function returns a list of dictionaries, each representing a package with its name, publisher, architecture, and install location.

### Returns
- **list**: A list of dictionaries where each dictionary represents an AppX package with keys: `Name`, `Publisher`, `Architecture`, and `InstallLocation`. If an error occurs during the execution of the PowerShell command, an empty list is returned.

### Example Usage
```python
appx_packages = get_appx_packages()
for package in appx_packages:
    print(package['Name'], package['Publisher'])
```

