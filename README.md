# ♻️ py-recycler
**py-recycler** is a lightweight command-line utility for Windows that lets you send files or
folders either to a temporary buffer bin or directly to the Windows Recycle Bin.  

## 🚀 Installation
+ Download the latest release.
+ Extract it to any directory of your choice (⚠️ The path should
  not contain space).
+ Add that directory to your system `PATH`.  

## 📋 System Requirements
### 🐍 Python  
- Requires **Python 3.11+**, as it relies on the built-in `tomllib` module for reading TOML configuration files.  
- Also requires the [`tomli-w`](https://pypi.org/project/tomli-w/) package for writing TOML files. Install it with:  
```bash
pip install tomli-w
```

### 🔐 Execution Policy
In some cases, you may need to adjust the PowerShell *ExecutionPolicy* settings to allow the script to run.

## 🛠️ Usage
### ♻️ Recycle Files/folders
Recycle files/folders to the **buffer bin** 🗂️ or directly to the **Windows Recycle Bin** 🗑️.  
(Default behavior is defined in `config.toml` 📄).  
Use `-b` to reverse the default option:  
```bash
rc <file/folder> [<file/folder> ...]
```

### 🗑️ Empty the Buffer Bin
Send everything in the buffer bin to the **Windows Recycle Bin** 🗑️.  
⚠️ Files/folders sent to the recycle bin cannot be recovered with this program:
```bash
rc [-e | --empty=<true/false>]
```
### 💥 Permanently Delete
⚠️ **PERMANENTLY** deletes all files/folders in the **Windows Recycle Bin** 🗑️ (use with caution!):
```bash
rc [-x | --emptyrecycle=<true/false>]
```

### ⚙️ Configuration
Modify the configuration file (`config.toml` 📄):
- No arguments → prints the full config
- Name only → prints that value
- Name + value → updates the config
```bash
rc [-c | --config=<true/false>] [<name> <value>]
```

### 🔄 Recover Files
Recover files/folders from the buffer bin.
If none specified, restores the **last** item sent to the buffer bin:
```bash
rc [-r | --recovery=<true/false>] [<file/folder> ...]
```

### 👀 View Buffer Bin
Show files/folders currently in the buffer bin.
If none specified, lists all items:
```bash
rc [-v | --view=<true/false>] [<file/folder> ...]
```

### 📖 Help
Display the help message:
```bash
rc [-h | --help=<true/false>]
```
### ⚡ Additional Options
```bash
[-s | --silent=<true/false>]   # Run without prompts  
[-l | --log=<true/false>]      # Enable/disable logging  
[-y | --yes=<true/false>]      # Auto-confirm actions  
[-b | --buffer=<true/false>]   # Switch buffer/recycle mode
```



