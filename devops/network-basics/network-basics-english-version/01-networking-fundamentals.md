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
| **Pros** | Excellent UX: rich graphics/audio stored locally<br>Offline capability (single-player games, document editing)<br>Better security, data can be stored locally |
| **Cons** | Higher dev/maintenance cost (client + server)<br>Users must download updates<br>Cross-platform complexity (iOS, Android, Windows) |

### 1.1.2 B/S: Browser / Server

No installation needed; access via browser using URLs.

| Aspect | Description |
|--------|-------------|
| **Access** | Browser + URL (baidu.com, jd.com, bilibili.com) |
| **Use Cases** | Entertainment, shopping, web games (convenience-focused) |
| **Pros** | No client development needed (web page + server only)<br>Zero install for users; open browser and go<br>Easy updates: server-side only, users just refresh<br>Cross-platform: any device with a browser |
| **Cons** | Everything loaded from server → network dependent<br>Poor performance for large apps (low quality graphics/audio)<br>Limited interactivity compared to native apps |

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

2. **Network Address Translation (NAT)** (see 1.4.4)
   - Allows multiple devices on a private network to share a single public IP
   - Router translates private IP to public IP for internet access
   - Temporarily extends IPv4 lifespan but creates network complexity

3. **Classless Inter-Domain Routing (CIDR)** (see 1.4.3)
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
| Universal | `ping [IP/hostname]` | Test network connectivity (see 1.6.1) |

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
| **Uniqueness** | Each port number can only be used by one application at a time per device, per protocol (TCP and UDP are independent — e.g., DNS uses port 53 on both TCP and UDP simultaneously) |

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

**Pros**: Establishes unified communication standards and reduces development difficulty through clear layer separation.

**Cons**: Overly idealistic and structurally too complex for direct practical engineering implementation.

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

#### 1.3.3.1 Three-Way Handshake (Establish Connection)

1. Client sends a SYN packet (seq = x), requesting a connection.
2. Server replies with a SYN + ACK packet (seq = y, ack = x + 1), indicating the connection can be established.
3. Client sends an ACK packet (ack = y + 1), and the connection is formally established.

**Terminology:**
- **SYN**: Synchronize bit. SYN = 1 indicates a connection request.
- **ACK**: Acknowledgment bit. ACK = 1 indicates acknowledgment is valid.
- **ack**: Acknowledgment number = sender's sequence number + 1.
- **seq**: Sequence number. Random, uncertain, non-fixed value.

#### 1.3.3.2 Four-Way Handshake (Disconnect)

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

#### 1.4.1.1 Why DNS Matters

Without DNS, users would have to remember IP addresses for every website or service. DNS is often called the **phonebook of the internet**.

#### 1.4.1.2 DNS Resolution Process

1. User enters `www.example.com` in a browser.
2. Browser checks local cache; if not found, queries the OS resolver.
3. OS queries the configured DNS server (usually provided by the ISP or a public DNS like `8.8.8.8` or `1.1.1.1`).
4. If the DNS server does not have the record, it queries upstream servers recursively until it finds the authoritative name server for the domain.
5. The authoritative server returns the IP address.
6. The result is cached and returned to the browser, which then initiates an HTTP/TCP connection.

#### 1.4.1.3 Common DNS Records

| Record Type | Purpose | Example |
|-------------|---------|---------|
| **A** | Maps a domain to an IPv4 address | `example.com → 93.184.216.34` |
| **AAAA** | Maps a domain to an IPv6 address | `example.com → 2606:2800:220:1:248:1893:25c8:1946` |
| **CNAME** | Alias to another domain | `www.example.com → example.com` |
| **MX** | Mail server for the domain | `example.com → mail.example.com` |
| **NS** | Authoritative name server for the domain | `example.com → ns1.example.com` |
| **TXT** | Text information, often used for SPF/DKIM verification | `v=spf1 include:_spf.example.com ~all` |

### 1.4.2 MAC Addresses and ARP

#### 1.4.2.1 MAC Address

A **MAC (Media Access Control) address** is a hardware address assigned to a network interface card (NIC). It is 48 bits long (6 bytes) and usually written as 6 pairs of hexadecimal digits, e.g., `00:1B:44:11:3A:B7`.

- **Uniqueness**: The first 24 bits identify the manufacturer (OUI); the last 24 bits are unique to the device.
- **Scope**: MAC addresses are used only within the local network segment (LAN).
- **Purpose**: Switches use MAC addresses to forward frames within a LAN.

#### 1.4.2.2 ARP (Address Resolution Protocol)

ARP maps IP addresses to MAC addresses on a local network. When a device wants to communicate with another device on the same LAN, it uses ARP to find the corresponding MAC address.

**ARP Process:**
1. Device A knows Device B's IP address but not its MAC address.
2. Device A broadcasts an ARP request: "Who has this IP?"
3. Device B replies with its MAC address.
4. Device A stores the mapping in its ARP cache and sends the frame.

> **Command**: `arp -a` (Windows) or `ip neigh` (Linux) displays the ARP cache.

### 1.4.3 Subnet Masks, CIDR, and Gateways

#### 1.4.3.1 Subnet Mask

A subnet mask divides an IP address into a **network portion** and a **host portion**. It determines which devices are on the same local network.

- Example: `255.255.255.0` means the first 3 octets are the network part and the last octet is the host part.
- CIDR notation: `/24` is equivalent to `255.255.255.0`.

#### 1.4.3.2 CIDR (Classless Inter-Domain Routing)

CIDR replaces the old class-based IP allocation system (Class A, B, C) with a more flexible notation using a prefix length.

| CIDR | Subnet Mask | Hosts per Network | Example |
|------|-------------|-------------------|---------|
| /24 | 255.255.255.0 | ~254 | 192.168.1.0/24 |
| /16 | 255.255.0.0 | ~65,534 | 10.0.0.0/16 |
| /8 | 255.0.0.0 | ~16,777,214 | 10.0.0.0/8 |

> **Quick calculation**: Number of usable hosts = 2^(32 - prefix) - 2 (subtract 2 for network and broadcast addresses).

#### 1.4.3.3 Gateway

A **default gateway** is the device (usually a router) that forwards traffic from the local network to other networks, including the internet. If a destination IP is outside the local subnet, the device sends the packet to the gateway.

### 1.4.4 NAT (Network Address Translation)

NAT allows multiple devices on a private network to share one or more public IP addresses when accessing the internet. It is the primary mechanism that has extended the life of IPv4.

#### 1.4.4.1 How NAT Works

1. A device with a private IP (e.g., `192.168.1.10`) sends a request to an internet server.
2. The router replaces the private source IP with the router's public IP.
3. The router tracks the translation in a NAT table.
4. When the response returns, the router translates the destination back to the private IP and forwards it.

#### 1.4.4.2 Types of NAT

| Type | Description |
|------|-------------|
| **SNAT (Source NAT)** | Changes the source IP address, typically used for outbound internet access from private networks. |
| **DNAT (Destination NAT)** | Changes the destination IP address, typically used for port forwarding to internal servers. |
| **PAT / NAT Overload** | Many private IPs share one public IP by using different source port numbers. This is the most common home-router NAT. |

#### 1.4.4.3 NAT and DevOps

- NAT is common in cloud environments (VPCs, private subnets).
- Kubernetes services and cloud load balancers often use NAT or proxy mechanisms to expose internal pods.
- Port forwarding is a form of DNAT that exposes internal services (e.g., `ssh user@public-ip -p 2222` → internal server `192.168.1.50:22`).

## 1.5 HTTP/HTTPS Fundamentals

HTTP and HTTPS are the most widely used application-layer protocols in modern networking, especially for web applications and DevOps work.

### 1.5.1 HTTP Basics

**HTTP (Hypertext Transfer Protocol)** is a request-response protocol used to transfer web pages, APIs, and other resources between clients and servers.

#### 1.5.1.1 HTTP Request Structure

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

#### 1.5.1.2 HTTP Response Structure

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

#### 1.5.2.1 TLS Handshake (Simplified)

1. Client sends supported TLS versions and a list of cipher suites (ClientHello).
2. Server responds with the chosen cipher suite and its certificate (ServerHello + Certificate).
3. Client validates the certificate, generates a pre-master secret, encrypts it with the server's public key, and sends it to the server.
4. Both sides independently derive the same session key from the pre-master secret.
5. Subsequent communication is encrypted symmetrically with the session key.

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

#### 1.6.1.1 `ping`

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

#### 1.6.1.2 `traceroute` / `tracert`

Shows the route/path taken through intermediate routers to reach a destination.

```bash
traceroute google.com    # Linux/macOS
tracert google.com       # Windows
```

Useful for identifying where along the path a connection fails.

### 1.6.2 DNS Verification

#### 1.6.2.1 `nslookup`

```bash
nslookup google.com
nslookup -type=mx example.com
```

#### 1.6.2.2 `dig` (Linux/macOS, more detailed)

```bash
dig google.com
dig @8.8.8.8 google.com  # Query specific DNS server
```

### 1.6.3 Port and Connection Inspection

#### 1.6.3.1 `netstat` / `ss`

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

#### 1.6.3.2 `lsof`

```bash
lsof -i :80          # Show which process is using port 80
lsof -i tcp:8080     # Show process using TCP port 8080
```

### 1.6.4 Packet Capture

#### 1.6.4.1 Wireshark

A graphical, cross-platform packet analyzer. Wireshark captures and inspects packets at the network interface level, allowing deep analysis of protocols like TCP, UDP, HTTP, DNS, and TLS.

**Common use cases:**
- Diagnosing connection failures
- Analyzing slow network performance
- Inspecting TLS handshake failures
- Verifying DNS responses

> **Tip**: Capture filters reduce noise. Examples: `tcp port 80`, `host 192.168.1.1`, `icmp`.

#### 1.6.4.2 tcpdump

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

#### 1.6.5.1 `curl`

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

#### 1.6.5.2 `wget`

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


[Next: Socket Programming →](02-socket-programming.md)
