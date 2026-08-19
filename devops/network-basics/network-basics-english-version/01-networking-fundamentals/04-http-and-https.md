# HTTP and HTTPS

[Previous: Network Layers and Transport Protocols](03-network-layers-and-transport-protocols.md) | [Back to chapter index](README.md) | [Next: Network Troubleshooting](05-network-troubleshooting.md)

## 1. HTTP Requests and Responses

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

## 2. Common Methods

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

## 3. HTTP Versions and Caching

- **HTTP/1.1**: Text-based messages with persistent connections and chunked transfer.
- **HTTP/2**: Binary frames, multiplexing, and header compression; it usually still runs over TLS.
- **HTTP/3**: Built on QUIC/UDP to reduce TCP setup costs and head-of-line blocking effects.

Caching uses fields such as `Cache-Control`, `ETag`, and `Last-Modified`. A client can send `If-None-Match` or `If-Modified-Since`; if the resource has not changed, the server can return `304 Not Modified`.

## 4. Status Codes

| Range | Meaning | Examples |
| --- | --- | --- |
| `1xx` | Informational | `100 Continue` |
| `2xx` | Success | `200`, `201`, `204` |
| `3xx` | Redirect or cache | `301`, `302`, `304` |
| `4xx` | Request-side error | `400`, `401`, `403`, `404` |
| `5xx` | Server-side processing failure | `500`, `502`, `503` |

`401` usually means valid authentication is missing; `403` means access is refused. `502` and `503` often involve a proxy or upstream service, but logs and the request path are needed for diagnosis.

## 5. HTTPS and TLS

HTTPS is HTTP carried over TLS. TLS provides confidentiality, server authentication, and integrity. Mutual TLS (mTLS) can also require and authenticate a client certificate.

The TLS handshake negotiates a protocol version and cipher suite, validates certificates, and establishes session keys. TLS 1.2 and TLS 1.3 differ, so the older “encrypt a pre-master secret with the server public key” description is not universal for modern TLS.

The usual default ports are HTTP `80` and HTTPS `443`. In DevOps, certificate expiry, hostname matching, certificate chains, protocol versions, and reverse-proxy configuration are common failure points.

## 6. Practice

1. Use `curl -i https://example.com` to distinguish the status line, headers, and body.
2. Use `curl -v` to observe DNS, TCP, and TLS setup, and record the certificate hostname and expiry.
3. Design an API's `Content-Type`, caching policy, and error status codes.

[Previous: Network Layers and Transport Protocols](03-network-layers-and-transport-protocols.md) | [Back to chapter index](README.md) | [Next: Network Troubleshooting](05-network-troubleshooting.md)
