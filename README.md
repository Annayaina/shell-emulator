# Shell Emulator with VFS

UNIX-like shell emulator written in Python. 
All state lives in an in-memory virtual file system (VFS) loaded from an XML file.

## Features
- REPL with prompt `<vfs>:<cwd>$ ` (VFS name is always shown)
- Parser: command + arguments split by whitespace
- Commands: `ls`, `cd`, `exit`
- XML-based VFS; binary data via `base64`
- CLI options: `--vfs`, `--script`, `--debug`
- Error reporting for unknown commands, bad arguments, missing files and invalid XML

## CLI options
- `--vfs PATH` — Path to the VFS XML file (required)
- `--script PATH` — Path to the startup script
- `--debug` — Print all parameters before starting

## How to run
```powershell
.\run.bat --vfs vfs\deep.xml --debug
.\run.bat --vfs vfs\deep.xml --script scripts\deep_startup.txt --debug
Author: Anna