# 1. Networking Fundamentals

## 1.1 Network Architecture

Two primary network architectures: **C/S** and **B/S**.

### C/S: Client / Server
Requires downloading a client application to use.

| Aspect | Description |
|--------|-------------|
| **Client** | Terminal program installed locally (WeChat, TikTok, Steam, LoL) |
| **Server** | 24/7 standby, responds to requests (e.g., Tencent WeChat Server) |
| **Use Cases** | Games, Banking Apps (high performance & security needs) |

**Pros:**
- Excellent UX: rich graphics/audio stored locally
- Offline capability (single-player games, document editing)
- Better security, data can be stored locally

**Cons:**
- Higher dev/maintenance cost (client + server)
- Users must download updates
- Cross-platform complexity (iOS, Android, Windows)

### B/S: Browser / Server
No installation needed; access via browser using URLs.

| Aspect | Description |
|--------|-------------|
| **Access** | Browser + URL (baidu.com, jd.com, bilibili.com) |
| **Use Cases** | Entertainment, shopping, web games (convenience-focused) |

**Pros:**
- No client development needed (web page + server only)
- Zero install for users; open browser and go
- Easy updates: server-side only, users just refresh
- Cross-platform: any device with a browser

**Cons:**
- Everything loaded from server → network dependent
- Poor performance for large apps (low quality graphics/audio)
- Limited interactivity compared to native apps

### Comparison Summary

| Criteria | C/S Architecture | B/S Architecture |
|----------|------------------|------------------|
| **Usage** | Download required | Browser only |
| **UX** | Fast, rich, smooth | Browser-limited, may lag |
| **Cross-platform** | Multiple versions needed | Any browser works |
| **Maintenance** | Client updates needed | Server-only updates |
| **Security** | More secure (local data) | Server-dependent, vulnerable |
| **Examples** | LoL, Banking apps | Taobao, JD, Weibo |

> **Conclusion:** C/S for performance/security (games); B/S for ease of use (web apps). Many apps use both.

## 1.2 Three Key Components of Networks

### 1.2.1 IP Address

A logical address assigned to each computer or network device on the internet, used to identify and locate the device within a network.

#### IP Address Classification

| Version | Description | Address Length | Format |
|---------|-------------|----------------|--------|
| **IPv4** | Internet Protocol version 4 | 32-bit binary | Dot-decimal notation (e.g., 192.168.1.34) |
| **IPv6** | Internet Protocol version 6 | 128-bit binary | 8 groups of hexadecimal numbers separated by colons |

#### IPv4 Address Structure

- **Binary representation**: 32 bits divided into 4 octets (8 bits each)
- **Display format**: Dot-decimal notation (e.g., 192.168.1.34)
- **Value range per octet**: 0 - 255
- **Total address space**: Approximately 4.2 billion (256^4) unique addresses

**Binary to Decimal Conversion:**
Each bit represents a power of 2, from right to left starting at 2^0.

```
11000000 = 1×2^7 + 1×2^6 = 128 + 64 = 192
10101000 = 1×2^7 + 1×2^5 + 1×2^3 = 128 + 32 + 8 = 168
00000001 = 1×2^0 = 1
00100010 = 1×2^5 + 1×2^1 = 32 + 2 = 34
```

**Number Systems:**
| System | Base | Digits |
|--------|------|--------|
| Binary | 2 | 0, 1 |
| Octal | 8 | 0-7 |
| Decimal | 10 | 0-9 |
| Hexadecimal | 16 | 0-9, a-f (where a=10, b=11, c=12, d=13, e=14, f=15) |

#### IPv6 Address Structure

- **Address format**: 8 groups of 4 hexadecimal digits separated by colons
- **Example**: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- **Zero compression**: Consecutive groups of zeros can be replaced with `::` (can only be used once per address)
- **Compressed example**: `2001:0db8:85a3::8a2e:0370:7334`

#### IP Address Types

| Type | Description | Address Range | Usage |
|------|-------------|---------------|-------|
| **Public IP** | Globally unique address accessible from the internet | Various | Internet communication |
| **Private IP** | Address used within local networks (LAN) | 192.168.x.x, 10.x.x.x, 172.16.x.x - 172.31.x.x | Internal network communication |
| **Loopback** | Local address referring to the current device | 127.0.0.1 (IPv4), ::1 (IPv6) | Local testing and development |

#### IPv4 Address Exhaustion Solution

IPv4 addresses were fully allocated by November 26, 2019. Two primary solutions:

1. **IPv6 Deployment**: Gradually replacing IPv4 with the larger address space of IPv6
2. **Network Address Translation (NAT)**: Allows multiple devices on a private network to share a single public IP address for internet access

#### Common IP-Related Commands

| Operating System | Command | Purpose |
|------------------|---------|---------|
| Windows | `ipconfig` | Display private IP address |
| Linux/macOS | `ifconfig` | Display private IP address |
| Universal | `curl ifconfig.me` | Display public IP address |
| Universal | `ping [IP/hostname]` | Test network connectivity |

### 1.2.2 Port Numbers

A numerical identifier for specific applications or services on a device.

| Attribute | Details |
|-----------|---------|
| **Range** | 0 - 65535 |
| **Well-known ports** | 0 - 1023 (reserved for system services) |
| **Registered ports** | 1024 - 49151 |
| **Dynamic/Private ports** | 49152 - 65535 |
| **Purpose** | Identifies specific applications/services on a device |
| **Uniqueness** | Each port number can only be used by one application at a time per device |

**Common Port Numbers:**
| Port | Service |
|------|---------|
| 80 | HTTP |
| 443 | HTTPS |
| 22 | SSH |
| 21 | FTP |
| 25 | SMTP |
| 8080 | Alternative HTTP |

### 1.2.3 Protocols

A set of rules that define how data is transmitted over a network.

| Function | Description |
|----------|-------------|
| **Message format** | Defines how data is structured |
| **Transmission rules** | Determines how messages are sent and received |
| **Error handling** | Specifies how errors are detected and corrected |

#### Network Communication Protocol Models

| Model | Layers | Description |
|-------|--------|-------------|
| **OSI Model** | 7 layers | Theoretical model (Physical, Data Link, Network, Transport, Session, Presentation, Application) |
| **TCP/IP Model** | 4 layers | Practical implementation standard (Network Interface, Internet, Transport, Application) |

The TCP/IP model is the de facto standard for internet communication.

## 1.3 Transport Layer: TCP and UDP

### 1.4.1 Comparison and Summary

*(To be filled)*

## 1.5 What Data Can Be Transmitted?

*(To be filled)*

> **Note**: This is an English version of the networking notes. The content is to be filled gradually.
