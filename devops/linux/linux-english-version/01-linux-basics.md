[Next: Linux advanced ->](02-linux-advanced.md)

# 1 Linux Basics

> This chapter covers what Linux is, how to set it up in a virtual machine, and the essential commands you use every day.

## 1.1 What is an Operating System

Common operating systems: **Windows, macOS, Android, iOS, Linux**.

An operating system (OS) is system software that runs directly on the computer hardware. It controls the hardware **and** supports the software running on top of it.

> **Role of the OS** — it is the bridge between two layers: **down** it controls the hardware, **up** it manages the application software.

### Why learn Linux

| Reason | Explanation |
| --- | --- |
| Deploy your projects | After learning a web framework, you deploy it on a cloud server (Tencent Cloud, Alibaba Cloud, Huawei Cloud...) — usually Linux |
| Cheap & accessible | Student cloud servers (2 cores / 2 GB) cost roughly ¥70–99 per year |
| Remote from anywhere | Connect to your server over SSH from any machine |

---

## 1.2 Virtual Machines & VMware

A **virtual machine (VM)** simulates a real computer — a virtual PC inside your physical machine. The most common VM software is **VMware**.

### Installing VMware

1. Right-click the installer and choose **Run as administrator**.
2. Keep clicking **Next**; make sure the install path has enough space (avoid the C: drive if possible).
3. Enter a license key (widely available online), then finish.

---

## 1.3 Creating a Virtual Machine

1. Create a new VM in VMware and follow the wizard.
2. Before powering on, attach a **CD/DVD image** (the Ubuntu ISO).
3. Fast domestic mirror (Ubuntu 22.04): https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/22.04.5/
4. The first boot takes a while — be patient.
5. During setup: timezone **Shanghai**, and use an **English username** (no Chinese).
6. After setup, save the current state as a **snapshot** so you can restore it later.

> **Tip** — if an update prompt appears right after the first login, skip it.

---

## 1.4 The Terminal

### Shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl + +` | Zoom in |
| `Ctrl + -` | Zoom out |
| `F11` | Fullscreen |

### The command prompt

```bash
bb@computer:~$
```

| Part | Meaning |
| --- | --- |
| `bb` | Current username |
| `@computer` | Hostname of the machine |
| `~` | Current directory; `~` means your home directory (`/home/bb`) |
| `$` | Prompt of a normal user (`#` means root / superuser) |

Every user has their own home directory: `bb` → `/home/bb`, `root` → `/root`.

```bash
sudo passwd root   # first time: set the root password
su root            # switch to root
su bb              # switch back to the normal user
```

---

## 1.5 Command Format

```text
command [-options] [parameter]
```

| Part | Meaning | Example |
| --- | --- | --- |
| `command` | The command name | `cd`, `pwd`, `ls` |
| `[-options]` | Zero or more options (can be combined) | `-r`, `-la` |
| `[parameter]` | Zero or more arguments | `cd game` → `game` is the parameter |

> `[ ]` means **optional** — it is not part of what you actually type.

---

## 1.6 First Commands

| Command | Purpose |
| --- | --- |
| `who` | Show the current logged-in user |
| `pwd` | Print the current (absolute) directory |
| `cd` | Change directory |
| `ls` | List files and directories |
| `ifconfig` | Show network interface info (install `net-tools` first) |
| `ping` | Test connectivity between hosts |
| `touch` | Create an empty file |
| `mkdir` | Create a directory |
| `clear` | Clear the terminal (`Ctrl + L`) |
| `uname` | Show OS information |
| `uname -r` | Show the kernel release version |
| `exit` | Log out |
| `reboot` | Restart the system |
| `shutdown` | Shut down |

### Paths: relative vs absolute

```bash
cd folder     # enter a subdirectory (relative path)
cd ..         # go up one level
cd ~          # go to the user's home directory
cd /          # go to the root directory
```

| Type | Definition |
| --- | --- |
| Relative path | Starts from the **current** location |
| Absolute path | Starts with `/` (the root) |

### `ifconfig` needs `net-tools`

```bash
sudo apt-get update      # refresh package sources
sudo apt install net-tools
```

> `sudo` runs a command as administrator. `apt install net-tools` is like `pip install xxx` in Python.

If you hit a lock error (`/var/lib/dpkg/lock-frontend`), find and kill the process holding it:

```bash
sudo lsof /var/lib/dpkg/lock-frontend
sudo kill -9 PID
```

---

## 1.7 Command-Line Tips

| Tip | How |
| --- | --- |
| Autocomplete | Type a few letters, then press `Tab` |
| History | Up / Down arrows, or `history`; run `!N` to re-run command N |
| Stop a command | `Ctrl + C` |
| Help | `command --help` (e.g. `uname --help`) |

---

## 1.8 Directory Structure

Windows starts from drives (`C:`, `D:`...); Linux starts everything from a single **root** `/`.

```bash
ls /
```

```text
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt
proc root  run  sbin  snap  srv  sys  tmp  usr  var
```

| Directory | Purpose |
| --- | --- |
| `/bin`, `/sbin` | Essential system binaries |
| `/boot` | Boot files |
| `/dev` | Device files |
| `/etc` | Configuration files |
| `/home` | User home directories |
| `/lib`, `/lib64` | Shared libraries |
| `/media`, `/mnt` | Mount points |
| `/opt` | Optional / third-party software |
| `/proc`, `/sys` | Virtual filesystems (kernel & process info) |
| `/root` | Root user's home |
| `/tmp` | Temporary files |
| `/usr` | User programs |
| `/var` | Variable data (logs, caches) |

---

## 1.9 Common Commands

### 1.9.1 `ls` — list directory contents

Shows files and subdirectories (name, permission, size, time...).

```bash
ls            # current directory
ls /home/bb   # a specific directory
ls .          # same as ls
ls ..         # parent directory
ls ~          # home directory
ls /          # root directory
```

| Option | Meaning |
| --- | --- |
| `-l` | Long format (permissions, owner, size, time) |
| `-a` | Show all files, including hidden ones (starting with `.`) |
| `-la` | Both (same as `ll`) |

```bash
ls -la
```

### 1.9.2 `cd` — change directory

```bash
cd ~        # home directory (same as plain cd)
cd ..       # up one level
cd ../..    # up two levels
cd /path    # absolute path
cd dir      # subdirectory (relative)
cd -        # go back to the previous directory
```

### 1.9.3 `pwd` — print working directory

Prints the absolute path of the current directory.

### 1.9.4 `touch` — create a file

```bash
touch filename
```

### 1.9.5 `cat` — read a file

Prints file content to the terminal.

```bash
cat filename
cat -n filename   # show line numbers (including empty lines)
```

### 1.9.6 `mkdir` — make a directory

```bash
mkdir mydir              # one folder
mkdir mydir1 mydir2      # several folders
mkdir -p game/fps        # create parents recursively (game and fps)
```

### 1.9.7 `rmdir` — remove an empty directory

```bash
rmdir -p game/fps/   # remove game and fps (parent-child chain)
```

> Only works on **empty** directories — use `rm` for non-empty ones.

### 1.9.8 `rm` — remove files / directories

```bash
rm -f file    # force, no prompt
rm -r dir     # recursive (for directories)
rm -rf dir    # force + recursive (dangerous!)
```

> `sudo rm -rf` is very dangerous — deleted data cannot be recovered.

### 1.9.9 `cp` — copy

```bash
cp source destination
```

| Option | Meaning |
| --- | --- |
| `-r` | Copy directories recursively (**required** for folders) |
| `-i` | Ask before overwriting |
| `-f` | Overwrite directly |
| `-n` | Never overwrite (skip) |
| `-s` | Create a symbolic link (shortcut) |

### 1.9.10 `mv` — move / rename

```bash
mv dir /        # move dir to root
mv dir dir2     # rename dir to dir2
```

| Option | Meaning |
| --- | --- |
| `-i` | Ask before overwriting |
| `-f` | Force overwrite |
| `-n` | Never overwrite |

### 1.9.11 `clear` — clear the terminal

```bash
clear    # shortcut: Ctrl + L
```

---

## 1.10 Wildcards

| Wildcard | Meaning |
| --- | --- |
| `*` | Any number of characters (0 or more) |
| `?` | Exactly one character |
| `[abcd]` | One of the characters `a`, `b`, `c`, `d` |
| `[0-9]` | One digit (a range) |

```bash
rm -rf test[234567]   # delete test2 ~ test7
rm -rf file*.json     # delete files matching file*.json
```

| Pattern | Matches |
| --- | --- |
| `bb*` | Files starting with `bb` |
| `bb*.py` | Files starting with `bb`, ending with `.py` |
| `bb?.txt` | `bb` + one character + `.txt` |
| `bb????` | `bb` + exactly four characters |
| `[abcd]*` | Files starting with a/b/c/d |
| `b[0-9][0-9]*` | `b` + two digits + anything |

---

| Do | Don't |
| --- | --- |
| Use `cd ~` / `cd /` to jump home / root quickly | Don't set a Chinese username during install |
| Press `Tab` to autocomplete and avoid typos | Don't run `sudo rm -rf /` — it wipes the system |
| Use `ls -la` to see hidden files & permissions | Don't confuse relative vs absolute paths |
| Take a VM snapshot before risky experiments | Don't auto-update right after the first login |

**Summary Mnemonic** — `cd` to move, `ls` to see, `pwd` to know where you are; `touch` a file, `mkdir` a folder, `rm -rf` with care. Everything starts from the root `/`.

[Next: Linux advanced ->](02-linux-advanced.md)
