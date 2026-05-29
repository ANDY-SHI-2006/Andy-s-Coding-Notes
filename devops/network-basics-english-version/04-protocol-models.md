# 4. Protocol Models

A set of rules that define how data is transmitted over a network.

| Function | Description |
|----------|-------------|
| **Message format** | Defines how data is structured |
| **Transmission rules** | Determines how messages are sent and received |
| **Error handling** | Specifies how errors are detected and corrected |

## 4.1 Network Communication Protocol Models

| Model | Layers | Description |
|-------|--------|-------------|
| **OSI Model** | 7 layers | Theoretical model (Physical, Data Link, Network, Transport, Session, Presentation, Application) |
| **TCP/IP Model** | 4 layers | Practical implementation standard (Network Interface, Internet, Transport, Application) |

The TCP/IP model is the de facto standard for internet communication.

## 4.2 OSI Model (7 Layers)

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

### 4.2.1 Data Flow

- **Sender**: Data starts at Application layer, processed downward through each layer, finally transmitted as binary signals at Physical layer.
- **Receiver**: Binary signals processed at Physical layer, moves upward through each layer, finally reconstructed to usable data at Application layer.

### 4.2.2 Pros

Establishes unified communication standards, reduces development difficulty through clear layer separation.

### 4.2.3 Cons

Overly idealistic, structurally too complex for practical engineering implementation.

## 4.3 OSI vs TCP/IP Layer Mapping

| OSI Layer | OSI Name | TCP/IP Layer | TCP/IP Name | Merged? |
|-----------|----------|--------------|-------------|---------|
| 7 | Application | 4 | Application | ✅ Merged |
| 6 | Presentation | 4 | Application | ✅ Merged |
| 5 | Session | 4 | Application | ✅ Merged |
| 4 | Transport | 3 | Transport | ❌ Same |
| 3 | Network | 2 | Internet | ❌ Same (renamed) |
| 2 | Data Link | 1 | Network Interface | ✅ Merged |
| 1 | Physical | 1 | Network Interface | ✅ Merged |

## 4.4 TCP/IP Model (4 Layers)

Practical implementation standard used in actual networking.

| Layer | Name | Main Protocols | Function |
|-------|------|----------------|----------|
| 4 | **Application** | HTTP, FTP, SMTP, DNS | Application-specific protocols |
| 3 | **Transport** | TCP, UDP | Process-to-process communication |
| 2 | **Internet** | IP, ICMP, ARP | End-to-end data routing |
| 1 | **Network Interface** | Ethernet, Wi-Fi | Binary signal transmission over physical medium |

### 4.4.1 Key Protocols

- **Application Layer**: HTTP (web browsing), FTP (file transfer), SMTP (email), DNS (domain name resolution)
- **Transport Layer**: TCP (reliable, slower), UDP (unreliable, fast)
- **Internet Layer**: IP (addressing), ICMP (error reporting), ARP (address resolution)
