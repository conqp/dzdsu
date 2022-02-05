# DayZ dedicated server utilities
This python package provides utilities for hosting DayZ servers
on both Windows and Linux machines.

## Configuration
Servers are configured in a JSON file with the structure listed below.

### The server list
The outermost object defines key-value pairs of server names and server objects.
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ServerList",
    "description": "List of servers",
    "type": "object",
    "patternProperties": {
        "*": {
            "type": "Server"
        }
    }
}
```
### A single server
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Server",
    "description": "Configuration for a single server",
    "type": "object",
    "properties": {
        "basedir": {
            "description": "The path to the server's base directory",
            "type": "string"
        },
        "appId": {
            "description": "The server's Steam app ID",
            "type": "integer"
        },
        "params": {
            "description": "Additional parameters for the server",
            "type": "ServerParams"
        },
        "mods": {
            "description": "Mods for the server",
            "type": "ModList"
        },
        "serverMods": {
            "description": "Mods for the server only that are not propagated to clients",
            "type": "ModList"
        }
    },
    "required": ["basedir"]
}
```
### Server parameters
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ServerParams",
    "description": "Additional start parameters for a server",
    "type": "object",
    "properties": {
        "config": {
            "description": "The name of the config file to load",
            "type": "string"
        },
        "doLogs": {
            "description": "Add -doLogs flag",
            "type": "boolean"
        },
        "adminLog": {
            "description": "Add -adminLog flag",
            "type": "boolean"
        },
        "netLog": {
            "description": "Add -netLog flag",
            "type": "boolean"
        },
        "srcAllowFileWrite": {
            "description": "Add -srcAllowFileWrite flag",
            "type": "boolean"
        },
        "noFilePatching": {
            "description": "Add -noFilePatching flag",
            "type": "boolean"
        },
        "freezeCheck": {
            "description": "Add -freezeCheck flag",
            "type": "boolean"
        },
        "port": {
            "description": "Override port",
            "type": "integer"
        },
        "profiles": {
            "description": "Override profiles",
            "type": "string"
        },
        "cpuCount": {
            "description": "Override cpuCount",
            "type": "integer"
        }
    }
}
```
### Mods
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ModList",
    "description": "List of Mods",
    "type": "array",
    "items": {
        "type": "Mod"
    },
    "minItems": 0,
    "uniqueItems": true
}
```
```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Mod",
    "description": "A single Mod",
    "type": "object",
    "properties": {
        "id": {
            "description": "The steam workshop ID",
            "type": "integer"
        },
        "name": {
            "description": "A human-readable name",
            "type": "string"
        }
    },
    "required": ["id"]
}
```
#### Disable mods
Mods with IDs <= 0 will be filtered out.  
So you can disable mods on a server by prefixing their ID with `-`,  i.e. making the ID negative.

### Default file paths
The default servers file location differs based on the operating system.
#### Windows
On Windows the default servers file is expected to be under `%PROGRAMFILES%\dzsrv\servers.json`.
#### POSIX
On POSIX Systems the default servers file is expected to be under `/etc/dzservers.json`.

## Command line tools
The server utilities ship the two following command line programs:
### `dzdsw`
A wrapper script to start a dedicated server. Use
```shell
$ dzdsw -h
```
to get further information.
### `dzdsu`
A utility script to update a dedicated server and / or its mods. Use
```shell
$ dzdsu -h
```
to get further information.