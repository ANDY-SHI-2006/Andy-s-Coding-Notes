# Network Troubleshooting

[Previous: HTTP and HTTPS](04-http-and-https.md) | [Back to chapter index](README.md)

## 1. Recommended Order

Narrow the problem in this order: local configuration, local gateway, DNS, target port, application response, then path analysis and packet capture. Record the command, target, time, and result at each step.

## 2. Connectivity and Path

```bash
ping -n 4 example.com       # Windows
ping -c 4 example.com       # Linux/macOS
tracert example.com         # Windows
traceroute example.com      # Linux/macOS
```

A failed `ping` does not prove that a service is unavailable because ICMP may be blocked. A `*` in a route trace may simply mean that a router does not return probes.

## 3. DNS Checks

```bash
nslookup example.com
nslookup -type=mx example.com
dig example.com
dig @8.8.8.8 example.com
```

Compare local and specified resolvers and check record type, TTL, authoritative responses, and returned addresses.

## 4. Ports and Connections

```bash
ss -tulnp                # Linux: include process information
netstat -ano             # Windows
netstat -an              # Common option on macOS/Linux
lsof -i :8080            # macOS/Linux
```

Windows PowerShell also provides:

```powershell
Get-NetTCPConnection -LocalPort 8080
Test-NetConnection example.com -Port 443
```

First confirm that the service listens on the expected address and port. Then check firewalls, security groups, network policies, and load balancers.

## 5. HTTP Tests

```bash
curl -I https://example.com
curl -v https://example.com
curl -L https://example.com
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"alice"}'
```

`curl -v` exposes DNS, TCP, TLS, request headers, and response headers. For HTTPS, also check certificates, SNI, proxies, and hostnames.

## 6. Narrowing by Symptom

| Symptom | Check first | Common directions |
| --- | --- | --- |
| Domain does not resolve | `nslookup`, `dig` | DNS settings, records, cache, split DNS |
| IP reachable but port closed | `Test-NetConnection`, `ss` | Listener, firewall, security group, network policy |
| Port reachable but `502` returned | `curl -v`, proxy logs | Reverse proxy, upstream service, timeout |
| HTTPS certificate error | `curl -v`, certificate checks | Hostname, chain, expiry, SNI |
| Intermittent timeouts | `traceroute`, metrics, capture | Loss, congestion, load balancing, connection pool |

## 6. Packet Capture

Wireshark is useful for graphical analysis; `tcpdump` is useful for collecting traffic on a server:

```bash
sudo tcpdump -i eth0 port 53
sudo tcpdump -i eth0 -w capture.pcap
```

The interface may not be named `eth0`; use `ip link` or `tcpdump -D` to confirm it. Captures may contain passwords, tokens, and personal data. Capture only on authorized networks and use filters to limit the scope.

## 7. Practice

1. Simulate a DNS configuration error and record the investigation from name resolution to port testing.
2. Start a local HTTP service and compare “no listener” with “application returns 500”.
3. Save only the necessary output from an HTTPS request or capture, and remove tokens and personal data.

[Previous: HTTP and HTTPS](04-http-and-https.md) | [Back to chapter index](README.md)
