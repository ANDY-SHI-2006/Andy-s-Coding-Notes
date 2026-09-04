[← 上一篇：Linux 基础](01-Linux基础.md) | [下一篇：部署 →](03-部署.md)

# 2 Linux 进阶

> 本章介绍文件权限、管道与重定向、打包压缩、编辑、查找、网络，以及用户和进程管理。

## 2.1 文件权限

像 `drwxr-xr-x` 这样的权限字符串共有 **10 个字符**。

| 位置 | 含义 |
| --- | --- |
| 第 1 个字符 | 文件类型 |
| 第 2~4 个字符 | 属主（创建者）权限 |
| 第 5~7 个字符 | 属组权限 |
| 第 8~10 个字符 | 其他用户权限 |

### 文件类型（第 1 个字符）

| 字符 | 含义 |
| --- | --- |
| `d` | 目录（文件夹） |
| `-` | 普通文件 |
| `l` | 符号链接（指向另一目标） |
| `b` | 块设备文件 |
| `c` | 字符设备文件 |

### 权限字母（第 2~10 个字符）

| 字符 | 含义 |
| --- | --- |
| `r` | 读 |
| `w` | 写 |
| `x` | 执行 |
| `-` | 无权限 |

以 `rwxr-xr-x` 为例：

| 对象 | 权限 | 含义 |
| --- | --- | --- |
| 属主 | `rwx` | 可读、可写、可执行 |
| 属组 | `r-x` | 可读、可执行（不可写） |
| 其他 | `r-x` | 可读、可执行（不可写） |

### 三种表示法

| 表示法 | 示例 | 规则 |
| --- | --- | --- |
| 字母法 | `rwxr-xr-x` | 每位 `r`/`w`/`x`/`-` |
| 二进制法 | `111 101 101` | `1` 有权限，`0` 无权限 |
| 八进制法 | `755` | `r=4, w=2, x=1` |

```text
rwx = 4+2+1 = 7      rw- = 4+2+0 = 6
r-x = 4+0+1 = 5      r-- = 4+0+0 = 4
```

> `777` 开放所有权限——学习阶段方便，但**不安全**。

---

## 2.2 管道与重定向

### 重定向

把原本输出到屏幕的内容，输出到文件中（文件不存在则自动创建）。

| 符号 | 模式 |
| --- | --- |
| `>` | 覆盖 |
| `>>` | 追加 |

```bash
ll > test.txt     # 把 ll 的输出写入 test.txt（覆盖）
ls > test.txt     # 用 ls 的输出覆盖 test.txt
ll >> test.txt    # 把 ll 的输出追加到 test.txt
> test.py         # 小技巧：快速创建空文件
```

### 管道

把前一个程序的输出，作为后一个程序的输入。

```bash
command1 | command2
```

```bash
cd ~
ll | more    # 分屏查看详细文件列表
```

> `more` 分屏查看：`空格` 下一页，上下箭头翻行，`q` 退出。

### 小练习

```bash
history > myfile.txt        # 1. 把历史命令写入 myfile.txt
ls / >> myfile.txt          # 2. 把根目录列表追加到 myfile.txt
ls / | more                 # 3. 分屏显示根目录内容
```

---

## 2.3 `tar`——打包与压缩

`tar` 有两个核心能力：

1. **打包（Archive）**——把多个分散的文件/目录合并成一个 `.tar` 归档（只改存储形式，不改内容）。
2. **压缩（Compress）**——在打包基础上调用外部工具（`gzip`、`bzip2`、`xz`），生成 `.tar.gz`、`.tar.bz2`、`.tar.xz`。

```text
tar [选项] [输出文件名] [源文件/目录]
```

| 选项 | 含义 |
| --- | --- |
| `-c` | 创建新归档（打包） |
| `-x` | 提取归档（解压） |
| `-f` | 指定文件名（**必选**，一般放最后） |
| `-z` | 使用 gzip（`.gz`） |
| `-C` | 解压到指定目录 |
| `-v` | 显示详情 |

### gzip（`.tar.gz`）

```bash
tar -zcvf test.tar.gz test          # 打包并压缩一个文件夹
tar -zxvf test.tar.gz               # 解压到当前目录
tar -zxvf test.tar.gz -C ~          # 解压到指定目录
```

### bzip2（`.tar.bz2`）

```bash
tar -jcvf name.tar.bz2 files        # 打包并压缩
tar -jxvf name.tar.bz2 -C target/   # 解压到指定目录（目录需存在）
```

---

## 2.4 `chmod`——修改权限

| 选项 | 含义 |
| --- | --- |
| `-R` | 递归修改（文件夹内的文件也一起改） |

### 字母法

| 角色 | 含义 |
| --- | --- |
| `u` | 创建文件的用户（属主） |
| `g` | 同组用户 |
| `o` | 其他用户 |
| `a` | 所有用户 |

| 操作 | 含义 |
| --- | --- |
| `+` | 增加权限 |
| `-` | 撤销权限 |
| `=` | 设置权限 |

```bash
chmod u=r test.tar.gz    # 属主：只读
chmod u+w test.tar.gz    # 属主：增加可写
chmod u-w test.tar.gz    # 属主：去掉可写
chmod u=rwx test.tar.gz  # 属主：全部权限
chmod a=rwx test.tar.gz  # 所有用户：全部权限
```

### 数字法（更常用）

```bash
chmod 777 test.tar.gz    # 所有用户全部权限（等价 chmod a=rwx）
chmod 754 test.tar.gz    # 属主全部、属组读+执行、其他只读
```

---

## 2.5 SSH 远程连接

工具：FinalShell、Xshell 等。

1. Windows 上安装 **FinalShell**。
2. Linux 上安装 SSH 服务器：

```bash
sudo apt install openssh-server
```

3. 管理 `sshd` 服务：

```bash
sudo systemctl start sshd      # 启动
sudo systemctl stop sshd       # 停止
sudo systemctl status sshd     # 查看状态（active 表示激活）
```

4. 在 FinalShell 里新建 **SSH 连接**，填入虚拟机的 IP、用户名和密码。

> 若 apt 报锁错误（`/var/lib/dpkg/lock-frontend`），用 `kill -9 PID` 杀掉占用锁的进程。

---

## 2.6 `vim` 编辑器（基础）

```bash
sudo apt install vim
vim filename
```

### 三种工作模式

| 模式 | 进入方式 | 用途 |
| --- | --- | --- |
| 命令模式（默认） | 启动 Vim | 键盘输入的都是操作指令，不是文本 |
| 编辑模式 | `i`、`a`、`o` | 输入文本 |
| 末行模式 | `Shift + ;`（即 `:`） | 保存 / 退出 / 设置 |

### 命令模式按键

| 按键 | 作用 |
| --- | --- |
| `h` `j` `k` `l` | 左、下、上、右（也可用方向键） |
| `gg` | 跳到文件开头 |
| `G` | 跳到文件末尾 |

### 进入编辑模式

| 按键 | 作用 |
| --- | --- |
| `i` | 在当前光标**前**插入 |
| `a` | 在当前光标**后**追加 |
| `o` | 在下一行插入新行 |

按 `Esc` 回到命令模式。

### 末行模式命令

| 命令 | 作用 |
| --- | --- |
| `:w` | 保存 |
| `:q` | 退出 |
| `:wq` | 保存并退出 |
| `:q!` | 不保存退出 |
| `:set nu` | 显示行号 |
| `:set nonu` | 隐藏行号 |

```bash
:wq!   # 保存并退出
:q!    # 不保存退出
```

> 没有图形界面的情况下，vim 是常用编辑工具。

---

## 2.7 查找

### `which`——查找程序

在环境变量 `PATH` 中搜索与命令名匹配的可执行文件。

```bash
which python3
```

### `find`——查找文件

```text
find [起始目录] [选项] 匹配条件
```

```bash
find -name aaa.txt       # 从当前目录查找
find -name "*.txt"       # 引号内可用通配符
find / -name aaa.txt     # 从根目录查找（需加 sudo）
find ~ -name aaa.txt     # 从用户主目录查找（无需 sudo）
```

### `grep`——文本搜索

```text
grep [选项] 查找模式 [文件1 文件2 ...]
```

| 选项 | 含义 |
| --- | --- |
| `-i` | 不区分大小写 |
| `-n` | 同时输出行号 |
| `-v` | 匹配取反（找不匹配的内容） |

```bash
grep 'root' /etc/passwd        # 包含 root 的行
grep -in 'root' /etc/passwd    # 不区分大小写 + 行号
grep -inv 'root' /etc/passwd   # 不包含 root 的行
netstat -ln | grep -n "22"     # 在 netstat 输出中找 "22"
```

---

## 2.8 网络相关

### `ifconfig`——网卡信息

显示网卡名（如 `ens33`）和局域网 IP（如 `192.168.203.138`）。

### `netstat`——网络状态

可视化网络状态（监听端口、连接等）。

```bash
netstat -ln    # 最常用
```

---

## 2.9 用户管理

### 添加用户

```bash
useradd -m username -s /bin/bash   # -m：自动创建主目录
passwd username                    # 设置密码
```

| 选项 | 含义 |
| --- | --- |
| `-m` | 自动创建主目录 |
| `-d` | 指定主目录（默认 `/home/username`） |
| `-M` | 不创建主目录 |
| `-s` | 指定登录 shell（默认 `/bin/sh`） |

### 修改用户——`usermod`

```bash
usermod -s /bin/bash username     # 修改登录 shell
usermod -d /data/username username # 修改主目录
usermod -g developers username    # 修改主组
```

### 删除用户

```bash
userdel username       # 删除用户
userdel -r username    # 同时删除主目录
```

---

## 2.10 进程管理

**进程** 是运行中的程序——程序被“激活”后在计算机里“活着”的状态。

### `ps`——进程快照

```bash
ps -aux                 # 当前运行的进程快照
ps -aux | grep 'ssh'    # 搜索包含 ssh 的进程
```

### `free`——内存使用

显示系统内存使用情况。

### `top`——实时监控

按资源消耗程度实时排行、动态变化。

| 按键 | 作用 |
| --- | --- |
| `Ctrl + C` | 终止当前前台进程 |
| `Ctrl + Z` | 暂停（挂起）当前前台进程 |

### `kill`——杀死进程

```bash
kill PID        # 终止进程
kill -9 PID     # 强制杀死（普通 kill 无效时）
```

---

## 2.11 `apt`——软件包管理

Ubuntu 常用 `apt`（类比 Python 的 `pip`）；CentOS 用 `yum`。

```bash
sudo apt update                 # 更新软件源元数据（必须先执行）
sudo apt upgrade                # 升级已安装的软件包
sudo apt install pkg            # 安装（可空格隔开装多个）
sudo apt remove pkg             # 删除（保留配置文件）
sudo apt purge pkg              # 彻底卸载
sudo apt autoremove             # 清理无用依赖
sudo apt full-upgrade           # 全系统升级
```

```bash
sudo apt install mysql-server
```

---

| 推荐做 | 不要做 |
| --- | --- |
| 用数字法 `chmod`（如 `755`）更直观 | 生产环境不要 `chmod 777`——不安全 |
| 追加内容优先用 `>>` | 不要混淆 `>`（覆盖）和 `>>`（追加） |
| 解压用 `tar -zxvf` + `-C` 指定目录 | 不要首选 `kill -9` |
| 用 `grep -in` 忽略大小写并显示行号 | 不确定的路径不要 `rm -rf` |

**记忆口诀**——`>` 覆盖、`>>` 追加、`|` 管道；`tar -c` 打包、`tar -x` 解包；`chmod 777` 全开放（不安全）；`ps` 看进程、`kill -9` 结束它、`apt install` 装软件。

[← 上一篇：Linux 基础](01-Linux基础.md) | [下一篇：部署 →](03-部署.md)
