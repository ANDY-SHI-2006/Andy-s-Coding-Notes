# 2. IP Address

## 2.1 IP Address Classification

| Version | Description | Address Length | Format |
|---------|-------------|----------------|--------|
| **IPv4** | Internet Protocol version 4 | 32-bit binary | Dot-decimal notation (e.g., 192.168.1.34) |
| **IPv6** | Internet Protocol version 6 | 128-bit binary | 8 groups of hexadecimal numbers separated by colons |

## 2.2 IPv4 Address Structure

- **Binary representation**: 32 bits divided into 4 octets (8 bits each)
- **Display format**: Dot-decimal notation (e.g., 192.168.1.34)
- **Value range per octet**: 0 - 255
- **Total address space**: Approximately 4.2 billion (256^4) unique addresses

## 2.3 IPv6 Address Structure

- **Address format**: 8 groups of 4 hexadecimal digits separated by colons
- **Example**: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- **Zero compression**: Consecutive groups of zeros can be replaced with `::`
  - Example: `2001:0db8:0000:0000:0000:0000:0000:0001` → `2001:0db8::0001`
  - **Rule**: Can only be used once per address
  - **Reason**: Using `::` twice would make it impossible to determine how many zero groups each represents (8 total groups minus visible groups = groups represented by `::`)

## 2.4 IP Address Types

| Type | Description | Address Range | Usage |
|------|-------------|---------------|-------|
| **Public IP** | Globally unique address accessible from the internet | Various | Internet communication |
| **Private IP** | Address used within local networks (LAN) | 192.168.x.x, 10.x.x.x, 172.16.x.x - 172.31.x.x | Internal network communication |
| **Loopback** | Local address referring to the current device | 127.0.0.1 (IPv4), ::1 (IPv6) | Local testing and development |

## 2.5 IPv4 Address Exhaustion

IPv4 provides approximately 4.2 billion unique addresses (2^32). With the explosive growth of internet-connected devices, IPv4 addresses were fully allocated by **November 26, 2019**.

### 2.5.1 Solutions

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

## 2.6 Common IP-Related Commands

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
