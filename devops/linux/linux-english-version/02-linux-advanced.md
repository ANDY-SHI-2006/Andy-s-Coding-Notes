[<- Prev: Linux basics](01-linux-basics.md) | [Next: deployment ->](03-deployment.md)

# 2 Linux Advanced

> This chapter covers file permissions, piping and redirection, archiving, editing, searching, networking, and managing users and processes.

## 2.1 File Permissions

A permission string like `drwxr-xr-x` has **10 characters**.

| Position | Meaning |
| --- | --- |
| Character 1 | File type |
| Characters 2–4 | Owner permissions |
| Characters 5–7 | Group permissions |
| Characters 8–10 | Other users' permissions |

### File type (character 1)

| Char | Meaning |
| --- | --- |
| `d` | Directory |
| `-` | Regular file |
| `l` | Symbolic link (points to another target) |
| `b` | Block device file |
| `c` | Character device file |

### Permission letters (characters 2–10)

| Char | Meaning |
| --- | --- |
| `r` | Read |
| `w` | Write |
| `x` | Execute |
| `-` | No permission |

For `rwxr-xr-x`:

| Group | Permissions | Meaning |
| --- | --- | --- |
| Owner | `rwx` | Read, write, execute |
| Group | `r-x` | Read, execute (no write) |
| Others | `r-x` | Read, execute (no write) |

### Three notations

| Notation | Example | Rule |
| --- | --- | --- |
| Letters | `rwxr-xr-x` | `r`/`w`/`x`/`-` per position |
| Binary | `111 101 101` | `1` = has, `0` = none |
| Octal | `755` | `r=4, w=2, x=1` |

```text
rwx = 4+2+1 = 7      rw- = 4+2+0 = 6
r-x = 4+0+1 = 5      r-- = 4+0+0 = 4
```

> `777` opens every permission — convenient while learning, but **not safe**.

---

## 2.2 Pipe & Redirection

### Redirection

Send output that would go to the screen into a file instead (the file is created if it doesn't exist).

| Symbol | Mode |
| --- | --- |
| `>` | Overwrite |
| `>>` | Append |

```bash
ll > test.txt     # write ll output into test.txt (overwrite)
ls > test.txt     # overwrite test.txt with ls output
ll >> test.txt    # append ll output to test.txt
> test.py         # quick trick: create an empty file
```

### Pipe

Pass the output of one program as the input of the next.

```bash
command1 | command2
```

```bash
cd ~
ll | more    # view a long listing one screen at a time
```

> `more` shows a file one screen at a time: `Space` next page, arrows up/down, `q` quit.

### Practice

```bash
history > myfile.txt        # 1. write command history to myfile.txt
ls / >> myfile.txt          # 2. append the root listing to myfile.txt
ls / | more                 # 3. list root and view one screen at a time
```

---

## 2.3 `tar` — archive & compress

`tar` does two things:

1. **Archive** — combine many files/directories into one `.tar` file (storage form changes, content doesn't).
2. **Compress** — on top of archiving, call an external tool (`gzip`, `bzip2`, `xz`) to produce `.tar.gz`, `.tar.bz2`, `.tar.xz`.

```text
tar [options] [output file] [source file/directory]
```

| Option | Meaning |
| --- | --- |
| `-c` | Create a new archive (pack) |
| `-x` | Extract an archive (unpack) |
| `-f` | Specify the file name (**required**, usually last) |
| `-z` | Use gzip (`.gz`) |
| `-C` | Extract to a specific directory |
| `-v` | Show details (verbose) |

### gzip (`.tar.gz`)

```bash
tar -zcvf test.tar.gz test          # pack + compress a folder
tar -zxvf test.tar.gz               # extract to the current directory
tar -zxvf test.tar.gz -C ~          # extract to a specific directory
```

### bzip2 (`.tar.bz2`)

```bash
tar -jcvf name.tar.bz2 files        # pack + compress
tar -jxvf name.tar.bz2 -C target/   # extract to a directory (must exist)
```

---

## 2.4 `chmod` — change permissions

| Option | Meaning |
| --- | --- |
| `-R` | Apply recursively (to files inside a folder too) |

### Letter method

| Role | Meaning |
| --- | --- |
| `u` | Owner |
| `g` | Group |
| `o` | Others |
| `a` | All users |

| Operator | Meaning |
| --- | --- |
| `+` | Add permission |
| `-` | Remove permission |
| `=` | Set permission |

```bash
chmod u=r test.tar.gz    # owner: read only
chmod u+w test.tar.gz    # owner: add write
chmod u-w test.tar.gz    # owner: remove write
chmod u=rwx test.tar.gz  # owner: all permissions
chmod a=rwx test.tar.gz  # everyone: all permissions
```

### Numeric method (more common)

```bash
chmod 777 test.tar.gz    # everyone: all permissions (= chmod a=rwx)
chmod 754 test.tar.gz    # owner all, group read+execute, others read only
```

---

## 2.5 SSH Remote Connection

Tools: FinalShell, Xshell, etc.

1. On Windows, install **FinalShell**.
2. On Linux, install the SSH server:

```bash
sudo apt install openssh-server
```

3. Manage the `sshd` service:

```bash
sudo systemctl start sshd      # start
sudo systemctl stop sshd       # stop
sudo systemctl status sshd     # check status (active = running)
```

4. In FinalShell, create an **SSH connection** using the VM's IP, username, and password.

> If apt reports a lock (`/var/lib/dpkg/lock-frontend`), kill the process holding it: `kill -9 PID`.

---

## 2.6 `vim` Editor (basics)

```bash
sudo apt install vim
vim filename
```

### Three modes

| Mode | How to enter | Purpose |
| --- | --- | --- |
| Command mode (default) | Start Vim | Keys are commands, not text |
| Edit (insert) mode | `i`, `a`, `o` | Type text |
| Last-line mode | `Shift + ;` (i.e. `:`) | Save / quit / settings |

### Command-mode keys

| Key | Action |
| --- | --- |
| `h` `j` `k` `l` | Left, down, up, right (or use arrow keys) |
| `gg` | Jump to the top of the file |
| `G` | Jump to the bottom |

### Entering edit mode

| Key | Action |
| --- | --- |
| `i` | Insert **before** the cursor |
| `a` | Append **after** the cursor |
| `o` | Insert a new line below |

Press `Esc` to return to command mode.

### Last-line mode commands

| Command | Action |
| --- | --- |
| `:w` | Save |
| `:q` | Quit |
| `:wq` | Save and quit |
| `:q!` | Quit without saving |
| `:set nu` | Show line numbers |
| `:set nonu` | Hide line numbers |

```bash
:wq!   # save and quit
:q!    # quit without saving
```

> Without a GUI, Vim is the standard editing tool.

---

## 2.7 Searching

### `which` — find a program

Searches `PATH` for an executable matching the command name.

```bash
which python3
```

### `find` — find files

```text
find [start directory] [options] condition
```

```bash
find -name aaa.txt       # search from the current directory
find -name "*.txt"       # use wildcards inside quotes
find / -name aaa.txt     # from root (needs sudo)
find ~ -name aaa.txt     # from home (no sudo needed)
```

### `grep` — search inside files

```text
grep [options] pattern [file1 file2 ...]
```

| Option | Meaning |
| --- | --- |
| `-i` | Ignore case |
| `-n` | Show line numbers |
| `-v` | Invert match (lines that don't match) |

```bash
grep 'root' /etc/passwd        # lines containing root
grep -in 'root' /etc/passwd    # ignore case + line numbers
grep -inv 'root' /etc/passwd   # lines NOT containing root
netstat -ln | grep -n "22"     # find "22" in netstat output
```

---

## 2.8 Network

### `ifconfig` — network interfaces

Shows the network interface name (e.g. `ens33`) and the LAN IP (e.g. `192.168.203.138`).

### `netstat` — network status

Visualizes network state (listening ports, connections).

```bash
netstat -ln    # the most common use
```

---

## 2.9 User Management

### Add a user

```bash
useradd -m username -s /bin/bash   # -m: create home directory
passwd username                    # set the password
```

| Option | Meaning |
| --- | --- |
| `-m` | Create the home directory automatically |
| `-d` | Specify the home directory (default `/home/username`) |
| `-M` | Do not create a home directory |
| `-s` | Specify the login shell (default `/bin/sh`) |

### Modify a user — `usermod`

```bash
usermod -s /bin/bash username     # change the login shell
usermod -d /data/username username # change the home directory
usermod -g developers username    # change the primary group
```

### Delete a user

```bash
userdel username       # delete the user
userdel -r username    # also delete the home directory
```

---

## 2.10 Process Management

A **process** is a running program — a program that has been "activated".

### `ps` — process snapshot

```bash
ps -aux                 # snapshot of current processes
ps -aux | grep 'ssh'    # find processes matching "ssh"
```

### `free` — memory usage

Shows system memory usage.

### `top` — live monitor

Real-time, ranked by resource consumption (dynamic).

| Key | Action |
| --- | --- |
| `Ctrl + C` | Stop the current foreground process |
| `Ctrl + Z` | Suspend the process (move to background) |

### `kill` — kill a process

```bash
kill PID        # terminate a process
kill -9 PID     # force kill (when normal kill doesn't work)
```

---

## 2.11 `apt` — package management

Ubuntu uses `apt` (like `pip` for Python); CentOS uses `yum`.

```bash
sudo apt update                 # refresh source metadata (run first!)
sudo apt upgrade                # upgrade installed packages
sudo apt install pkg            # install (space-separated for several)
sudo apt remove pkg             # remove (keeps config files)
sudo apt purge pkg              # remove completely
sudo apt autoremove             # clean up unused dependencies
sudo apt full-upgrade           # full system upgrade
```

```bash
sudo apt install mysql-server
```

---

| Do | Don't |
| --- | --- |
| Use numeric `chmod` (e.g. `755`) for clarity | Don't `chmod 777` in production — it's unsafe |
| Prefer `>>` to append instead of overwriting | Don't confuse `>` (overwrite) with `>>` (append) |
| `tar -zxvf` + `-C` to extract where you want | Don't run `kill -9` as the first option |
| Use `grep -in` for case-insensitive + line numbers | Don't run `rm -rf` on paths you aren't sure about |

**Summary Mnemonic** — `>` overwrites, `>>` appends, `|` pipes; `tar -c` packs, `tar -x` unpacks; `chmod 777` opens all (unsafe); `ps` sees processes, `kill -9` ends them, `apt install` gets software.

[<- Prev: Linux basics](01-linux-basics.md) | [Next: deployment ->](03-deployment.md)
