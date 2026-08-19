# HTTP 与 HTTPS

[上一篇：网络分层与传输协议](03-网络分层与传输协议.md) | [返回章节目录](README.md) | [下一篇：网络故障排查](05-网络故障排查.md)

## 1. HTTP 请求与响应

HTTP 是应用层的请求-响应协议，常用于网页、API 和服务间通信。

```http
GET /index.html HTTP/1.1
Host: www.example.com
Accept: text/html
User-Agent: example-client/1.0
Connection: keep-alive
```

请求通常包含方法、目标路径、版本、请求头和可选请求体。响应包含状态码、响应头和响应体。

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Cache-Control: max-age=60
Content-Length: 13

Hello, client!
```

常见请求头包括 `Authorization`、`Content-Type`、`Accept` 和 `Cookie`；常见响应头包括 `Content-Type`、`Cache-Control`、`Location`、`Set-Cookie` 和 `Server`。请求体和响应体的格式由 `Content-Type` 说明，例如 `application/json`。

## 2. 常用方法

| 方法 | 常见用途 | 幂等性 |
| --- | --- | --- |
| `GET` | 获取资源 | 是 |
| `POST` | 创建资源或触发处理 | 通常否 |
| `PUT` | 完整替换资源 | 是 |
| `PATCH` | 部分修改资源 | 取决于具体设计 |
| `DELETE` | 删除资源 | 通常按语义视为是 |
| `HEAD` | 只获取响应头 | 是 |
| `OPTIONS` | 查询支持的操作 | 是 |

幂等表示重复执行请求的最终预期效果与执行一次相同，不代表每次响应完全相同。

## 3. HTTP 版本与缓存

- **HTTP/1.1**：文本格式，支持持久连接和分块传输。
- **HTTP/2**：二进制帧、多路复用和头部压缩，通常仍运行在 TLS 上。
- **HTTP/3**：基于 QUIC/UDP，减少 TCP 建连和队头阻塞带来的影响。

缓存由 `Cache-Control`、`ETag`、`Last-Modified` 等字段控制。客户端可以携带 `If-None-Match` 或 `If-Modified-Since`，服务器在资源未变化时返回 `304 Not Modified`。

## 4. 状态码

| 范围 | 含义 | 示例 |
| --- | --- | --- |
| `1xx` | 信息 | `100 Continue` |
| `2xx` | 成功 | `200`、`201`、`204` |
| `3xx` | 重定向或缓存 | `301`、`302`、`304` |
| `4xx` | 请求方错误 | `400`、`401`、`403`、`404` |
| `5xx` | 服务端处理失败 | `500`、`502`、`503` |

`401` 通常表示缺少有效认证，`403` 表示服务器拒绝访问；`502` 和 `503` 常见于代理或上游服务异常，但仍需结合日志和链路判断。

## 5. HTTPS 与 TLS

HTTPS 是运行在 TLS 之上的 HTTP。TLS 提供机密性、服务器身份认证和数据完整性；双向 TLS（mTLS）还可以要求客户端提供证书并完成客户端认证。

TLS 握手会协商协议版本和密码套件、验证证书、建立会话密钥。TLS 1.2 和 TLS 1.3 的握手细节不同，学习时不应把“客户端用服务器公钥加密预主密钥”当作所有现代 TLS 的通用流程。

默认端口通常是 HTTP `80`、HTTPS `443`。在 DevOps 中，证书有效期、主机名匹配、证书链、协议版本和反向代理配置都是常见排查点。

## 6. 实操题

1. 使用 `curl -i https://example.com` 区分响应状态行、响应头和响应体。
2. 使用 `curl -v` 观察 DNS、TCP 和 TLS 建连阶段，记录证书主机名和有效期。
3. 为一个 API 设计 `Content-Type`、缓存策略和错误状态码。

[上一篇：网络分层与传输协议](03-网络分层与传输协议.md) | [返回章节目录](README.md) | [下一篇：网络故障排查](05-网络故障排查.md)
