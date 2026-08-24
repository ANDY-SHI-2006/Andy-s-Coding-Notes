[Next: Socket Programming →](02-socket-programming.md)

# 1. Networking Fundamentals

A practical networking fundamentals chapter for developers and DevOps engineers.

## 1.1 Network Architecture and Core Concepts

### 1.1.1 Components of the Internet

The Internet is built from end systems, communication links, and packet switches:

- **End systems (hosts)**: devices running applications, including computers, phones, servers, TVs, and IoT devices.
- **Communication links**: wired or wireless links with different transmission rates.
- **Packet switches**: devices that forward packets based on header information, mainly routers and link-layer switches.
- **ISPs**: Internet Service Providers are networks of switches and links that provide access to end systems.

The sender divides application data into smaller pieces and adds headers to form packets. Packets can be compared to trucks, links to roads, switches to intersections, and end systems to the buildings where the data is delivered.

### 1.1.2 C/S and B/S Architectures

C/S (Client / Server) combines a local client with server-side services and is common for desktop software, games, and specialist clients. B/S (Browser / Server) exposes a Web application through a browser and usually requires no dedicated installation. Modern applications may use both approaches.

| Dimension | C/S | B/S |
| --- | --- | --- |
| Access | Usually requires installation | Browser access |
| Updates | Client and server may both change | Mostly server-side |
| Performance | Can use local resources directly | Influenced by browser, network, and server |
| Cross-platform | Multiple clients may be needed | Browser compatibility matters |
| Typical use | Desktop software, games, specialist clients | Websites, admin panels, online services |

Both architectures need authentication, authorization, encryption, logging, and monitoring. C/S also requires attention to client versions, connection stability, and updates; B/S usually emphasizes HTTP latency, status codes, TLS, reverse proxies, and load balancing.

### 1.1.3 DevOps implications

- B/S systems emphasize HTTP latency, status codes, TLS, reverse proxies, and load balancing.
- C/S systems also require attention to client versions, connection stability, latency, packet loss, and update mechanisms.
- Both need authentication, access control, logs, metrics, and tracing.

## 1.2 Network Addressing and Name Resolution

### 1.2.1 IPv4 and IPv6

IPv4 uses 32-bit addresses in dotted-decimal notation, such as `192.168.1.34`; each octet ranges from `0` to `255`. IPv6 uses 128-bit hexadecimal addresses, such as `2001:db8::1`. One run of zero groups may be compressed with `::`.

### 1.2.2 Address types

| Type | Purpose | Examples |
| --- | --- | --- |
| Public IP | Routable on the Internet | Assigned by an ISP or cloud provider |
| Private IP | Local network or VPC use | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` |
| Loopback | Refers to the local host | `127.0.0.1`, `::1` |

IPv6, CIDR, NAT, and address reclamation all help address IPv4 scarcity.

### 1.2.3 MAC, ARP, and NDP

A MAC address is usually 48 bits and identifies a network interface on a local link. Switches forward frames using MAC addresses.

ARP maps an IPv4 address to a MAC address on a local network. A host broadcasts a request, the target replies, and the result is cached. Use `arp -a` on Windows or `ip neigh` on Linux to inspect the cache.

IPv6 does not use ARP. It uses Neighbor Discovery Protocol (NDP), which is based on ICMPv6 and also supports neighbor reachability detection and router discovery.

### 1.2.4 Subnets, CIDR, and Gateways

A useful starting point for network analysis is: the IP address identifies the destination host or interface, the port identifies the process or service on that host, and the protocol defines the exchange format and rules. These are often combined as `IP:port` and a protocol, such as `192.168.1.10:443/TCP`.

An IP address provides network-layer addressing, and a port distinguishes services on the same host.

A subnet mask divides an IPv4 address into network and host portions. `255.255.255.0` is equivalent to `/24`.

| CIDR | Mask | Usable hosts in a traditional IPv4 subnet |
| --- | --- | ---: |
| `/8` | `255.0.0.0` | 16,777,214 |
| `/16` | `255.255.0.0` | 65,534 |
| `/24` | `255.255.255.0` | 254 |

For a traditional IPv4 subnet, usable hosts are usually $2^{32-p}-2$, where $p$ is the CIDR prefix length; point-to-point links, cloud networks, and IPv6 may use different rules.

A default gateway forwards traffic outside the local subnet. Useful commands are:

```bash
ip route                 # Linux
route print              # Windows
netstat -rn              # macOS
```

During troubleshooting, check whether a matching route exists, whether the next hop is correct, and whether the interface is enabled.

### 1.2.5 DNS

DNS is a distributed, hierarchical database and an application-layer protocol. It maps domain names to IP addresses and can provide other information such as mail servers.

The DNS hierarchy commonly includes:

- **Root DNS servers**: direct queries toward top-level domains.
- **Top-level domain (TLD) DNS servers**: handle domains such as `.com`, `.org`, and `.cn`.
- **Authoritative DNS servers**: store the official records for a domain.

A recursive resolver queries these servers on behalf of a client and caches results for a period defined by the TTL. Caching uses locality of reference, so most queries do not need to reach the root. If root servers are temporarily unavailable, existing cached entries can still resolve some domains. A typical lookup path is local cache, recursive resolver, root server, TLD server, authoritative server, and then a cached response back to the client.

DNS records commonly include:

| Record | Purpose |
| --- | --- |
| `A` | Name to IPv4 |
| `AAAA` | Name to IPv6 |
| `CNAME` | Alias to another name |
| `MX` | Mail server |
| `NS` | Authoritative name server |
| `TXT` | Text and validation data |

The visible sequence can differ because of browser and operating-system caches, prefetching, split DNS, and DNS over HTTPS/TLS.

### 1.2.6 NAT

NAT changes IP addresses or ports at an address boundary and commonly lets private networks access the Internet.

- **SNAT** changes the source address for outbound access.
- **DNAT** changes the destination address, often for port forwarding.
- **PAT/NAT overload** lets multiple private addresses share one public address through different ports.

NAT is not a firewall replacement. Cloud VPCs, port forwarding, and some container networks use translation or proxy mechanisms, but the exact behavior depends on the platform.

## 1.3 Network Layers and Transport Protocols

### 1.3.1 OSI and TCP/IP Models

OSI is mainly a teaching and analysis model with seven layers. TCP/IP is the more common engineering model for the Internet. Names vary slightly between textbooks; focus on responsibilities and encapsulation.

| OSI | Common TCP/IP mapping | Examples |
| --- | --- | --- |
| Application, presentation, session | Application | HTTP, DNS, SMTP |
| Transport | Transport | TCP, UDP |
| Network | Internet | IP, ICMP |
| Data link, physical | Network access | Ethernet, Wi-Fi |

Data is encapsulated from the upper layers downward when sent and decapsulated upward when received. ARP is often discussed near the network-access layer because it crosses the network/link-layer boundary.

Each layer provides services to the layer above and uses services from the layer below. Layering reduces complexity through abstraction and separation of responsibilities: an upper layer can use lower-layer capabilities without knowing every implementation detail.

The data units are commonly called **messages** at the application layer, **segments/datagrams** at the transport layer, **datagrams** at the network layer, **frames** at the link layer, and **bits** at the physical layer.

| Layer | Common devices or components | Troubleshooting clues |
| --- | --- | --- |
| Application | Web server, reverse proxy | Status codes, request logs, application latency |
| Transport | Load balancer, firewall | Listening ports, handshakes, retransmissions |
| Internet | Router, cloud route table | Addresses, routes, loss, TTL |
| Network access | Switch, NIC, wireless AP | Link state, VLAN, MAC |

### 1.3.2 TCP and UDP

| Feature | TCP | UDP |
| --- | --- | --- |
| Connection | Connection-oriented | Connectionless |
| Reliability | Acknowledgment, retransmission, ordered delivery | No delivery, order, or retransmission guarantee |
| Overhead | Higher | Lower |
| Typical use | Web, file transfer, databases | DNS, real-time media, some games and IoT |

UDP does not require applications to use only small data; applications still need to consider MTU, fragmentation, and loss. TCP also does not preserve application message boundaries, so applications must define framing.

Transport services are commonly evaluated by:

- **Reliable data transfer**: whether data arrives, arrives in order, and is not duplicated.
- **Throughput**: the number of bits transferred per unit of time.
- **Timing/latency**: how long data takes to travel from sender to receiver.
- **Security**: confidentiality, integrity, and endpoint authentication. TCP itself does not encrypt data; TLS or another protocol is needed.

TCP also provides flow control and congestion control. The receive window prevents a sender from exceeding receiver capacity, while the congestion window adapts the sending rate to network conditions. These mechanisms affect throughput but do not remove the need for application timeouts and retry policies.

### 1.3.3 TCP Data and Exceptional States

TCP presents application data as a continuous byte stream and does not preserve `send()` or `write()` boundaries. Applications commonly use length prefixes, delimiters, or fixed-size messages to define framing.

`RST` immediately resets a connection. Common causes include an unlistened port, an actively rejected connection, or a stateful middlebox losing connection state. After a graceful close, the active closer may enter `TIME_WAIT` so delayed old segments cannot affect a later connection.

### 1.3.4 TCP Connection Setup and Close

1. The client sends `SYN` with an initial sequence number.
2. The server returns `SYN + ACK`, confirming the client and declaring its own sequence number.
3. The client returns `ACK`, and the connection can carry data.

![[tcp-three-way-handshake.png]]

> The diagram above is a humorous analogy of the three-way handshake: the client sends SYN=1, seq=x; the server replies SYN=1, ACK=1, ack=x+1, seq=y; the client returns ACK=1, ack=y+1.

TCP is full-duplex, so the two directions can close independently. A graceful close commonly exchanges `FIN` and `ACK`, hence the traditional term “four-way termination”. Delayed acknowledgment, simultaneous close, and reset can change the observed packets.

![[tcp-four-way-termination.png]]

> The diagram above is a humorous analogy of the four-way termination: each direction exchanges its own FIN/ACK pair and closes independently.

### 1.3.5 Network Layer: Forwarding and Routing

The network-layer data unit is commonly called a datagram. The network layer exists in end systems and routers and moves datagrams across networks:

- **Forwarding** is a data-plane action. It sends the current datagram from an input interface to the correct output interface using the routing table.
- **Routing** is a control-plane function. It computes and maintains paths to different destination networks.

Forwarding is the immediate decision made by one device for one packet; routing is the network-wide process of computing and maintaining paths. Therefore, “no matching route in the routing table” is primarily a routing problem, while “a matching route exists but the packet leaves through the wrong interface” points more toward forwarding or device state.

### 1.3.6 Application Processes, Sockets, and Addressing

Application-layer communication is performed by processes running on different end systems. A socket is the interface between an application process and the network; a process can be compared to a house and its socket to the door.

Locating a receiving process normally requires two pieces of information: the destination host's IP address and the port number identifying the process on that host. HTTP services commonly use `80` or `443`, while SMTP commonly uses `25`; applications may use different configured ports.

### 1.3.7 Link Layer, LANs, and Wireless Networks

The link layer transfers data between neighboring network nodes. Its data unit is a frame, and MAC addresses provide local-link addressing. Link-layer functions are commonly implemented by NICs, switches, and wireless access points, with some work performed in hardware and some by the operating system.

A LAN (Local-Area Network) connects devices within a home, institution, or other limited area. Common wireless network types include:

- **Bluetooth**: short-range communication, often for personal devices.
- **Wi-Fi**: short-range LAN access, usually through a wireless access point.
- **Cellular networks**: wider-area access for mobile devices through an operator network.

Wireless networks share a radio medium and are affected by distance, obstacles, interference, signal strength, and contention for the medium.

## 1.4 HTTP and HTTPS

### 1.4.1 HTTP Requests and Responses

HTTP is an application-layer request-response protocol used for Web pages, APIs, and service-to-service communication.

```http
GET /index.html HTTP/1.1
Host: www.example.com
Accept: text/html
User-Agent: example-client/1.0
Connection: keep-alive
```

A request usually contains a method, target path, version, headers, and an optional body. A response contains a status code, headers, and a body.

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Cache-Control: max-age=60
Content-Length: 13

Hello, client!
```

Common request headers include `Authorization`, `Content-Type`, `Accept`, and `Cookie`. Common response headers include `Content-Type`, `Cache-Control`, `Location`, `Set-Cookie`, and `Server`. The `Content-Type` header describes the body format, such as `application/json`.

### 1.4.2 Common Methods and Status Codes

| Method | Typical use | Idempotency |
| --- | --- | --- |
| `GET` | Retrieve a resource | Yes |
| `POST` | Create a resource or trigger processing | Usually no |
| `PUT` | Replace a resource | Yes |
| `PATCH` | Partially update a resource | Depends on the design |
| `DELETE` | Delete a resource | Usually yes by semantics |
| `HEAD` | Retrieve headers only | Yes |
| `OPTIONS` | Query supported operations | Yes |

Idempotency means repeated requests have the same intended effect as one request; it does not require identical responses.

| Range | Meaning | Examples |
| --- | --- | --- |
| `1xx` | Informational | `100 Continue` |
| `2xx` | Success | `200`, `201`, `204` |
| `3xx` | Redirect or cache | `301`, `302`, `304` |
| `4xx` | Request-side error | `400`, `401`, `403`, `404` |
| `5xx` | Server-side processing failure | `500`, `502`, `503` |

`401` usually means valid authentication is missing; `403` means access is refused. `502` and `503` often involve a proxy or upstream service, but logs and the request path are needed for diagnosis.

### 1.4.3 HTTP Versions and Caching

- **HTTP/1.1**: Text-based messages with persistent connections and chunked transfer.
- **HTTP/2**: Binary frames, multiplexing, and header compression; it usually still runs over TLS.
- **HTTP/3**: Built on QUIC/UDP to reduce TCP setup costs and head-of-line blocking effects.

Caching uses fields such as `Cache-Control`, `ETag`, and `Last-Modified`. A client can send `If-None-Match` or `If-Modified-Since`; if the resource has not changed, the server can return `304 Not Modified`.

### 1.4.4 HTTPS and TLS

HTTPS is HTTP carried over TLS. TLS provides confidentiality, server authentication, and integrity. Mutual TLS (mTLS) can also require and authenticate a client certificate.

The TLS handshake negotiates a protocol version and cipher suite, validates certificates, and establishes session keys. TLS 1.2 and TLS 1.3 differ, so the older “encrypt a pre-master secret with the server public key” description is not universal for modern TLS.

The usual default ports are HTTP `80` and HTTPS `443`. In DevOps, certificate expiry, hostname matching, certificate chains, protocol versions, and reverse-proxy configuration are common failure points.

## 1.5 Network Troubleshooting

### 1.5.1 Recommended Order

Narrow the problem in this order: local configuration, local gateway, DNS, target port, application response, then path analysis and packet capture. Record the command, target, time, and result at each step.

### 1.5.2 Connectivity and Path

```bash
ping -n 4 example.com       # Windows
ping -c 4 example.com       # Linux/macOS
tracert example.com         # Windows
traceroute example.com      # Linux/macOS
```

A failed `ping` does not prove that a service is unavailable because ICMP may be blocked. A `*` in a route trace may simply mean that a router does not return probes.

### 1.5.3 DNS Checks

```bash
nslookup example.com
nslookup -type=mx example.com
dig example.com
dig @8.8.8.8 example.com
```

Compare local and specified resolvers and check record type, TTL, authoritative responses, and returned addresses. A public resolver may be unavailable on a corporate or restricted network.

### 1.5.4 Ports and Connections

```bash
ss -tulnp                # Linux: include process information
netstat -ano             # Windows
netstat -an              # macOS/Linux
lsof -i :8080            # macOS/Linux
```

Windows PowerShell also provides:

```powershell
Get-NetTCPConnection -LocalPort 8080
Test-NetConnection example.com -Port 443
```

First confirm that the service listens on the expected address and port. Then check firewalls, security groups, network policies, and load balancers.

### 1.5.5 HTTP Tests

```bash
curl -i https://example.com
curl -v https://example.com
curl -L https://example.com
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"alice"}'
```

`curl -v` exposes DNS, TCP, TLS, request headers, and response headers. For HTTPS, also check certificates, SNI, proxies, and hostnames.

### 1.5.6 Narrowing by Symptom

| Symptom | Check first | Common directions |
| --- | --- | --- |
| Domain does not resolve | `nslookup`, `dig` | DNS settings, records, cache, split DNS |
| IP reachable but port closed | `Test-NetConnection`, `ss` | Listener, firewall, security group, network policy |
| Port reachable but `502` returned | `curl -v`, proxy logs | Reverse proxy, upstream service, timeout |
| HTTPS certificate error | `curl -v`, certificate checks | Hostname, chain, expiry, SNI |
| Intermittent timeouts | `traceroute`, metrics, capture | Loss, congestion, load balancing, connection pool |

### 1.5.7 Packet Capture

Wireshark is useful for graphical analysis; `tcpdump` is useful for collecting traffic on a server:

```bash
sudo tcpdump -i eth0 port 53
sudo tcpdump -i eth0 -w capture.pcap
```

The interface may not be named `eth0`; use `ip link` or `tcpdump -D` to confirm it. Captures may contain passwords, tokens, and personal data. Capture only on authorized networks and use filters to limit the scope.

[Back to networking basics](README.md) | [Next: Socket Programming](02-socket-programming.md)
