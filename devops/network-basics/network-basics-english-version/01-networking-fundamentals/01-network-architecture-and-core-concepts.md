# Network Architecture and Core Concepts

[Back to chapter index](README.md) | [Next: Network Addressing and Name Resolution](02-network-addressing-and-name-resolution.md)

## 1. Network Architecture

### 1.1 C/S: Client / Server

C/S architecture combines a local client with server-side services. The client may handle the interface, part of the business logic, and local resources, while the server provides centralized data and services.

Common examples include desktop software, games, and banking clients. It can provide a rich local experience, but client versions and operating-system compatibility must be maintained. Security does not automatically improve because data is local; it depends on authentication, authorization, encryption, and endpoint protection.

### 1.2 B/S: Browser / Server

B/S architecture exposes a Web application through a browser and usually requires no dedicated installation.

It simplifies release and updates and reduces cross-platform cost, but depends on the network, browser capabilities, and server performance. Modern Web applications can improve offline behavior with caching, WebAssembly, and Service Workers.

### 1.3 C/S vs B/S

| Dimension | C/S | B/S |
| --- | --- | --- |
| Access | Usually requires installation | Browser access |
| Updates | Client and server may both change | Mostly server-side |
| Performance | Can use local resources directly | Influenced by browser, network, and server |
| Cross-platform | Multiple clients may be needed | Browser compatibility matters |
| Typical use | Desktop software, games, specialist clients | Websites, admin panels, online services |

### 1.4 DevOps implications

- B/S systems emphasize HTTP latency, status codes, TLS, reverse proxies, and load balancing.
- C/S systems also require attention to client versions, connection stability, latency, packet loss, and update mechanisms.
- Both need authentication, access control, logs, metrics, and tracing.

## 2. Three Core Elements

A useful starting point for network analysis is:

1. **IP address**: which host or interface should receive the data?
2. **Port**: which process or service on that host?
3. **Protocol**: which format and rules govern the exchange?

These are often combined as `IP:port` and a protocol, such as `192.168.1.10:443/TCP`.

### 2.1 IP address

An IP address is used for network-layer addressing. Public addresses are routable on the Internet; private addresses can be reused in different local networks. “Unique device identifier” therefore needs an address scope.

IPv4 uses 32-bit addresses such as `192.168.1.34`; IPv6 uses 128-bit hexadecimal addresses such as `2001:db8::1`.

### 2.2 Port number

Ports distinguish network services on the same host and range from `0` to `65535`. Port ownership is protocol-specific, so TCP and UDP can use the same number independently.

| Range | Name | Typical use |
| --- | --- | --- |
| `0-1023` | Well-known | Common system services |
| `1024-49151` | Registered | Applications and vendors |
| `49152-65535` | Dynamic/private | Temporary client ports |

Common ports include `22/SSH`, `53/DNS`, `80/HTTP`, `443/HTTPS`, `3306/MySQL`, `5432/PostgreSQL`, `6379/Redis`, and `27017/MongoDB`.

### 2.3 Protocol

A protocol defines message format, exchange order, error handling, and state changes. HTTP, DNS, TCP, UDP, and IP operate at different layers and have different responsibilities.

## 3. Learning Path

Follow the chapter in this order: addressing, transport, application protocols, then troubleshooting.

- [Network Addressing and Name Resolution](02-network-addressing-and-name-resolution.md)
- [Network Layers and Transport Protocols](03-network-layers-and-transport-protocols.md)
- [HTTP and HTTPS](04-http-and-https.md)
- [Network Troubleshooting](05-network-troubleshooting.md)

[Back to chapter index](README.md) | [Next: Network Addressing and Name Resolution](02-network-addressing-and-name-resolution.md)
