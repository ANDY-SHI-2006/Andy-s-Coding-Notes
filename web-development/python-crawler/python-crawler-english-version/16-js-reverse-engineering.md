[<- Previous: elasticsearch](15-elasticsearch.md) | [Next: font anti-crawler and obfuscation ->](17-font-anti-crawler-and-ob.md)

# 16 JS Reverse Engineering and Debugging Bypass

Many websites no longer return plaintext data. Instead they encrypt request parameters and response bodies, then encrypt and decrypt them in the browser with JavaScript. "Reverse engineering" means reconstructing that encryption logic — through packet capture, breakpoints, and reading obfuscated JS — without seeing the original source, then re-implementing it in Python to bypass the protection. This chapter covers the general workflow, the common algorithms (MD5 / base64 / AES / SHA-256 / RC4), sign signatures, bypassing infinite `debugger` traps, and how to run JS reliably from Python.

## 16.1 Concept and Locating Approach

### 16.1.1 What Is JS Reverse Engineering

> **Key idea:** Anti anti-crawler = understand the website's encryption JS, then re-implement the algorithm in Python to bypass it.

Requests in a browser are readable, but what the server returns to a crawler is usually encrypted by JS. The goal of reverse engineering is not to crack the encryption itself, but to **find the JS that the browser runs automatically, understand it, and make Python execute the same logic**.

### 16.1.2 Locating Approach

1. Open the Network panel of DevTools (F12) and refresh the page.
2. Find the XHR / Fetch request that actually returns the data (not the page itself).
3. Inspect the request parameters and response body: which are plaintext (page number, keyword) and which are gibberish.
4. For a gibberish parameter, search its key name globally in the Sources panel to locate the JS that produces it.
5. Set a breakpoint at the suspicious spot, refresh, and trace the variables step by step to reconstruct the algorithm.

## 16.2 Recognizing Encrypted Parameters

To decide whether a parameter needs reverse engineering, first check whether it "looks encrypted":

| Feature | Explanation |
|---|---|
| Plaintext parameter | `page`, `kw`, `cid` — values are readable and stable |
| Encrypted parameter | A long gibberish string, or one that changes on every request (mixed with timestamps or random numbers) |
| Common key names | `sign`, `token`, `_signature`, `encrypt`, `encode` |

> **Key idea:** The key name is the clue. `sign` / `_signature` almost always means a signature; `encrypt` / `encode` usually means encryption; `ts` / `timestamp` / `nonce` are timestamps and random numbers.

The part that changes (timestamp, random number) is the "dynamic input" of the encryption — exactly the variable to watch closely while debugging.

## 16.3 Three Approaches to Reverse Engineering

Once you have an encrypted parameter, there are three ways to land it:

| Approach | How | Pros / cons |
|---|---|---|
| ① Re-implement in Python | Rewrite the algorithm in Python with `hashlib`, `pycryptodome` | No Node needed, cross-platform, but slow and error-prone for complex algorithms |
| ② Extract the JS | "Pull out" the encryption function from the site's JS and call it with `execjs` | Fastest and most stable, but depends on a Node runtime |
| ③ Third-party module | Use an existing reverse-engineering library | Convenient, but may break or be uncontrollable |

> **Key idea:** The common workflow is — **locate the encrypted parameter → search the JS by key name → find the algorithm with breakpoints → re-implement or extract**. Approaches ① and ② differ only in the final "landing" step.

## 16.4 Node.js Environment and crypto-js

Approach ② (extracting JS) requires running JS locally, which depends on Node.js. The most common front-end crypto library is `crypto-js`:

```bash
npm install -g crypto-js
```

Then write a `pwd.js`:

```js
// pwd.js: MD5 hashing (to be called from Python via execjs)
var crypto = require('crypto-js');
function f1(mima) {
  return crypto.MD5(mima).toString();
}
```

> **Note:** `require('crypto-js')` must run from a location where the package can be resolved. A global install (`-g`) lets you test with `node pwd.js` from any directory; alternatively `npm install crypto-js` installs it locally.

## 16.5 Running JS from Python: PyExecJS

`PyExecJS` is a bridge library that lets Python call JS. Under the hood it launches a local JS runtime (Node.js is preferred by default).

```bash
pip install PyExecJS
```

### 16.5.1 Basic Usage

```python
import execjs

# Inline JS
ctx = execjs.compile("function f(){return 111}")
print(ctx.call('f'))           # 111

# Read a .js file and call a function from it
js = open('pwd.js', encoding='utf-8').read()
res = execjs.compile(js).call('f1', '123456')
print(res)                     # e10adc3949ba59abbe56e057f20f883e
```

`compile(js)` returns a context, and `call(func_name, args...)` invokes a JS function and returns its result.

> **Note:** `PyExecJS` is no longer maintained and may fail to find a runtime across environments (especially newer Node versions). See 16.14 for alternatives.

### 16.5.2 Pointing to a Local Node Runtime

When the default runtime is missing or mismatched, you can manually point to the Node executable:

```python
import execjs
from execjs import _runner_sources as runner_sources

rt = execjs.ExternalRuntime(
    name="Node.js (local)", command='', encoding='UTF-8',
    runner_source=runner_sources.Node)
rt._binary_cache = [r'C:\Program Files\nodejs\node.exe']   # actual path to node.exe
rt._available = True
execjs.register('local_node', rt)
nodejs = execjs.get('local_node')

# Then use nodejs.eval(js) or nodejs.compile(js).call('f', ...)
print(nodejs.eval("1 + 1"))   # 2
```

> **Correction:** This code relies on the private `_binary_cache` / `_available` attributes of `ExternalRuntime`. It is an undocumented hack and breaks easily across versions. A more robust approach is to call `node` via `subprocess`, or switch to a maintained library such as `py_mini_racer` / `js2py`.

## 16.6 Common Algorithms at a Glance

The algorithms you meet most often are MD5, base64, AES, and less frequently SHA-256 and RC4. Knowing the JS and Python equivalents lets you recognize at a glance what an extracted JS function is doing.

| Algorithm | JS (crypto-js) | Python |
|---|---|---|
| MD5 | `crypto.MD5(s).toString()` | `hashlib.md5(s.encode()).hexdigest()` |
| SHA-256 | `crypto.SHA256(s).toString()` | `hashlib.sha256(s.encode()).hexdigest()` |
| base64 | `crypto.enc.Base64.stringify(...)` (or browser `btoa`) | `base64.b64encode(...)` |
| AES | `crypto.AES.encrypt` / `crypto.AES.decrypt` | `pycryptodome`'s `AES` |

## 16.7 MD5: JS vs Python

MD5 is an irreversible digest, commonly used for passwords and signatures.

```js
// JS side (crypto-js)
var crypto = require('crypto-js');
function f1(mima) {
  return crypto.MD5(mima).toString();
}
```

```python
# Python side
import hashlib

s = hashlib.md5()
s.update('123456'.encode())
print(s.hexdigest())          # e10adc3949ba59abbe56e057f20f883e
```

> **Correction:** The source materials write `var crypot = require('crypto-js')` in a comment, misspelling `crypto` as `crypot`. The correct spelling is `crypto`.

WeChat Official Account login is a classic application: MD5 the password, POST it to the login endpoint, and generate `fingerprint = md5(UA + 8-digit random integer)`.

```python
import hashlib, random

def get_fingerprint(ua):
    rand = str(random.randint(0, 99999999)).zfill(8)
    return hashlib.md5((ua + rand).encode()).hexdigest()
```

> **Correction:** The source materials hard-code `fingerprint` as `'6f30a0770ecc9964c3b9927f773cc45a'` and never call the `get_fingerprint()` function defined in the same file. The correct approach is to generate `md5(UA + random 8 digits)` on every call.

## 16.8 base64 and btoa

base64 is a reversible encoding, often used to give a parameter a shell that is not instantly readable. Browsers use `btoa()`; Python uses the `base64` module.

> **Correction:** `btoa` is a **browser API** and does not exist in Node (Node can use `Buffer.from(s).toString('base64')` or a manual implementation). This is exactly why the source `demo.py` rewrote that logic in Python.

Virustotal's `x-vt-anti-abuse-header` is `btoa(random - fixed string - timestamp)`:

```python
import base64, random, time

rand = (1 + random.random() % 50000) * 10**10
raw = f"{rand}-<fixed string>-{int(time.time())}"
b64 = base64.b64encode(raw.encode()).decode('utf-8')
headers = {'x-vt-anti-abuse-header': b64}
```

> **Correction:** The source `rand = (1 + random.random() % 50000) + 10**10` is not equivalent to the JS `(1 + Math.random() % 5e4) * 1e10` (it drops the multiplication and gets precedence wrong). It should be `(1 + random.random() % 50000) * 10**10`.
>
> **Correction:** `base64.b64encode(...)` returns `bytes`; putting it directly into headers would produce a `b'...'` string. Call `.decode('utf-8')` first.

## 16.9 AES Encryption and Decryption (crypto-js)

AES is a block symmetric cipher that needs a `key`, an `iv`, a mode (usually CBC), and padding (usually Pkcs7). In reverse engineering you meet both directions: encrypting request parameters and decrypting response ciphertext.

### 16.9.1 Decrypting the Response Ciphertext

The server encrypts the response, and the front-end JS decrypts it before rendering. Extract the decryption function:

```js
// get_response.js: decrypt the response ciphertext and parse it as JSON
var crypto = require('crypto-js');

function b(t) {
  var e = crypto.enc.Utf8.parse('<32-byte key>');   // key (redacted)
    , n = crypto.enc.Utf8.parse('<16-byte IV>');    // iv (redacted)
    , a = crypto.AES.decrypt(t, e, {
        iv: n, mode: crypto.mode.CBC, padding: crypto.pad.Pkcs7
      });
  return a.toString(crypto.enc.Utf8);
}

function get_response(mi) {
  return JSON.parse(b(mi));
}
```

> **Key idea:** `enc.Utf8.parse` converts a string into a WordArray, `enc.Base64.stringify` / `enc.Utf8.parse` handle encoding, and `toString(crypto.enc.Utf8)` turns the decrypted result back into readable text. The key/iv length determines AES-128 / 192 / 256.

### 16.9.2 Encrypting a Request Parameter with AES

The reverse operation: AES-encrypt a timestamp to use as a request header, which the server then decrypts to validate.

```js
function getResCode() {
  var c = crypto.AES.encrypt(
    crypto.enc.Utf8.parse(String(Math.floor(new Date().getTime() / 1000))),
    crypto.enc.Utf8.parse('1234567887654321'),        // example key (16 bytes)
    { iv: crypto.enc.Utf8.parse('1234567887654321'),  // example iv
      mode: crypto.mode.CBC, padding: crypto.pad.Pkcs7 });
  return crypto.enc.Base64.stringify(c.ciphertext);   // Accept-EncKey
}
```

> **Key idea:** Take `c.ciphertext` (stripping the WordArray metadata) and base64-encode it to form the `Accept-EncKey` header.

## 16.10 SHA-256 and RC4 Skeleton

- **SHA-256** is a digest like MD5 but stronger: `hashlib.sha256(b'...').hexdigest()`.
- **RC4** is a stream symmetric cipher built on a 256-byte S-box permutation (KSA initialization + PRGA encryption). In ob obfuscation, RC4 is commonly used to decrypt the string array (see Chapter 17).

```python
def rc4(key: bytes, data: bytes) -> bytes:
    S = list(range(256))
    j = 0
    for i in range(256):                 # KSA: scramble S with the key
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = []
    for ch in data:                      # PRGA: XOR byte by byte
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(ch ^ S[(S[i] + S[j]) % 256])
    return bytes(out)
```

## 16.11 Reverse Engineering a Sign Signature

Many APIs require you to sort parameters, concatenate them, add a salt, and MD5 the result, sending it as a `sign` (or `portal-sign`) header to prevent parameter tampering. A typical algorithm:

```js
function l(t, e) {                       // compare keys case-insensitively
  var a = t.toString().toUpperCase(), b = e.toString().toUpperCase();
  return a > b ? 1 : a == b ? 0 : -1;
}
function u(t) {                          // sort keys and join key=value
  var ks = Object.keys(t).sort(l), n = "";
  for (var i = 0; i < ks.length; i++) n += ks[i] + t[ks[i]];
  return n;
}
function d(t) {                          // sign = MD5(salt + joined), lowercase
  var n = "<fixed salt>" + u(t);
  return crypto.MD5(n).toString().toLocaleLowerCase();
}
```

Re-implement in Python (use `key=str.upper` to sort case-insensitively):

```python
import hashlib

def sign(params: dict) -> str:
    salt = "<fixed salt>"
    joined = ''.join(k + str(params[k])
                     for k in sorted(params, key=str.upper))
    return hashlib.md5((salt + joined).encode()).hexdigest()
```

> **Key idea:** The signature has three steps — **sort, concatenate, then MD5 with a salt**. The salt is a fixed string (the source materials use a real site's salt, redacted here as `<fixed salt>`). The sort order must match the front end exactly, or the signature will not verify.

## 16.12 Full Example: Encrypted Request and Ciphertext Decryption

String the pieces together: compute `sign` and `Accept-EncKey`, send the request, then decrypt the `Data` ciphertext in the response.

```python
import execjs, requests

# Extracted algorithms: encrypt the header + decrypt the response
js = open('get_response.js', encoding='utf-8').read()
ctx = execjs.compile(js)

params = {'page': 1, 'keyword': '<keyword>'}
headers = {
    'User-Agent': '<UA>',
    'portal-sign': sign(params),                 # sign re-implemented in Python
    'Accept-EncKey': ctx.call('getResCode'),     # encrypted header from JS
}

resp = requests.get('<api url>', params=params, headers=headers).json()
plain = ctx.call('get_response', resp['Data'])   # decrypt the response ciphertext
print(plain)
```

> **Key idea:** Reverse engineering is a mix: re-implement what you can in Python (sign), extract the complex or changing parts into JS and run them through `execjs` (AES), and combine both to complete one request.

## 16.13 Infinite debugger: Principle and Bypass

### 16.13.1 Principle

Websites embed the `debugger` keyword in page JS, combined with a timer or an infinite loop, to freeze any crawler or researcher who opens DevTools:

```js
// Anti-debugging code (illustrative)
setInterval(function () { debugger; }, 100);
// or
while (true) { debugger; }
```

As long as DevTools is listening for breakpoints, `debugger` triggers a pause, creating an "infinite breakpoint".

### 16.13.2 Four Bypass Methods

| Method | Action |
|---|---|
| ① Disable breakpoints globally | Click "Deactivate breakpoints" in DevTools (or Ctrl+F8) |
| ② Never pause here | Right-click the `debugger` line → "Never pause here" |
| ③ Conditional breakpoint `false` | Right-click the line → "Add conditional breakpoint", enter `false` |
| ④ Rewrite the response with Fiddler | Use a proxy to replace `debugger` in the response JS with an empty string before returning it |

> **Note:** Methods ①–③ are temporary debugging tricks; method ④ removes the anti-debugging trap at the source, but alters page logic and is for research only.

## 16.14 PyExecJS Limitations and Alternatives

When PyExecJS's default runtime is unavailable and you want to avoid private APIs, call `node` directly with `subprocess`:

```python
import subprocess

def call_js(js_path: str, func: str, arg: str) -> str:
    # The JS file must end with a console.log(func(arg)) call
    cmd = ['node', '-e',
           f"const f=require('{js_path}');console.log(f.{func}('{arg}'))"]
    return subprocess.check_output(cmd, text=True).strip()
```

Comparison of alternatives:

| Option | Notes |
|---|---|
| `subprocess` + `node` | Most controllable and stable across versions, but has process overhead per call |
| `py_mini_racer` | Embeds V8, no external Node needed, actively maintained |
| `js2py` | Pure Python, no Node needed, but limited performance and compatibility |

**Summary Mnemonic**

- **Three locating steps:** find the endpoint → distinguish plaintext/encrypted → search JS by the signature key.
- **Three landing choices:** re-implement in Python / extract JS with execjs / third-party module.
- **Four core algorithms:** MD5, base64, AES (CBC/Pkcs7), SHA-256/RC4.
- **Signature recipe:** sort + concatenate + salt + MD5.
- **Four debugger bypasses:** disable breakpoints / Never pause here / conditional breakpoint `false` / Fiddler rewrite.

[<- Previous: elasticsearch](15-elasticsearch.md) | [Next: font anti-crawler and obfuscation ->](17-font-anti-crawler-and-ob.md)
