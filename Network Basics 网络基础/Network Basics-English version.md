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

#### Pros

- Excellent UX: rich graphics/audio stored locally
- Offline capability (single-player games, document editing)
- Better security, data can be stored locally

#### Cons

- Higher dev/maintenance cost (client + server)
- Users must download updates
- Cross-platform complexity (iOS, Android, Windows)

### B/S: Browser / Server
No installation needed; access via browser using URLs.

| Aspect | Description |
|--------|-------------|
| **Access** | Browser + URL (baidu.com, jd.com, bilibili.com) |
| **Use Cases** | Entertainment, shopping, web games (convenience-focused) |

#### Pros

- No client development needed (web page + server only)
- Zero install for users; open browser and go
- Easy updates: server-side only, users just refresh
- Cross-platform: any device with a browser

#### Cons

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

#### IPv6 Address Structure

- **Address format**: 8 groups of 4 hexadecimal digits separated by colons
- **Example**: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- **Zero compression**: Consecutive groups of zeros can be replaced with `::`
  - Example: `2001:0db8:0000:0000:0000:0000:0000:0001` → `2001:0db8::0001`
  - **Rule**: Can only be used once per address
  - **Reason**: Using `::` twice would make it impossible to determine how many zero groups each represents (8 total groups minus visible groups = groups represented by `::`)

#### IP Address Types

| Type | Description | Address Range | Usage |
|------|-------------|---------------|-------|
| **Public IP** | Globally unique address accessible from the internet | Various | Internet communication |
| **Private IP** | Address used within local networks (LAN) | 192.168.x.x, 10.x.x.x, 172.16.x.x - 172.31.x.x | Internal network communication |
| **Loopback** | Local address referring to the current device | 127.0.0.1 (IPv4), ::1 (IPv6) | Local testing and development |

#### IPv4 Address Exhaustion

IPv4 provides approximately 4.2 billion unique addresses (2^32). With the explosive growth of internet-connected devices, IPv4 addresses were fully allocated by **November 26, 2019**.

##### Solutions

1. **IPv6 Deployment**
   - 128-bit address space provides 340 undecillion addresses (2^128)
   - Written as 8 groups of hexadecimal numbers separated by colons
   - Gradually replacing IPv4 as the standard protocol

2. **Network Address Translation (NAT)**
   - Allows multiple devices on a private network to share a single public IP
   - Router translates private IP to public IP for internet access
   - Temporarily extends IPv4 lifespan but creates network complexity

3. **Classless Inter-Domain Routing (CIDR)**
   - More flexible allocation of IP addresses
   - Replaces old class-based system (A, B, C classes)
   - Reduces address waste through subnetting

4. **Address Recycling**
   - Reclaiming unused address blocks from organizations
   - Selling allocated but unused addresses on the market
   - Limited effectiveness as a long-term solution

#### Common IP-Related Commands

| Operating System | Command              | Purpose                    |
| ---------------- | -------------------- | -------------------------- |
| Windows          | `ipconfig`           | Display private IP address |
| Linux/macOS      | `ifconfig`           | Display private IP address |
| Universal        | `curl ifconfig.me`   | Display public IP address  |
| Universal        | `ping [IP/hostname]` | Test network connectivity  |

> **Note on hostname**: Hostname is a network identifier that can be:
> - **Domain name**: `google.com`, `github.com`
> - **Local hostname**: `localhost` (refers to 127.0.0.1)
> - **FQDN**: `www.example.com` (Fully Qualified Domain Name)
>
> Examples: `ping google.com`, `ping localhost`, `ping 192.168.1.1`

### 1.2.2 Port Numbers

A numerical identifier for specific applications or services on a device.

| Attribute                 | Details                                                                   |
| ------------------------- | ------------------------------------------------------------------------- |
| **Range**                 | 0 - 65535                                                                 |
| **Well-known ports**      | 0 - 1023 (reserved for system services)                                   |
| **Registered ports**      | 1024 - 49151                                                              |
| **Dynamic/Private ports** | 49152 - 65535                                                             |
| **Purpose**               | Identifies specific applications/services on a device                     |
| **Uniqueness**            | Each port number can only be used by one application at a time per device |

#### Common Port Numbers

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

#### OSI Model (7 Layers)

A theoretical model used in network education.

| Layer | Name             | Function                                                           |
| ----- | ---------------- | ------------------------------------------------------------------ |
| 7     | **Application**  | Provides services directly to end-user applications                |
| 6     | **Presentation** | Data formatting, encryption/decryption, compression                |
| 5     | **Session**      | Establishes, manages, and terminates sessions between applications |
| 4     | **Transport**    | Provides reliable process-to-process communication                 |
| 3     | **Network**      | Implements end-to-end data routing                                 |
| 2     | **Data Link**    | Provides node-to-node reliable transmission                        |
| 1     | **Physical**     | Transmits raw bit streams over physical medium                     |

##### Data Flow

- **Sender**: Data starts at Application layer, processed downward through each layer, finally transmitted as binary signals at Physical layer.
- **Receiver**: Binary signals processed at Physical layer, moves upward through each layer, finally reconstructed to usable data at Application layer.

##### Pros

Establishes unified communication standards, reduces development difficulty through clear layer separation.

##### Cons

Overly idealistic, structurally too complex for practical engineering implementation.

#### TCP/IP Model (4 Layers)

Practical implementation standard used in actual networking.

| Layer | Name | Main Protocols | Function |
|-------|------|----------------|----------|
| 4 | **Application** | HTTP, FTP, SMTP, DNS | Application-specific protocols |
| 3 | **Transport** | TCP, UDP | Process-to-process communication |
| 2 | **Internet** | IP, ICMP, ARP | End-to-end data routing |
| 1 | **Network Interface** | Ethernet, Wi-Fi | Binary signal transmission over physical medium |

##### Key Protocols

- **Application Layer**: HTTP (web browsing), FTP (file transfer), SMTP (email), DNS (domain name resolution)
- **Transport Layer**: TCP (reliable, slower), UDP (unreliable, fast)
- **Internet Layer**: IP (addressing), ICMP (error reporting), ARP (address resolution)

## 1.3 Transport Layer: TCP and UDP

### 1.3.1 TCP vs UDP Comparison

| Feature | UDP | TCP |
|---------|-----|-----|
| **Connection** | Connectionless | Connection-oriented (3-way handshake to establish, 4-way to terminate) |
| **Reliability** | No guarantee of delivery or order | Guaranteed delivery with correct order |
| **Latency** | Low latency, fast transmission | Higher latency due to acknowledgment and retransmission |
| **Data Size** | Small data, high-frequency transmission | Large data transmission |
| **Use Cases** | Gaming, voice calls, live streaming, DNS, IoT | File transfer, web browsing, email, payment, remote login |
| **Requirements** | Low latency, high real-time requirements | High data integrity, acceptable delay |

#### TCP Use Cases

File downloads/uploads, email, database synchronization, banking/payment transactions, online games with low latency tolerance (e.g., World of Warcraft).

#### UDP Use Cases

Competitive gaming, video conferencing, live streaming, DNS queries, IoT devices.

### 1.3.2 Connection Analogy

- **TCP (Phone Call)**: Connection-based and reliable
  - Call must be connected first
  - Two-way communication
  - Hang up when finished

- **UDP (Text Message)**: Connectionless and unreliable
  - Did the recipient receive it?
  - Is the content complete?
  - Unknown network conditions

## 1.4 Data Transmission Format

All data (strings, numbers, containers) must be converted to byte sequences (binary data) before transmission.

### 1.4.1 String Encoding/Decoding

| Operation | Direction | Description |
|-----------|-----------|-------------|
| **encode** | Data → Binary | Converts human-readable data to transmittable binary format |
| **decode** | Binary → Data | Converts binary data back to human-readable format |

#### Example

```
"hello world" → b"hello world"
"你好世界" → b'\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c'
```

Byte sequences are indicated by the `b` prefix.

### 1.4.2 Container Data (Lists, Dictionaries)

Containers cannot be directly encoded. Must be converted to string first (e.g., JSON), then encoded to binary.

#### Process

Container → String (JSON) → Binary Data

#### Example

```python
list1 = ['apple', 'banana', 'watermelon']
# Step 1: Convert list to JSON string
str_list = json.dumps(list1)  # '["apple", "banana", "watermelon"]'
# Step 2: Encode string to binary
bytelist = str_list.encode()   # b'[...]'

# Reverse process:
strinfo2 = bytelist.decode()   # JSON string
list2 = json.loads(strinfo2)   # Original list
```
