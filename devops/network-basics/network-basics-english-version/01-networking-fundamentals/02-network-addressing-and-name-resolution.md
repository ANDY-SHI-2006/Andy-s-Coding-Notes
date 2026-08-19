# Network Addressing and Name Resolution

[Previous: Network Architecture and Core Concepts](01-network-architecture-and-core-concepts.md) | [Back to chapter index](README.md) | [Next: Network Layers and Transport Protocols](03-network-layers-and-transport-protocols.md)

## 1. IP Addresses

### 1.1 IPv4 and IPv6

IPv4 uses 32-bit addresses in dotted-decimal notation, such as `192.168.1.34`; each octet ranges from `0` to `255`. IPv6 uses 128-bit hexadecimal addresses, such as `2001:db8::1`. One run of zero groups may be compressed with `::`.

### 1.2 Address types

| Type | Purpose | Examples |
| --- | --- | --- |
| Public IP | Routable on the Internet | Assigned by an ISP or cloud provider |
| Private IP | Local network or VPC use | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` |
| Loopback | Refers to the local host | `127.0.0.1`, `::1` |

IPv6, CIDR, NAT, and address reclamation all help address IPv4 scarcity.

## 2. MAC Addresses and ARP

A MAC address is usually 48 bits and identifies a network interface on a local link. Switches forward frames using MAC addresses.

ARP maps an IPv4 address to a MAC address on a local network. A host broadcasts a request, the target replies, and the result is cached. Use `arp -a` on Windows or `ip neigh` on Linux to inspect the cache.

IPv6 does not use ARP. It uses Neighbor Discovery Protocol (NDP), which is based on ICMPv6 and also supports neighbor reachability detection and router discovery.

## 3. Subnets, CIDR, and Gateways

A subnet mask divides an IPv4 address into network and host portions. `255.255.255.0` is equivalent to `/24`.

| CIDR | Mask | Usable hosts in a traditional IPv4 subnet |
| --- | --- | ---: |
| `/8` | `255.0.0.0` | 16,777,214 |
| `/16` | `255.255.0.0` | 65,534 |
| `/24` | `255.255.255.0` | 254 |

For a traditional IPv4 subnet, usable hosts are usually $2^{32-p}-2$, where $p$ is the CIDR prefix length; point-to-point links, cloud networks, and IPv6 may use different rules.

A default gateway forwards traffic outside the local subnet. A host first determines whether the destination is local; otherwise it sends the packet to the gateway.

Useful commands:

```bash
ip route                 # Linux
route print              # Windows
netstat -rn              # macOS
```

During troubleshooting, check whether a matching route exists, whether the next hop is correct, and whether the interface is enabled.

## 4. DNS

DNS maps domain names to IP addresses and can provide other information such as mail servers.

| Record | Purpose |
| --- | --- |
| `A` | Name to IPv4 |
| `AAAA` | Name to IPv6 |
| `CNAME` | Alias to another name |
| `MX` | Mail server |
| `NS` | Authoritative name server |
| `TXT` | Text and validation data |

Resolution commonly involves browser or operating-system caches, a recursive resolver, and authoritative name servers. On a cache miss, the recursive resolver may query root, top-level-domain, and authoritative servers in sequence. Caching and DNS over HTTPS/TLS can change the visible sequence.

## 5. NAT

NAT changes IP addresses or ports at an address boundary and commonly lets private networks access the Internet.

- **SNAT** changes the source address for outbound access.
- **DNAT** changes the destination address, often for port forwarding.
- **PAT/NAT overload** lets multiple private addresses share one public address through different ports.

NAT is not a firewall replacement. Cloud VPCs, port forwarding, and some container networks use translation or proxy mechanisms, but the exact behavior depends on the platform.

## 6. Practice

1. Inspect the local addresses and route table and identify the default route's next hop.
2. Use `arp -a` or `ip neigh` to find the link-layer address of the default gateway.
3. Query `A`, `AAAA`, and `MX` records with `nslookup` or `dig`, and record their TTL values.

[Previous: Network Architecture and Core Concepts](01-network-architecture-and-core-concepts.md) | [Back to chapter index](README.md) | [Next: Network Layers and Transport Protocols](03-network-layers-and-transport-protocols.md)
