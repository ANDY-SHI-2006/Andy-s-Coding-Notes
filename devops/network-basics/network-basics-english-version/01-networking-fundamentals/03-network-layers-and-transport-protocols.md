# Network Layers and Transport Protocols

[Previous: Network Addressing and Name Resolution](02-network-addressing-and-name-resolution.md) | [Back to chapter index](README.md) | [Next: HTTP and HTTPS](04-http-and-https.md)

## 1. OSI and TCP/IP Models

OSI is mainly a teaching and analysis model with seven layers. TCP/IP is the more common engineering model for the Internet. Names vary slightly between textbooks; focus on responsibilities and encapsulation.

| OSI | Common TCP/IP mapping | Examples |
| --- | --- | --- |
| Application, presentation, session | Application | HTTP, DNS, SMTP |
| Transport | Transport | TCP, UDP |
| Network | Internet | IP, ICMP |
| Data link, physical | Network access | Ethernet, Wi-Fi |

Data is encapsulated from the upper layers downward when sent and decapsulated upward when received. ARP is often discussed near the network-access layer because it crosses the network/link-layer boundary.

## 2. TCP and UDP

| Feature | TCP | UDP |
| --- | --- | --- |
| Connection | Connection-oriented | Connectionless |
| Reliability | Acknowledgment, retransmission, ordered delivery | No delivery, order, or retransmission guarantee |
| Overhead | Higher | Lower |
| Typical use | Web, file transfer, databases | DNS, real-time media, some games and IoT |

UDP does not require applications to use only small data; applications still need to consider MTU, fragmentation, and loss. TCP also does not preserve application message boundaries, so applications must define framing.

## 3. TCP Connection Setup and Close

### 3.1 Three-way handshake

1. The client sends `SYN` with an initial sequence number.
2. The server returns `SYN + ACK`.
3. The client returns `ACK`, and the connection can carry data.

### 3.2 Connection close

TCP is full-duplex, so the two directions can close independently. A graceful close commonly exchanges `FIN` and `ACK`, hence the traditional term “four-way termination”. Delayed acknowledgment, simultaneous close, and reset can change the observed packets.

[Previous: Network Addressing and Name Resolution](02-network-addressing-and-name-resolution.md) | [Back to chapter index](README.md) | [Next: HTTP and HTTPS](04-http-and-https.md)
