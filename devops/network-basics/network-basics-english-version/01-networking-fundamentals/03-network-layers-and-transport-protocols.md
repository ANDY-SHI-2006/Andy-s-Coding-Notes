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

| Layer | Common devices or components | Troubleshooting clues |
| --- | --- | --- |
| Application | Web server, reverse proxy | Status codes, request logs, application latency |
| Transport | Load balancer, firewall | Listening ports, handshakes, retransmissions |
| Internet | Router, cloud route table | Addresses, routes, loss, TTL |
| Network access | Switch, NIC, wireless AP | Link state, VLAN, MAC |

## 2. TCP and UDP

| Feature | TCP | UDP |
| --- | --- | --- |
| Connection | Connection-oriented | Connectionless |
| Reliability | Acknowledgment, retransmission, ordered delivery | No delivery, order, or retransmission guarantee |
| Overhead | Higher | Lower |
| Typical use | Web, file transfer, databases | DNS, real-time media, some games and IoT |

UDP does not require applications to use only small data; applications still need to consider MTU, fragmentation, and loss. TCP also does not preserve application message boundaries, so applications must define framing.

TCP also provides flow control and congestion control. The receive window prevents a sender from exceeding receiver capacity, while the congestion window adapts the sending rate to network conditions. These mechanisms affect throughput but do not remove the need for application timeouts and retry policies.

## 3. TCP Data and Exceptional States

TCP presents application data as a continuous byte stream and does not preserve `send()` or `write()` boundaries. Applications commonly use length prefixes, delimiters, or fixed-size messages to define framing.

`RST` immediately resets a connection. Common causes include an unlistened port, an actively rejected connection, or a stateful middlebox losing connection state. After a graceful close, the active closer may enter `TIME_WAIT` so delayed old segments cannot affect a later connection.

## 4. TCP Connection Setup and Close

### 4.1 Three-way handshake

1. The client sends `SYN` with an initial sequence number.
2. The server returns `SYN + ACK`.
3. The client returns `ACK`, and the connection can carry data.

### 4.2 Connection close

TCP is full-duplex, so the two directions can close independently. A graceful close commonly exchanges `FIN` and `ACK`, hence the traditional term “four-way termination”. Delayed acknowledgment, simultaneous close, and reset can change the observed packets.

## 5. Practice

1. Capture a TCP handshake and label `SYN`, `ACK`, and sequence numbers.
2. Connect to a port with no listening service and compare the failure observed with `curl` or `Test-NetConnection`.
3. Design a length-prefixed message format and explain how it handles TCP coalescing and fragmentation.

[Previous: Network Addressing and Name Resolution](02-network-addressing-and-name-resolution.md) | [Back to chapter index](README.md) | [Next: HTTP and HTTPS](04-http-and-https.md)
