# 1. Networking Fundamentals

## 1.1 Network Architecture

Two primary network architectures: **C/S** and **B/S**.

### 1.1.1 C/S: Client / Server

Requires downloading a client application to use.

| Aspect | Description |
|--------|-------------|
| **Client** | Terminal program installed locally (WeChat, TikTok, Steam, LoL) |
| **Server** | 24/7 standby, responds to requests (e.g., Tencent WeChat Server) |
| **Use Cases** | Games, Banking Apps (high performance & security needs) |

#### 1.1.1.1 Pros

- Excellent UX: rich graphics/audio stored locally
- Offline capability (single-player games, document editing)
- Better security, data can be stored locally

#### 1.1.1.2 Cons

- Higher dev/maintenance cost (client + server)
- Users must download updates
- Cross-platform complexity (iOS, Android, Windows)

### 1.1.2 B/S: Browser / Server

No installation needed; access via browser using URLs.

| Aspect | Description |
|--------|-------------|
| **Access** | Browser + URL (baidu.com, jd.com, bilibili.com) |
| **Use Cases** | Entertainment, shopping, web games (convenience-focused) |

#### 1.1.2.1 Pros

- No client development needed (web page + server only)
- Zero install for users; open browser and go
- Easy updates: server-side only, users just refresh
- Cross-platform: any device with a browser

#### 1.1.2.2 Cons

- Everything loaded from server → network dependent
- Poor performance for large apps (low quality graphics/audio)
- Limited interactivity compared to native apps

### 1.1.3 Comparison Summary

| Criteria | C/S Architecture | B/S Architecture |
|----------|------------------|------------------|
| **Usage** | Download required | Browser only |
| **UX** | Fast, rich, smooth | Browser-limited, may lag |
| **Cross-platform** | Multiple versions needed | Any browser works |
| **Maintenance** | Client updates needed | Server-only updates |
| **Security** | More secure (local data) | Server-dependent, vulnerable |
| **Examples** | LoL, Banking apps | Taobao, JD, Weibo |

> **Conclusion:** C/S for performance/security (games); B/S for ease of use (web apps). Many apps use both.

### 1.1.4 Why Architecture Matters for DevOps

DevOps engineers deploy, monitor, and troubleshoot both C/S and B/S applications. Understanding these architectures helps determine:

- **Load balancing strategy**: B/S apps usually balance HTTP traffic; C/S apps may balance TCP/UDP game or banking traffic.
- **Deployment patterns**: B/S enables blue-green or rolling updates on the server side only; C/S requires client update mechanisms.
- **Monitoring points**: B/S focuses on response time and status codes; C/S focuses on connection stability, packet loss, and latency.
- **Security boundary**: C/S can store sensitive data locally; B/S relies entirely on server-side and transport security.

## 1.2 Core Network Elements

Every network communication involves three core elements: **IP addresses**, **port numbers**, and **protocols**.

### 1.2.1 IP Address

An IP address is a unique identifier assigned to a device on a network.

#### 1.2.1.1 IP Address Classification

| Version | Description | Address Length | Format |
|---------|-------------|----------------|--------|
| **IPv4** | Internet Protocol version 4 | 32-bit binary | Dot-decimal notation (e.g., `192.168.1.34`) |
| **IPv6** | Internet Protocol version 6 | 128-bit binary | 8 groups of hexadecimal numbers separated by colons |

#### 1.2.1.2 IPv4 Address Structure

- **Binary representation**: 32 bits divided into 4 octets (8 bits each)
- **Display format**: Dot-decimal notation (e.g., `192.168.1.34`)
- **Value range per octet**: 0 - 255
- **Total address space**: Approximately 4.3 billion (2^32) unique addresses

#### 1.2.1.3 IPv6 Address Structure

- **Address format**: 8 groups of 4 hexadecimal digits separated by colons
- **Example**: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- **Zero compression**: Consecutive groups of zeros can be replaced with `::`
  - Example: `2001:0db8:0000:0000:0000:0000:0000:0001` → `2001:0db8::0001`
  - **Rule**: Can only be used once per address
  - **Reason**: Using `::` twice would make it impossible to determine how many zero groups each represents (8 total groups minus visible groups = groups represented by `::`)

#### 1.2.1.4 IP Address Types

| Type | Description | Address Range | Usage |
|------|-------------|---------------|-------|
| **Public IP** | Globally unique address accessible from the internet | Various | Internet communication |
| **Private IP** | Address used within local networks (LAN) | `192.168.0.0/16`, `10.0.0.0/8`, `172.16.0.0/12` | Internal network communication |
| **Loopback** | Local address referring to the current device | `127.0.0.1` (IPv4), `::1` (IPv6) | Local testing and development |

> **Note on private IP ranges**: The `172.16.0.0/12` range spans from `172.16.0.0` to `172.31.255.255`.

#### 1.2.1.5 IPv4 Address Exhaustion

IPv4 provides approximately 4.3 billion unique addresses (2^32). With the explosive growth of internet-connected devices, the global IPv4 address pool was exhausted in stages:

- **IANA** allocated the last IPv4 address blocks on **February 3, 2011**.
- **Regional Internet Registries (RIRs)** ran out of free IPv4 addresses at different times (between 2011 and 2019).
- This shortage makes IPv6 and address conservation techniques essential.

##### 1.2.1.5.1 Solutions

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

#### 1.2.1.6 Common IP-Related Commands

| Operating System | Command | Purpose |
| ---------------- | -------------------- | -------------------------- |
| Windows | `ipconfig` | Display private IP address |
| Linux (modern) | `ip addr` | Display private IP address |
| Linux/macOS (legacy) | `ifconfig` | Display private IP address |
| Universal | `curl ifconfig.me` | Display public IP address |
| Universal | `ping [IP/hostname]` | Test network connectivity |

> **Note on hostname**: A hostname is a network identifier that can be:
> - **Domain name**: `google.com`, `github.com`
> - **Local hostname**: `localhost` (refers to `127.0.0.1`)
> - **FQDN**: `www.example.com` (Fully Qualified Domain Name)
>
> Examples: `ping google.com`, `ping localhost`, `ping 192.168.1.1`

### 1.2.2 Port Numbers

A numerical identifier for specific applications or services on a device.

| Attribute | Details |
| ------------------------- | ------------------------------------------------------------------------- |
| **Range** | 0 - 65535 |
| **Well-known ports** | 0 - 1023 (reserved for system services; requires root/admin on most systems) |
| **Registered ports** | 1024 - 49151 |
| **Dynamic/Private ports** | 49152 - 65535 |
| **Purpose** | Identifies specific applications/services on a device |
| **Uniqueness** | Each port number can only be used by one application at a time per device |

#### 1.2.2.1 Common Port Numbers

| Port | Service | Description |
|------|---------|-------------|
| 20/21 | FTP | File Transfer Protocol |
| 22 | SSH | Secure Shell remote login |
| 25 | SMTP | Simple Mail Transfer Protocol |
| 53 | DNS | Domain Name System |
| 80 | HTTP | Hypertext Transfer Protocol |
| 110 | POP3 | Post Office Protocol v3 |
| 143 | IMAP | Internet Message Access Protocol |
| 443 | HTTPS | HTTP over TLS/SSL |
| 3306 | MySQL/MariaDB | Relational database |
| 5432 | PostgreSQL | Relational database |
| 6379 | Redis | In-memory data store |
| 8080 | Alternative HTTP | Common development/proxy port |
| 27017 | MongoDB | NoSQL database |

### 1.2.3 Protocols

A set of rules that define how data is transmitted over a network.

| Function | Description |
|----------|-------------|
| **Message format** | Defines how data is structured |
| **Transmission rules** | Determines how messages are sent and received |
| **Error handling** | Specifies how errors are detected and corrected |

#### 1.2.3.1 Network Communication Protocol Models

| Model | Layers | Description |
|-------|--------|-------------|
| **OSI Model** | 7 layers | Theoretical model (Physical, Data Link, Network, Transport, Session, Presentation, Application) |
| **TCP/IP Model** | 4 layers | Practical implementation standard (Network Interface, Internet, Transport, Application) |

The TCP/IP model is the de facto standard for internet communication.

#### 1.2.3.2 OSI Model (7 Layers)

A theoretical model used in network education.

| Layer | Name | Function |
| ----- | ---------------- | ------------------------------------------------------------------ |
| 7 | **Application** | Provides services directly to end-user applications |
| 6 | **Presentation** | Data formatting, encryption/decryption, compression |
| 5 | **Session** | Establishes, manages, and terminates sessions between applications |
| 4 | **Transport** | Provides reliable process-to-process communication |
| 3 | **Network** | Implements end-to-end data routing |
| 2 | **Data Link** | Provides node-to-node reliable transmission |
| 1 | **Physical** | Transmits raw bit streams over physical medium |

##### 1.2.3.2.1 Data Flow

- **Sender**: Data starts at the Application layer, is processed downward through each layer, and is finally transmitted as binary signals at the Physical layer.
- **Receiver**: Binary signals are processed at the Physical layer, move upward through each layer, and are finally reconstructed into usable data at the Application layer.

##### 1.2.3.2.2 Pros

Establishes unified communication standards and reduces development difficulty through clear layer separation.

##### 1.2.3.2.3 Cons

Overly idealistic and structurally too complex for direct practical engineering implementation.

#### 1.2.3.3 OSI vs TCP/IP Layer Mapping

| OSI Layer | OSI Name | TCP/IP Layer | TCP/IP Name | Merged? |
|-----------|----------|--------------|-------------|---------|
| 7 | Application | 4 | Application | ✅ Merged |
| 6 | Presentation | 4 | Application | ✅ Merged |
| 5 | Session | 4 | Application | ✅ Merged |
| 4 | Transport | 3 | Transport | ❌ Same |
| 3 | Network | 2 | Internet | ❌ Same (renamed) |
| 2 | Data Link | 1 | Network Interface | ✅ Merged |
| 1 | Physical | 1 | Network Interface | ✅ Merged |

#### 1.2.3.4 TCP/IP Model (4 Layers)

Practical implementation standard used in actual networking.

| Layer | Name | Main Protocols | Function |
|-------|------|----------------|----------|
| 4 | **Application** | HTTP, FTP, SMTP, DNS | Application-specific protocols |
| 3 | **Transport** | TCP, UDP | Process-to-process communication |
| 2 | **Internet** | IP, ICMP, ARP | End-to-end data routing |
| 1 | **Network Interface** | Ethernet, Wi-Fi | Binary signal transmission over physical medium |

##### 1.2.3.4.1 Key Protocols

- **Application Layer**: HTTP (web browsing), FTP (file transfer), SMTP (email), DNS (domain name resolution)
- **Transport Layer**: TCP (reliable, slower), UDP (unreliable, fast)
- **Internet Layer**: IP (addressing), ICMP (error reporting), ARP (address resolution)

## 1.3 Transport Layer Protocols: TCP and UDP

The Transport layer is responsible for process-to-process communication. Its two most important protocols are **TCP** and **UDP**.

### 1.3.1 TCP vs UDP Comparison

| Feature | UDP | TCP |
|---------|-----|-----|
| **Connection** | Connectionless | Connection-oriented (3-way handshake to establish, 4-way to terminate) |
| **Reliability** | No guarantee of delivery or order | Guaranteed delivery with correct order |
| **Latency** | Low latency, fast transmission | Higher latency due to acknowledgment and retransmission |
| **Data Size** | Small data, high-frequency transmission | Large data transmission |
| **Use Cases** | Gaming, voice calls, live streaming, DNS, IoT | File transfer, web browsing, email, payment, remote login |
| **Requirements** | Low latency, high real-time requirements | High data integrity, acceptable delay |

### 1.3.2 Connection Analogy

- **TCP (Phone Call)**: Connection-based and reliable
  - Call must be connected first
  - Two-way communication
  - Hang up when finished

- **UDP (Text Message)**: Connectionless and unreliable
  - Did the recipient receive it?
  - Is the content complete?
  - Unknown network conditions

### 1.3.3 TCP Three-Way Handshake and Four-Way Termination

#### Three-Way Handshake (Establish Connection)

1. Client sends a request packet, requesting connection.
2. Server receives the request and replies, indicating that the connection is possible.
3. Client receives the reply and sends a packet again to establish the connection.

**Terminology:**
- **SYN**: Synchronize bit. SYN = 1 indicates a connection request.
- **ACK**: Acknowledgment bit. ACK = 1 indicates acknowledgment is valid.
- **ack**: Acknowledgment number = sender's sequence number + 1.
- **seq**: Sequence number. Random, uncertain, non-fixed value.

#### Four-Way Handshake (Disconnect)

1. Active side sends a packet requesting disconnection.
2. Passive side receives the request and replies immediately, indicating preparation for disconnection.
3. Passive side sends a packet again when ready, indicating disconnection is possible.
4. Active side receives the acknowledgment and sends a final packet to complete disconnection.

**Terminology:**
- **FIN = 1**: Indicates a disconnection request.

> **Why four ways?** TCP is full-duplex (both sides can send data independently). Each direction must be closed separately, which is why two FIN/ACK pairs are needed.

## 1.4 Network Addressing and Name Resolution in Practice

Beyond IP addresses and port numbers, real-world networking relies on several mapping and resolution mechanisms.

### 1.4.1 DNS (Domain Name System)

DNS translates human-readable domain names (e.g., `google.com`) into machine-readable IP addresses (e.g., `142.250.80.46`).

#### Why DNS Matters

Without DNS, users would have to remember IP addresses for every website or service. DNS is often called the **phonebook of the internet**.

#### DNS Resolution Process

1. User enters `www.example.com` in a browser.
2. Browser checks local cache; if not found, queries the OS resolver.
3. OS queries the configured DNS server (usually provided by the ISP or a public DNS like `8.8.8.8` or `1.1.1.1`).
4. If the DNS server does not have the record, it queries upstream servers recursively until it finds the authoritative name server for the domain.
5. The authoritative server returns the IP address.
6. The result is cached and returned to the browser, which then initiates an HTTP/TCP connection.

#### Common DNS Records

| Record Type | Purpose | Example |
|-------------|---------|---------|
| **A** | Maps a domain to an IPv4 address | `example.com → 93.184.216.34` |
| **AAAA** | Maps a domain to an IPv6 address | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | Alias to another domain | `www.example.com → example.com` |
| **MX** | Mail server for the domain | `example.com → mail.example.com` |
| **NS** | Authoritative name server for the domain | `example.com → ns1.example.com` |
| **TXT** | Text information, often used for SPF/DKIM verification | `v=spf1 include:_spf.example.com ~all` |

### 1.4.2 MAC Addresses and ARP

#### MAC Address

A **MAC (Media Access Control) address** is a hardware address assigned to a network interface card (NIC). It is 48 bits long (6 bytes) and usually written as 6 pairs of hexadecimal digits, e.g., `00:1B:44:11:3A:B7`.

- **Uniqueness**: The first 24 bits identify the manufacturer (OUI); the last 24 bits are unique to the device.
- **Scope**: MAC addresses are used only within the local network segment (LAN).
- **Purpose**: Switches use MAC addresses to forward frames within a LAN.

#### ARP (Address Resolution Protocol)

ARP maps IP addresses to MAC addresses on a local network. When a device wants to communicate with another device on the same LAN, it uses ARP to find the corresponding MAC address.

**ARP Process:**
1. Device A knows Device B's IP address but not its MAC address.
2. Device A broadcasts an ARP request: "Who has this IP?"
3. Device B replies with its MAC address.
4. Device A stores the mapping in its ARP cache and sends the frame.

> **Command**: `arp -a` (Windows) or `ip neigh` (Linux) displays the ARP cache.

### 1.4.3 Subnet Masks, CIDR, and Gateways

#### Subnet Mask

A subnet mask divides an IP address into a **network portion** and a **host portion**. It determines which devices are on the same local network.

- Example: `255.255.255.0` means the first 3 octets are the network part and the last octet is the host part.
- CIDR notation: `/24` is equivalent to `255.255.255.0`.

#### CIDR (Classless Inter-Domain Routing)

CIDR replaces the old class-based IP allocation system (Class A, B, C) with a more flexible notation using a prefix length.

| CIDR | Subnet Mask | Hosts per Network | Example |
|------|-------------|-------------------|---------|
| /24 | 255.255.255.0 | ~254 | 192.168.1.0/24 |
| /16 | 255.255.0.0 | ~65,534 | 10.0.0.0/16 |
| /8 | 255.0.0.0 | ~16,777,214 | 10.0.0.0/8 |

> **Quick calculation**: Number of usable hosts = 2^(32 - prefix) - 2 (subtract 2 for network and broadcast addresses).

#### Gateway

A **default gateway** is the device (usually a router) that forwards traffic from the local network to other networks, including the internet. If a destination IP is outside the local subnet, the device sends the packet to the gateway.

### 1.4.4 NAT (Network Address Translation)

NAT allows multiple devices on a private network to share one or more public IP addresses when accessing the internet. It is the primary mechanism that has extended the life of IPv4.

#### How NAT Works

1. A device with a private IP (e.g., `192.168.1.10`) sends a request to an internet server.
2. The router replaces the private source IP with the router's public IP.
3. The router tracks the translation in a NAT table.
4. When the response returns, the router translates the destination back to the private IP and forwards it.

#### Types of NAT

| Type | Description |
|------|-------------|
| **SNAT (Source NAT)** | Changes the source IP address, typically used for outbound internet access from private networks. |
| **DNAT (Destination NAT)** | Changes the destination IP address, typically used for port forwarding to internal servers. |
| **PAT / NAT Overload** | Many private IPs share one public IP by using different source port numbers. This is the most common home-router NAT. |

#### NAT and DevOps

- NAT is common in cloud environments (VPCs, private subnets).
- Kubernetes services and cloud load balancers often use NAT or proxy mechanisms to expose internal pods.
- Port forwarding is a form of DNAT that exposes internal services (e.g., `ssh user@public-ip -p 2222` → internal server `192.168.1.50:22`).

## 1.5 HTTP/HTTPS Fundamentals

HTTP and HTTPS are the most widely used application-layer protocols in modern networking, especially for web applications and DevOps work.

### 1.5.1 HTTP Basics

**HTTP (Hypertext Transfer Protocol)** is a request-response protocol used to transfer web pages, APIs, and other resources between clients and servers.

#### HTTP Request Structure

```http
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
```

Components:
- **Method**: What action to perform (e.g., `GET`, `POST`, `PUT`, `DELETE`)
- **Path**: Resource location on the server (e.g., `/index.html`)
- **Version**: HTTP version (e.g., `HTTP/1.1`, `HTTP/2`, `HTTP/3`)
- **Headers**: Metadata about the request
- **Body**: Optional data sent with the request (common in `POST`/`PUT`)

#### HTTP Response Structure

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234

<html>...</html>
```

Components:
- **Status code**: Result of the request (e.g., `200`, `404`, `500`)
- **Headers**: Metadata about the response
- **Body**: The actual returned data

### 1.5.2 HTTPS and TLS

**HTTPS (HTTP Secure)** is HTTP encrypted with **TLS/SSL** (Transport Layer Security / Secure Sockets Layer). TLS provides:

- **Encryption**: Prevents eavesdropping on transmitted data.
- **Authentication**: Verifies the server's identity via certificates.
- **Integrity**: Ensures data is not tampered with during transit.

#### TLS Handshake (Simplified)

1. Client sends supported TLS versions and cipher suites.
2. Server responds with its certificate and chosen cipher suite.
3. Client validates the certificate and generates a session key.
4. Client and server agree on the session key (often using asymmetric encryption).
5. Subsequent communication is encrypted with the session key.

> **Port 443** is the default port for HTTPS; port 80 is the default for HTTP.

### 1.5.3 Common HTTP Methods

| Method | Purpose | Idempotent* |
|--------|---------|-------------|
| **GET** | Retrieve a resource | Yes |
| **POST** | Submit data to create a resource | No |
| **PUT** | Replace or update a resource | Yes |
| **PATCH** | Partially update a resource | No |
| **DELETE** | Remove a resource | Yes |
| **HEAD** | Retrieve headers only | Yes |
| **OPTIONS** | Describe available methods | Yes |

*Idempotent means the same request can be repeated without different side effects.

### 1.5.4 Common HTTP Status Codes

| Code Range | Category | Examples |
|------------|----------|----------|
| **1xx** | Informational | `100 Continue` |
| **2xx** | Success | `200 OK`, `201 Created`, `204 No Content` |
| **3xx** | Redirection | `301 Moved Permanently`, `302 Found`, `304 Not Modified` |
| **4xx** | Client Error | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| **5xx** | Server Error | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

> **DevOps relevance**: Status codes are essential for monitoring, alerting, and health checks. `502` and `503` often indicate backend or load balancer issues.

## 1.6 Network Troubleshooting Tools and Commands

A DevOps engineer spends significant time debugging network issues. The following tools are indispensable.

### 1.6.1 Connectivity Testing

#### `ping`

Tests reachability and measures round-trip time using ICMP echo requests.

```bash
ping google.com          # macOS/Linux (press Ctrl+C to stop)
ping -n 4 google.com     # Windows: send 4 packets
ping -c 4 google.com     # Linux/macOS: send 4 packets
```

Common outputs:
- `Reply from ...`: Target is reachable.
- `Request timed out`: Packet did not return (could be firewall, routing issue, or target down).
- `Destination unreachable`: Router cannot deliver the packet.

#### `traceroute` / `tracert`

Shows the route/path taken through intermediate routers to reach a destination.

```bash
traceroute google.com    # Linux/macOS
tracert google.com       # Windows
```

Useful for identifying where along the path a connection fails.

### 1.6.2 DNS Verification

#### `nslookup`

```bash
nslookup google.com
nslookup -type=mx example.com
```

#### `dig` (Linux/macOS, more detailed)

```bash
dig google.com
dig @8.8.8.8 google.com  # Query specific DNS server
```

### 1.6.3 Port and Connection Inspection

#### `netstat` / `ss`

Display active connections, listening ports, and routing tables.

```bash
# Linux (modern)
ss -tlnp              # Show TCP listening ports with process names
ss -tuln             # Show all UDP and TCP listening ports

# Linux/macOS (legacy)
netstat -tlnp        # Show TCP listening ports with process names
netstat -an          # Show all connections and ports
```

> These are critical for verifying whether a service is actually listening on the expected port.

#### `lsof`

```bash
lsof -i :80          # Show which process is using port 80
lsof -i tcp:8080     # Show process using TCP port 8080
```

### 1.6.4 Packet Capture

#### Wireshark

A graphical, cross-platform packet analyzer. Wireshark captures and inspects packets at the network interface level, allowing deep analysis of protocols like TCP, UDP, HTTP, DNS, and TLS.

**Common use cases:**
- Diagnosing connection failures
- Analyzing slow network performance
- Inspecting TLS handshake failures
- Verifying DNS responses

> **Tip**: Capture filters reduce noise. Examples: `tcp port 80`, `host 192.168.1.1`, `icmp`.

#### tcpdump

A command-line packet analyzer available on most Unix-like systems.

```bash
# Capture all packets on interface eth0
sudo tcpdump -i eth0

# Capture only HTTP traffic on port 80
sudo tcpdump -i eth0 port 80

# Save capture to file for later analysis in Wireshark
sudo tcpdump -i eth0 -w capture.pcap

# Capture DNS traffic
sudo tcpdump -i eth0 port 53
```

> **Warning**: Packet capture can be resource-intensive and may capture sensitive data. Use capture filters to limit scope, and ensure you have permission to capture on the network.

### 1.6.5 HTTP Testing

#### `curl`

A versatile command-line tool for testing HTTP/HTTPS requests.

```bash
# Simple GET request
curl https://api.example.com/users

# Show response headers
curl -I https://example.com

# Follow redirects
curl -L https://example.com

# POST JSON data
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"alice","age":30}'

# Verbose output (shows TLS handshake, headers, etc.)
curl -v https://example.com
```

#### `wget`

```bash
wget https://example.com/file.zip
wget --spider https://example.com  # Check if URL is reachable without downloading
```

## 1.7 Chapter Summary

- **Network Architecture**: C/S provides rich local experiences; B/S offers accessibility and easier deployment. DevOps must support both, with different monitoring and deployment strategies.
- **Core Elements**: IP addresses identify devices, port numbers identify services, and protocols define communication rules.
- **Models**: OSI is a theoretical 7-layer model; TCP/IP is the practical 4-layer model used on the internet.
- **Transport Layer**: TCP is reliable and connection-oriented; UDP is fast and connectionless.
- **Practical Addressing**: DNS maps names to IPs, ARP maps IPs to MAC addresses, CIDR defines subnets, and NAT enables private networks to share public IPs.
- **HTTP/HTTPS**: The dominant application-layer protocol for web services. HTTPS adds encryption and authentication via TLS.
- **Troubleshooting**: `ping`, `traceroute`, `dig`, `ss`/`netstat`, `curl`, `tcpdump`, and Wireshark are essential tools for diagnosing network and application-layer issues.

# 2. Socket Programming

Before writing network programs, you must understand how to convert data into bytes for transmission and back again for use. This section covers the fundamentals of Python data encoding for network communication.

## 2.1 Python Data Encoding for Network Transmission

All data (strings, numbers, containers) must be converted to byte sequences (binary data) before transmission.

### 2.1.1 String Encoding/Decoding

| Operation | Direction | Description |
|-----------|-----------|-------------|
| **encode** | Data → Binary | Converts human-readable data to transmittable binary format |
| **decode** | Binary → Data | Converts binary data back to human-readable format |

#### 2.1.1.1 Example

```python
# String to binary (encode)
original_string = "hello world"
byte_data = original_string.encode()
print(f"Original: {original_string}")
print(f"Encoded:  {byte_data}")
# Output: b'hello world'

# Binary back to string (decode)
decoded_string = byte_data.decode()
print(f"Decoded:  {decoded_string}")
# Output: hello world

# Non-ASCII characters (e.g., Chinese)
chinese_text = "你好世界"
byte_data_cn = chinese_text.encode('utf-8')
print(f"Original: {chinese_text}")
print(f"Encoded:  {byte_data_cn}")
# Output: b'\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c'

decoded_cn = byte_data_cn.decode('utf-8')
print(f"Decoded:  {decoded_cn}")
# Output: 你好世界
```

**Key points:**
- `encode()` converts a string to bytes (default encoding is UTF-8).
- `decode()` converts bytes back to a string.
- The `b` prefix indicates byte sequences.
- Non-ASCII characters (Chinese, emoji, etc.) require UTF-8 encoding.

### 2.1.2 Container Data (Lists, Dictionaries)

Containers cannot be directly encoded. They must be converted to a string first (e.g., JSON), then encoded to binary.

#### 2.1.2.1 Process

```
Container → String (JSON) → Binary Data
```

#### 2.1.2.2 Example

```python
import json

list1 = ['apple', 'banana', 'watermelon']
# Step 1: Convert list to JSON string
str_list = json.dumps(list1)  # '["apple", "banana", "watermelon"]'
# Step 2: Encode string to binary
bytelist = str_list.encode()   # b'[...]'

# Reverse process:
strinfo2 = bytelist.decode()   # JSON string
list2 = json.loads(strinfo2)   # Original list
```

## 2.2 Socket Basics

**Socket** is a technical means to implement network programming for data transmission.

- **UDP Socket**: Connectionless, data transmission is unreliable, but efficiency is higher
- **TCP Socket**: Connection-oriented, data transmission is secure and stable, but efficiency is relatively lower

Python socket programming module import:
```python
import socket
```

## 2.3 Socket API Core Parameters

Function signature for creating a Socket:
```python
socket.socket(address_family, socket_type, proto=0, fileno=None)
```

### address_family — Address Type

| Value | Description |
|-------|-------------|
| `socket.AF_INET` | IPv4 (most common) |
| `socket.AF_INET6` | IPv6 |
| `socket.AF_UNIX` | Unix domain socket — IPC on the same machine (Linux/macOS only) |
| `socket.AF_BLUETOOTH` | Bluetooth communication |

### socket_type — Transmission Mode

| Value | Description |
|-------|-------------|
| `socket.SOCK_STREAM` | TCP: connection-oriented, reliable, stream-based |
| `socket.SOCK_DGRAM` | UDP: connectionless, unreliable, datagram-based |
| `socket.SOCK_RAW` | Raw socket: direct network-layer access; requires admin privileges; used for custom protocols or packet capture |
| `socket.SOCK_SEQPACKET` | Ordered, reliable, connection-oriented datagrams (rarely used) |

### proto — Protocol Number (Optional)

Default is `0`, the system automatically selects from the first two parameters. Only needed when using `SOCK_RAW`:

| Value | Description |
|-------|-------------|
| `socket.IPPROTO_TCP` (6) | TCP |
| `socket.IPPROTO_UDP` (17) | UDP |
| `socket.IPPROTO_ICMP` (1) | ICMP — used for `ping` |

**`fileno`** (Optional): Wraps an existing OS file descriptor as a socket object. Only used for low-level system programming, can be ignored for daily use.

## 2.4 UDP Socket

UDP socket is connectionless, with high efficiency but no guarantee of data transmission security.

### UDP Characteristics

- **Possible Packet Loss**: No guarantee of data arrival
- **Simple and Efficient**: Simple transmission process, easy to implement
- **Datagram Transmission**: Data is transmitted in packets
- **Connectionless**: When sending data, client IP, port and target IP/port must be included

### UDP Server Complete Process

```python
import socket

# 1. Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Bind IP and port
server.bind(('127.0.0.1', 8080))
# Address options explanation:
#   ('127.0.0.1', 8080)  - IPv4 loopback, local access only
#   ('localhost', 8080)  - Hostname resolves to 127.0.0.1, for development only
#   ('0.0.0.0', 8080)    - All network interfaces, allows external/LAN access
#   ('', 8080)           - Empty string, equivalent to '0.0.0.0'
#   ('192.168.1.10', 8080) - Bind to specific network interface

# Special port value: port=0 lets system auto-assign available port
# server.bind(('127.0.0.1', 0))
# actual_port = server.getsockname()[1]

# 3. Receive and send data (loop mode)
while True:
    # recvfrom() blocks until message arrives, returns (data_bytes, (client_ip, client_port))
    info, addr = server.recvfrom(1024)  # 1024 = maximum bytes to receive per call

    if info.decode() == 'exit':
        break

    print(f"Message: {info.decode()}")
    print(f"From: {addr}")

    # sendto must pass addr back
    server.sendto("Reply from server".encode(), addr)

# 4. Close socket
server.close()
```

**Key Binding Points:**

| Syntax | Correct? | Explanation |
|--------|----------|-------------|
| `bind(('127.0.0.1', 8080))` | ✓ | Must use tuple |
| `bind('127.0.0.1', 8080)` | ✗ | Missing parentheses |

- **IPv6 loopback**: `'::1'` is equivalent to `'127.0.0.1'`
- **IPv6 wildcard**: `'::'` is equivalent to `'0.0.0.0'`

### UDP Client Complete Process

```python
import socket

# 1. Create UDP socket (client doesn't need to bind)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Send and receive data (loop mode)
while True:
    msg = input("Message: ")

    # sendto: 1st parameter=data(bytes), 2nd parameter=target(ip, port) tuple
    client.sendto(msg.encode(), ('127.0.0.1', 8080))

    if msg == 'exit':
        break

    info, addr = client.recvfrom(1024)
    print(f"Server reply: {info.decode()}")

# 3. Close socket
client.close()
```

### UDP Applicable Scenarios

| Scenario | Reason |
|----------|--------|
| Video streaming, live broadcast, video chat | High real-time requirements, can tolerate some packet loss |
| Network broadcast, mass sending | Need one-to-many transmission |
| Gaming | Low latency requirement higher than reliability |

## 2.5 TCP Socket

TCP socket is connection-oriented, providing secure and stable data transmission, but with relatively lower efficiency.

### TCP Characteristics

- **Reliable Transmission**: No loss, disorder, errors, or duplication
- **Connection Mechanism**: Establish data connection before communication
- **Acknowledgment**: Automatically confirm received data
- **Normal Disconnection**: Properly disconnect after communication ends

### TCP Connection Establishment and Termination

#### Three-way Handshake (Establish Connection)

1. Client sends request packet, requesting connection
2. Server receives request and replies, indicating connection is possible
3. Client receives reply, sends packet again to establish connection

**Terminology:**
- **SYN**: Synchronize bit. SYN = 1 indicates connection request
- **ACK**: Acknowledgment bit. ACK = 1 indicates acknowledgment is valid, ACK = 0 indicates invalid
- **ack**: Acknowledgment number = sender's sequence number + 1
- **seq**: Sequence number. Random, uncertain, non-fixed value

#### Four-way Handshake (Disconnect)

1. Active side sends packet requesting disconnection
2. Passive side receives request and replies immediately, indicating preparation for disconnection
3. Passive side sends packet again when ready, indicating disconnection is possible
4. Active side receives acknowledgment and sends final packet to complete disconnection

**Terminology:**
- **FIN = 1**: Indicates disconnection request

### TCP Server Complete Process

```python
import socket

# 1. Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind address
server.bind(('127.0.0.1', 9090))

# 3. Set listening (maximum pending connections)
server.listen(5)

# 4. Accept connection (blocks until client connects, three-way handshake occurs here)
# accept() returns (conn_object, (client_ip, client_port))
# conn = connection object — all subsequent send/recv use conn, not server
conn, addr = server.accept()
print(f"Connected by {addr}")

# 5. Send and receive data (loop mode)
while True:
    # recv() doesn't need address (connection-oriented)
    info = conn.recv(1024)

    # When client disconnects unexpectedly, recv returns empty string
    if info.decode() == '':
        print("Client disconnected")
        break

    if info.decode() == 'exit':  # Client sends exit signal
        break

    print(f"Received: {info.decode()}")
    conn.send("Reply".encode())

# 6. Close connection (four-way handshake)
conn.close()     # Close connection object
server.close()   # Close server socket
```

### TCP Client Complete Process

```python
import socket

# 1. Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to server (automatically triggers three-way handshake)
client.connect(('127.0.0.1', 9090))

# 3. Send and receive data (loop mode)
while True:
    msg = input("Message: ")

    # ⚠ Cannot send empty string, will cause issues
    if msg == '':
        continue

    client.send(msg.encode())  # send() has only one parameter, data must be bytes

    if msg == 'exit':
        break

    data = client.recv(1024)
    print(f"Server reply: {data.decode()}")

# 4. Close socket (automatically triggers four-way handshake)
client.close()
```

### TCP Notes and Applicable Scenarios

**Important Details:**

| Situation | Explanation |
|-----------|-------------|
| When peer exits | If this side is blocked in `recv`, `recv` returns empty string immediately |
| Sending when peer doesn't exist | Will raise `BrokenPipeError` |
| `recv(n)` | Reads from buffer, maximum n bytes; excess data remains in buffer |
| Empty string | `client.send("".encode())` will cause issues, must validate before sending |

**TCP Applicable Scenarios:**

- File transfer, data download, photo upload, website access
- Email sending and receiving
- Point-to-point data transmission: login, remote access, red packets, one-on-one chat

**UDP vs TCP Scenario Comparison:**

| Requirement | Recommended Protocol |
|-------------|---------------------|
| High accuracy, large data transmission | TCP |
| Low reliability requirement, free transmission | UDP |
| Video streaming, live broadcast, video chat | UDP |
| Network broadcast, mass sending | UDP |
| Gaming (high real-time) | UDP |

## 2.6 TCP Sticky Packet Problem and Solutions

TCP is a **stream-oriented** protocol. Unlike UDP, where each `send` corresponds to one datagram, TCP treats data as a continuous stream of bytes. The operating system uses **send and receive buffers** to manage this stream, which can lead to the **sticky packet** problem.

### 2.6.1 How Sticky Packets Happen

When a client sends multiple small messages in quick succession, TCP may combine them into a single stream segment before sending. On the receiving side, `recv(n)` simply reads up to `n` bytes from the receive buffer, regardless of how many logical messages were sent.

**Example:**

```python
# Client sends three separate messages
client.send("abc".encode())
client.send("123".encode())
client.send("456".encode())
```

On the server, `recv(1024)` might receive all of them together as one chunk:

```
b'abc123456'
```

This makes it impossible for the receiver to know where one message ends and the next begins.

**Causes:**
- **Sender side**: The OS may merge small messages to improve efficiency (Nagle's algorithm).
- **Receiver side**: The receive buffer may contain multiple messages if the receiver is slower than the sender.

### 2.6.2 Demonstrating the Problem

```python
# server.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

info = conn.recv(10)  # Might receive b'abc123456' all at once
print(f"Received: {info.decode()}")

conn.send("Hello from server".encode())
conn.close()
server.close()
```

```python
# client.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

client.send("abc".encode())
client.send("123".encode())
client.send("456".encode())

msg = client.recv(1024)
print(f"Server reply: {msg.decode()}")
client.close()
```

### 2.6.3 Naive Workaround: Delay Between Sends

Adding `time.sleep(1)` between sends can reduce the problem because the OS may send the first packet before the next message is written. However, this is **not reliable** and severely hurts performance.

```python
import time

client.send("abc".encode())
time.sleep(1)
client.send("123".encode())
time.sleep(1)
client.send("456".encode())
```

> ⚠️ Do **not** use this in production. It is only a quick demonstration fix.

### 2.6.4 Proper Solution: Length-Prefix Header

The standard solution is to send a **fixed-length header** that contains the size of the upcoming message. The receiver first reads the header, then reads exactly that many bytes.

**Design:**
1. Send the message length as a 4-byte integer header.
2. Send the actual message data.
3. Receiver reads 4 bytes, unpacks the length, then reads exactly that many bytes.

In Python, use the `struct` module to convert integers to and from 4-byte binary format:

```python
import struct

# Pack an integer into 4 bytes (little-endian by default)
length_bytes = struct.pack("i", 100)  # 4 bytes
print(len(length_bytes))  # 4

# Unpack back to integer
length_tuple = struct.unpack("i", length_bytes)
print(length_tuple)      # (100,)
print(length_tuple[0])   # 100
```

> **Format `"i"`**: signed 4-byte integer. This gives a fixed header size of 4 bytes, supporting messages up to roughly 2 GB.

### 2.6.5 Server and Client with Length-Prefix Protocol

```python
# server.py
import socket
import struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()
print(f"Connected by {addr}")

while True:
    # Step 1: Read 4-byte header
    header = conn.recv(4)
    if not header:
        print("Client disconnected")
        break

    # Step 2: Unpack to get message length
    msg_length = struct.unpack('i', header)[0]

    # Step 3: Read exactly msg_length bytes
    msg = conn.recv(msg_length)
    if not msg:
        print("Client disconnected unexpectedly")
        break

    text = msg.decode()
    print(f"From client: {text}")

    if text == 'exit':
        break

conn.close()
server.close()
```

```python
# client.py
import socket
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    byte_info = info.encode()
    length = len(byte_info)

    # Send 4-byte length header, then the data
    client.send(struct.pack('i', length))
    client.send(byte_info)

    if info == 'exit':
        break

client.close()
```

### 2.6.6 Reusable Helper Functions

For real projects, it is cleaner to wrap the length-prefix logic in reusable functions.

```python
# util.py
import struct


def send_with_length(sock, message):
    """Send a string message with a 4-byte length header."""
    data = message.encode()
    length = len(data)
    sock.send(struct.pack('i', length))
    sock.send(data)


def recv_with_length(sock):
    """Receive a string message using a 4-byte length header.

    Returns the decoded message, or an empty string if the peer disconnected.
    """
    header = sock.recv(4)
    if not header:
        return ''

    length = struct.unpack('i', header)[0]
    data = sock.recv(length)
    if not data:
        return ''

    return data.decode()
```

```python
# server.py
import socket
from util import send_with_length, recv_with_length

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

while True:
    msg = recv_with_length(conn)
    if msg == '':
        print("Client disconnected unexpectedly")
        break
    if msg == 'exit':
        print("Client exited")
        break

    print(f"From client: {msg}")
    send_with_length(conn, "Hello from server")

conn.close()
server.close()
```

```python
# client.py
import socket
from util import send_with_length, recv_with_length

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    send_with_length(client, info)

    if info == 'exit':
        break

    reply = recv_with_length(client)
    print(f"Server reply: {reply}")

client.close()
```

### 2.6.7 Important Notes

- The receiver should not use `recv(1024)` for arbitrary messages. It should read exactly the announced length, possibly in a loop if the data is large.
- For production systems, consider using established protocols or libraries (e.g., HTTP, JSON-RPC, gRPC, `asyncio` streams, `struct` with network byte order `!i`).
- `struct.pack("i", ...)` uses the machine's native byte order by default. For cross-platform communication, use `!i` (network byte order / big-endian).

---

## 2.7 UDP vs TCP API Comparison

| Step | UDP | TCP |
|------|-----|-----|
| **Create socket** | `socket.SOCK_DGRAM` | `socket.SOCK_STREAM` |
| **Server bind** | `server.bind((ip, port))` | `server.bind((ip, port))` |
| **Server listen** | ❌ Not needed | `server.listen(n)` |
| **Server accept** | ❌ Not needed | `conn, addr = server.accept()` |
| **Send** | `socket.sendto(data, (ip, port))` | `socket.send(data)` |
| **Receive** | `data, addr = socket.recvfrom(n)` | `data = socket.recv(n)` |
| **Close** | `socket.close()` | `conn.close()` then `server.close()` |

> **Key difference**: UDP `sendto`/`recvfrom` always carry the address; TCP `send`/`recv` don't need it because the connection is already established.

## 2.8 Non-Blocking Sockets

By default, socket methods like `accept()` and `recv()` are **blocking**: the program pauses until a client connects or data arrives. This is fine for a single client, but it makes a single thread unable to handle many clients simultaneously.

### 2.8.1 What Is Non-Blocking?

A **non-blocking socket** returns immediately if no data or connection is available, raising a `BlockingIOError` instead of waiting. This allows one thread to poll many sockets in a loop.

```python
server.setblocking(False)  # Make the socket non-blocking
```

### 2.8.2 Handling Multiple Clients with Non-Blocking Sockets

The server maintains a list of connected client sockets. In each loop iteration:

1. Try to `accept()` a new connection. If none, catch the exception and continue.
2. Loop through all existing connections and try to `recv()` from each.
3. Remove disconnected clients from the list.

```python
# server.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)

connections = []

while True:
    # Try to accept a new connection
    try:
        conn, addr = server.accept()
        conn.setblocking(False)
        connections.append(conn)
        print(f"New connection from {addr}")
    except BlockingIOError:
        pass

    # Check each connection for incoming data
    disconnected = []
    for conn in connections:
        try:
            msg = conn.recv(1024)
            if not msg:
                # Client closed the connection gracefully
                disconnected.append(conn)
                continue

            text = msg.decode()
            if text == 'exit':
                disconnected.append(conn)
                continue

            print(f"Received: {text}")
            conn.send("Hello from server".encode())
        except BlockingIOError:
            # No data available from this client right now
            pass
        except ConnectionResetError:
            disconnected.append(conn)

    # Remove disconnected clients
    for conn in disconnected:
        if conn in connections:
            connections.remove(conn)
        conn.close()
```

```python
# client.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    client.send(info.encode())
    if info == 'exit':
        break

    msg = client.recv(1024)
    print(f"Server reply: {msg.decode()}")

client.close()
```

### 2.8.3 Pros and Cons of Non-Blocking Sockets

| Pros | Cons |
|------|------|
| One thread can manage many connections | CPU usage is high because of constant polling |
| Simple to understand conceptually | Many `try/except` blocks make code messy |
| No need for threading or multiprocessing | Inefficient when most connections are idle |

For serious servers, the next section (IO multiplexing) is usually preferred over pure non-blocking polling.

---

## 2.9 IO Multiplexing with `select`

**IO multiplexing** lets the operating system monitor multiple sockets and notify the program only when one of them is ready for reading or writing. It is more efficient than polling every socket in a loop.

In Python, the `select` module provides this capability. The core function is:

```python
readable, writable, exceptional = select.select(rlist, wlist, xlist)
```

| Parameter | Meaning |
|-----------|---------|
| `rlist` | Sockets to monitor for incoming data (read-ready) |
| `wlist` | Sockets to monitor for ability to send (write-ready) |
| `xlist` | Sockets to monitor for exceptional conditions (usually empty) |

The function **blocks** until at least one socket is ready, then returns three lists of ready sockets.

### 2.9.1 Basic Workflow

1. Put the server socket into the `rlist`.
2. When `select` returns, check each ready socket:
   - If the ready socket is the **server socket**, call `accept()` and add the new connection to `rlist`.
   - If the ready socket is a **client connection**, call `recv()` to read data.
3. Remove closed connections from the `rlist`.

### 2.9.2 Server with `select`

```python
import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)

# Start by monitoring the server socket for incoming connections
read_list = [server]

while True:
    readable, _, _ = select.select(read_list, [], [])

    for sock in readable:
        if sock is server:
            # New client connection
            conn, addr = server.accept()
            conn.setblocking(False)
            read_list.append(conn)
            print(f"New connection from {addr}")
        else:
            # Existing client sent data
            try:
                msg = sock.recv(1024)
                if not msg:
                    # Client disconnected
                    print("Client disconnected")
                    read_list.remove(sock)
                    sock.close()
                    continue

                text = msg.decode()
                if text == 'exit':
                    print("Client exited")
                    read_list.remove(sock)
                    sock.close()
                    continue

                print(f"From client: {text}")
                sock.send("Hello from server".encode())
            except ConnectionResetError:
                read_list.remove(sock)
                sock.close()
```

```python
# client.py (same as before)
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    client.send(info.encode())
    if info == 'exit':
        break

    msg = client.recv(1024)
    print(f"Server reply: {msg.decode()}")

client.close()
```

### 2.9.3 Advantages of `select`

| Feature | Benefit |
|---------|---------|
| Single-threaded concurrency | Handle many clients without threads |
| Event-driven | Only process sockets that are ready |
| Lower CPU usage | No busy polling; blocked until something happens |
| Portable | `select` is available on Unix, Linux, macOS, and Windows |

### 2.9.4 Limitations and Alternatives

| Limitation | Explanation |
|------------|-------------|
| Scalability | `select` has a limited number of file descriptors (often 1024 on Linux) |
| Performance | For thousands of connections, `poll` or `epoll` (Linux) / `kqueue` (BSD/macOS) perform better |
| Modern Python | For high-level concurrency, `asyncio` with `async`/`await` is recommended |

### 2.9.5 Common Use Cases

- Chat servers where one thread handles many connections
- Simple TCP proxy or relay services
- Monitoring tools that wait for data from multiple sources
- Learning the foundations before moving to `asyncio` or `selectors`

> **Summary**: Non-blocking sockets + `select` is a classic way to build single-threaded concurrent network servers. For modern Python projects, `asyncio` builds on the same ideas but provides a cleaner, higher-level API.
