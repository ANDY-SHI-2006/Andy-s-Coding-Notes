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

| Type | Description |
|------|-------------|
| **Public IP** | Globally unique address accessible from the internet |
| **Private IP** | Address used within local networks (LAN), not directly accessible from the internet |

### 1.2.2 Port Numbers

A numerical identifier for specific applications or services on a device. Each application corresponds to a unique port number.

| Attribute | Details |
|-----------|---------|
| **Range** | 0 - 65535 |
| **Well-known ports** | 0 - 1023 (reserved for system services, already occupied) |
| **Purpose** | Identifies specific software/applications on a device |
| **Uniqueness** | Each port number can only be used by one application at a time |

### 1.2.3 Protocols

A set of rules that define how data is transmitted over a network. Protocols determine the format, timing, sequencing, and error checking of data communication.

| Function | Description |
|----------|-------------|
| **Message format** | Defines how data is structured |
| **Transmission rules** | Determines how messages are sent and received |
| **Error handling** | Specifies how errors are detected and corrected |

## 1.3 Network Communication Protocol Models

### 1.3.1 The OSI Model

*(To be filled)*

### 1.3.2 The TCP/IP Model

*(To be filled)*

## 1.4 Transport Layer: TCP and UDP

### 1.4.1 Comparison and Summary

*(To be filled)*

## 1.5 What Data Can Be Transmitted?

*(To be filled)*

> **Note**: This is an English version of the networking notes. The content is to be filled gradually.
