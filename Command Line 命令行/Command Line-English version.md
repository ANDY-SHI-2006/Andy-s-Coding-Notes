# 0 Command Line Cheatsheet

Quick reference for Windows CMD commands.

## 0.1 Navigation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `cd` | Change directory | `cd Documents` |
| `cd ..` | Go to parent directory | `cd ..` |
| `cd \` | Go to root directory | `cd \` |
| `dir` | List directory contents | `dir` |
| `pwd` (or `cd`) | Print working directory | `cd` |

## 0.2 File Operations

| Command | Description | Example |
|---------|-------------|---------|
| `type` | Display file contents | `type file.txt` |
| `copy` | Copy files | `copy file.txt backup.txt` |
| `move` | Move/rename files | `move file.txt newname.txt` |
| `del` | Delete files | `del file.txt` |
| `ren` | Rename files | `ren old.txt new.txt` |

## 0.3 Directory Operations

| Command | Description | Example |
|---------|-------------|---------|
| `mkdir` (or `md`) | Create directory | `mkdir NewFolder` |
| `rmdir` (or `rd`) | Remove empty directory | `rmdir OldFolder` |
| `rmdir /s` | Remove directory with contents | `rmdir /s folder` |
| `tree` | Display directory structure | `tree` |

## 0.4 System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `cls` | Clear screen | `cls` |
| `echo` | Display message | `echo Hello World` |
| `echo %VAR%` | Display environment variable | `echo %PATH%` |
| `set` | Set/display variables | `set NAME=value` |
| `pause` | Pause execution | `pause` |

## 0.5 Network Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ipconfig` | Display IP configuration | `ipconfig` |
| `ipconfig /all` | Detailed IP configuration | `ipconfig /all` |
| `ping` | Test network connection | `ping google.com` |
| `tracert` | Trace route | `tracert google.com` |
| `netstat` | Display network connections | `netstat` |

---

# 1 Command Line Basics

The Windows Command Prompt (CMD) is a command-line interpreter that allows users to interact with the operating system using text commands.

## 1.1 Opening Command Prompt

### 1.1.1 Methods to Open CMD

| Method | Steps |
|--------|-------|
| **Run dialog** | Press `Win + R`, type `cmd`, press Enter |
| **Start menu** | Search for "Command Prompt" or "cmd" |
| **File Explorer** | Type `cmd` in address bar, press Enter |
| **Right-click** | Shift + Right-click in folder → "Open command window here" |

### 1.1.2 Administrator Privileges

Some commands require elevated permissions:

1. Right-click "Command Prompt"
2. Select "Run as administrator"
3. Confirm UAC prompt

> **Note:** Administrator CMD shows "Administrator:" in the title bar.

## 1.2 Command Syntax

### 1.2.1 Basic Structure

```
command [options] [arguments]
```

| Component | Description | Example |
|-----------|-------------|---------|
| **Command** | The action to perform | `dir`, `copy`, `del` |
| **Options** | Modify command behavior | `/s`, `/q`, `/y` |
| **Arguments** | Targets of the command | `file.txt`, `C:\Users` |

### 1.2.2 Common Options

| Option | Meaning | Usage |
|--------|---------|-------|
| `/?` | Display help | `dir /?` |
| `/s` | Include subdirectories | `dir /s` |
| `/q` | Quiet mode (no prompts) | `del /q *.tmp` |
| `/y` | Answer yes to prompts | `copy /y file.txt` |
| `/a` | Show hidden files | `dir /a` |

### 1.2.3 Getting Help

```cmd
:: Display help for a command
command /?

:: Examples
dir /?
copy /?
mkdir /?
```

## 1.3 File Paths

### 1.3.1 Path Types

| Type | Description | Example |
|------|-------------|---------|
| **Absolute** | Full path from root | `C:\Users\John\Documents` |
| **Relative** | Path from current directory | `Documents\file.txt` |

### 1.3.2 Special Characters

| Character | Meaning | Example |
|-----------|---------|---------|
| `\` | Directory separator | `C:\Windows\System32` |
| `..` | Parent directory | `cd ..` |
| `.` | Current directory | `copy .\file.txt D:\` |
| `*` | Wildcard (any characters) | `del *.txt` |
| `?` | Wildcard (single character) | `file?.txt` |
| `""` | Quote spaces in paths | `cd "Program Files"` |

### 1.3.3 Path Examples

```cmd
:: Absolute path
cd C:\Users\John\Documents

:: Relative path (one level up)
cd ..\Pictures

:: Using wildcards
dir *.txt
doc*.doc
file?.txt

:: Paths with spaces (must quote)
cd "C:\Program Files\Java"
copy "my document.txt" D:\Backup\
```

---

# 2 Navigation Commands

Navigation commands allow you to move through the file system.

## 2.1 cd (Change Directory)

The `cd` command changes the current working directory.

### 2.1.1 Syntax

```cmd
cd [drive:][path]
cd [/d] [drive:][path]
```

### 2.1.2 Basic Usage

| Command | Description |
|---------|-------------|
| `cd Documents` | Enter subdirectory "Documents" |
| `cd ..` | Go to parent directory |
| `cd ..\..` | Go up two levels |
| `cd \` | Go to drive root |
| `cd /d D:\` | Change to D: drive |

### 2.1.3 Examples

```cmd
:: Navigate to specific folder
cd C:\Users\John\Documents

:: Navigate up one level
cd ..

:: Navigate to root
cd \

:: Change drive (use /d switch)
cd /d D:\Games

:: Just typing drive letter also works
D:
cd Games
```

## 2.2 dir (Directory Listing)

The `dir` command displays the contents of a directory.

### 2.2.1 Syntax

```cmd
dir [drive:][path][filename] [/a[[:]<attributes>]] [/b] [/s] [/w]
```

### 2.2.2 Common Options

| Option | Description |
|--------|-------------|
| `/a` | Display files with specified attributes |
| `/b` | Bare format (filenames only) |
| `/s` | Include subdirectories |
| `/w` | Wide format (multiple columns) |
| `/o` | Sort by name |
| `/t:w` | Sort by modified time |

### 2.2.3 Examples

```cmd
:: Basic listing
dir

:: List all files including hidden
dir /a

:: List with subdirectories
dir /s

:: Bare format (for batch processing)
dir /b

:: Wide format
dir /w

:: Sort by date
dir /t:w /o:-d

:: List only .txt files
dir *.txt

:: List files in specific directory
dir C:\Windows\System32\*.dll
```

## 2.3 tree (Directory Structure)

The `tree` command displays the directory structure in a tree-like format.

### 2.3.1 Syntax

```cmd
tree [drive:][path] [/f] [/a]
```

### 2.3.2 Options

| Option | Description |
|--------|-------------|
| `/f` | Display filenames in each directory |
| `/a` | Use ASCII characters instead of extended characters |

### 2.3.3 Examples

```cmd
:: Display directory tree
tree

:: Display tree with files
tree /f

:: Save tree to file
tree /f > structure.txt
```

---

# 3 File Operations

File operation commands create, view, copy, move, and delete files.

## 3.1 type (Display File Contents)

The `type` command displays the contents of a text file.

### 3.1.1 Syntax

```cmd
type [drive:][path]filename
```

### 3.1.2 Examples

```cmd
:: Display file contents
type readme.txt

:: Display with more (paged)
type longfile.txt | more

:: Concatenate multiple files
type file1.txt file2.txt > combined.txt
```

> **Note:** `type` is for text files. For binary files, use `more` or `findstr`.

## 3.2 copy (Copy Files)

The `copy` command copies one or more files.

### 3.2.1 Syntax

```cmd
copy [/y | /-y] source destination
copy source1 + source2 destination
```

### 3.2.2 Options

| Option | Description |
|--------|-------------|
| `/y` | Suppress overwrite confirmation |
| `/-y` | Prompt for overwrite confirmation |
| `/v` | Verify file was written correctly |

### 3.2.3 Examples

```cmd
:: Copy single file
copy file.txt D:\Backup\

:: Copy with new name
copy file.txt D:\Backup\backup.txt

:: Copy multiple files
copy *.txt D:\Backup\

:: Copy and rename
copy report.txt "2024-03-25_report.txt"

:: Concatenate files
copy file1.txt + file2.txt combined.txt

:: Force overwrite without prompt
copy /y file.txt D:\Backup\

:: Copy to current directory (from another location)
copy C:\Users\John\Desktop\file.txt .
```

## 3.3 move (Move/Rename Files)

The `move` command moves files or renames them.

### 3.3.1 Syntax

```cmd
move [/y | /-y] source destination
```

### 3.3.2 Examples

```cmd
:: Move file to another folder
move file.txt D:\Archive\

:: Rename file
move oldname.txt newname.txt

:: Move multiple files
move *.log D:\Logs\

:: Move without confirmation
move /y file.txt D:\Destination\
```

> **Note:** `move` overwrites existing files without warning by default. Use `/-y` to prompt.

## 3.4 del (Delete Files)

The `del` command deletes one or more files.

### 3.4.1 Syntax

```cmd
del [/p] [/f] [/s] [/q] [/a[[:]<attributes>]] names
```

### 3.4.2 Options

| Option | Description |
|--------|-------------|
| `/p` | Prompt for confirmation before deleting |
| `/f` | Force delete read-only files |
| `/s` | Delete from subdirectories |
| `/q` | Quiet mode (no confirmation) |
| `/a` | Delete files with specified attributes |

### 3.4.3 Examples

```cmd
:: Delete single file
del file.txt

:: Delete with confirmation
del /p file.txt

:: Delete multiple files
del *.tmp

:: Force delete read-only files
del /f readonly.txt

:: Delete from subdirectories
del /s *.bak

:: Quiet delete (no prompts)
del /q *.log

:: Delete hidden files
del /a:h hidden.txt
```

> **Warning:** Deleted files are NOT sent to Recycle Bin. They are permanently deleted!

## 3.5 ren (Rename Files)

The `ren` (rename) command renames files.

### 3.5.1 Syntax

```cmd
ren [drive:][path]filename1 filename2
```

### 3.5.2 Examples

```cmd
:: Rename single file
ren old.txt new.txt

:: Rename with wildcards
ren *.txt *.bak

:: Rename in specific directory
ren C:\Temp\file.txt newname.txt
```

---

# 4 Directory Operations

Directory operation commands create and remove directories.

## 4.1 mkdir/md (Make Directory)

The `mkdir` (or `md`) command creates new directories.

### 4.1.1 Syntax

```cmd
mkdir [drive:]path
md [drive:]path
```

### 4.1.2 Examples

```cmd
:: Create single directory
mkdir NewFolder

:: Create nested directories
mkdir C:\Users\John\Documents\Projects\2024

:: Create multiple directories at once
mkdir Folder1 Folder2 Folder3

:: Create path with spaces (quote it)
mkdir "C:\My Projects\New Folder"
```

## 4.2 rmdir/rd (Remove Directory)

The `rmdir` (or `rd`) command removes directories.

### 4.2.1 Syntax

```cmd
rmdir [/s] [/q] [drive:]path
rd [/s] [/q] [drive:]path
```

### 4.2.2 Options

| Option | Description |
|--------|-------------|
| `/s` | Remove directory and all contents (subdirectories and files) |
| `/q` | Quiet mode (no confirmation) |

### 4.2.3 Examples

```cmd
:: Remove empty directory
rmdir EmptyFolder

:: Remove directory with contents
rmdir /s FolderWithContents

:: Force remove without confirmation
rmdir /s /q OldFolder

:: Multiple directories
rmdir Folder1 Folder2
```

> **Warning:** `/s /q` permanently deletes all contents. Be very careful!

---

# 5 System Information

System commands display information about the computer and control command execution.

## 5.1 System Commands

### 5.1.1 echo (Display Messages)

The `echo` command displays messages or toggles command echoing.

```cmd
:: Display text
echo Hello World

:: Display variable
echo %USERNAME%
echo %PATH%

:: Create or modify file
echo This is a line > file.txt
echo Another line >> file.txt

:: Turn off command display in batch files
@echo off

:: Display blank line
echo.
```

### 5.1.2 Environment Variables

| Variable | Description |
|----------|-------------|
| `%USERNAME%` | Current user name |
| `%USERPROFILE%` | User profile directory |
| `%PATH%` | System PATH variable |
| `%TEMP%` | Temporary directory |
| `%SYSTEMROOT%` | Windows directory |
| `%CD%` | Current directory |
| `%DATE%` | Current date |
| `%TIME%` | Current time |

### 5.1.3 set (Set Variables)

```cmd
:: Display all environment variables
set

:: Display specific variable
set PATH

:: Create variable
set MYVAR=Hello

:: Use variable
echo %MYVAR%

:: Remove variable
set MYVAR=
```

### 5.1.4 cls (Clear Screen)

```cmd
:: Clear command prompt screen
cls
```

### 5.1.5 pause (Pause Execution)

```cmd
:: Pause and wait for key press
pause

:: Custom message
pause Press any key to continue...
```

## 5.2 System Information Commands

| Command | Description |
|---------|-------------|
| `ver` | Display Windows version |
| `vol` | Display volume label |
| `systeminfo` | Detailed system information |
| `hostname` | Display computer name |
| `whoami` | Display current user |
| `date /t` | Display current date |
| `time /t` | Display current time |

### 5.2.1 Examples

```cmd
:: Windows version
ver

:: Computer name
hostname

:: Current user
whoami

:: Detailed system info
systeminfo

:: Disk volume label
vol C:
```

---

# 6 Network Commands

Network commands diagnose and display network configuration.

## 6.1 ipconfig (IP Configuration)

The `ipconfig` command displays network configuration.

### 6.1.1 Syntax

```cmd
ipconfig [/all] [/release] [/renew] [/flushdns]
```

### 6.1.2 Options

| Option | Description |
|--------|-------------|
| `/all` | Display detailed configuration |
| `/release` | Release IP address (DHCP) |
| `/renew` | Renew IP address (DHCP) |
| `/flushdns` | Clear DNS cache |
| `/displaydns` | Display DNS cache |

### 6.1.3 Examples

```cmd
:: Basic IP configuration
ipconfig

:: Detailed configuration
ipconfig /all

:: Release and renew IP
ipconfig /release
ipconfig /renew

:: Clear DNS cache
ipconfig /flushdns
```

## 6.2 ping (Test Connectivity)

The `ping` command tests network connectivity to a host.

### 6.2.1 Syntax

```cmd
ping [-t] [-n count] [-l size] target
```

### 6.2.2 Options

| Option | Description |
|--------|-------------|
| `-t` | Ping continuously (Ctrl+C to stop) |
| `-n count` | Number of pings |
| `-l size` | Packet size in bytes |
| `-a` | Resolve addresses to hostnames |

### 6.2.3 Examples

```cmd
:: Ping default (4 times)
ping google.com

:: Ping specific count
ping -n 10 8.8.8.8

:: Continuous ping
ping -t google.com

:: Ping with specific packet size
ping -l 1024 google.com

:: Ping localhost (test local TCP/IP)
ping 127.0.0.1
```

## 6.3 tracert (Trace Route)

The `tracert` command traces the route to a destination.

### 6.3.1 Syntax

```cmd
tracert [-d] [-h maximum_hops] target
```

### 6.3.2 Examples

```cmd
:: Trace route to Google
tracert google.com

:: Maximum 30 hops
tracert -h 30 example.com

:: Don't resolve hostnames (faster)
tracert -d 8.8.8.8
```

## 6.4 netstat (Network Statistics)

The `netstat` command displays network connections.

### 6.4.1 Syntax

```cmd
netstat [-a] [-b] [-n] [-o] [-p protocol]
```

### 6.4.2 Options

| Option | Description |
|--------|-------------|
| `-a` | Display all connections and listening ports |
| `-b` | Display executable names |
| `-n` | Display addresses numerically |
| `-o` | Display process IDs |
| `-p` | Show connections for specific protocol |

### 6.4.3 Examples

```cmd
:: Display active connections
netstat

:: All connections with process IDs
netstat -ano

:: Display by protocol
netstat -p tcp

:: Display executable names (requires admin)
netstat -b
```

## 6.5 Other Network Commands

| Command | Description | Example |
|---------|-------------|---------|
| `nslookup` | Query DNS | `nslookup google.com` |
| `route` | View/edit routing table | `route print` |
| `arp` | Display ARP cache | `arp -a` |
| `telnet` | Test port connectivity | `telnet host port` |
| `getmac` | Display MAC address | `getmac` |

---

# 7 Advanced Topics

## 7.1 Redirection Operators

Redirection operators control input/output streams.

| Operator | Description | Example |
|----------|-------------|---------|
| `>` | Redirect output to file (overwrite) | `dir > files.txt` |
| `>>` | Redirect output to file (append) | `echo line >> file.txt` |
| `<` | Redirect input from file | `command < input.txt` |
| `|` | Pipe output to another command | `dir | more` |
| `2>` | Redirect errors | `command 2> errors.txt` |

### 7.1.1 Examples

```cmd
:: Save directory listing to file
dir > files.txt

:: Append to file
echo New line >> log.txt

:: Pipe to more (paged output)
dir | more

:: Pipe to find
dir | find "txt"

:: Redirect errors
command 2> error.log

:: Redirect output and errors
command > output.txt 2>&1
```

## 7.2 Batch File Basics

Batch files (.bat) contain multiple CMD commands.

### 7.2.1 Basic Structure

```batch
@echo off
echo Hello World
echo Current date: %DATE%
pause
```

### 7.2.2 Common Batch Commands

| Command | Description |
|---------|-------------|
| `@echo off` | Don't display commands |
| `echo.` | Blank line |
| `pause` | Wait for key press |
| `goto` | Jump to label |
| `if` | Conditional execution |
| `for` | Loop through items |

### 7.2.3 Simple Batch File Example

```batch
@echo off
echo ===================================
echo    System Information Report
echo ===================================
echo.
echo Computer: %COMPUTERNAME%
echo User:     %USERNAME%
echo Date:     %DATE% %TIME%
echo.
echo --- Network Info ---
ipconfig | find "IPv4"
echo.
echo --- Disk Space ---
wmic logicaldisk get size,freespace,caption
echo.
pause
```

## 7.3 Useful Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Auto-complete file/folder names |
| `↑ / ↓` | Cycle through command history |
| `F7` | Show command history list |
| `Ctrl + C` | Cancel current command |
| `Ctrl + V` | Paste |
| `Ctrl + A` | Select all |
| `Ctrl + L` | Clear screen (same as `cls`) |
| `Esc` | Clear current line |
| `Ctrl + ←/→` | Jump word by word |
