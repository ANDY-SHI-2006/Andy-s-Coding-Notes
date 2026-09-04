[<- Previous: js reverse engineering](16-js-reverse-engineering.md) | [Next: real-world projects ->](18-real-world-projects.md)

# 17 Font Anti-Crawler and Obfuscation

In advanced crawling there are two kinds of protection that "look fine but can't be read": one replaces page text with a custom font so the source is gibberish but renders as normal text (font anti-crawler); the other obfuscates front-end JS into spaghetti and hands out cookies step by step through "521" challenges (ob obfuscation + accelerated-le / jsjiami). This chapter covers both: first restoring a font mapping with fontTools, then the string decryption, embedded SHA-256, and three-request flow of ob obfuscation.

## 17.1 How Font Anti-Crawler Works

A site renders text with a custom `.woff` font: the HTML contains encoded entities such as `&#xE000;`, and the font file maps those code points to glyphs that "look like normal digits/text".

> **Key idea:** Font anti-crawler is essentially a **lookup-table swap** — the mapping between a character's code point and its glyph is shuffled, and only the matching font renders it correctly. A crawler gets the code points, so it must reverse the plaintext from the font's cmap table.

Tools: the browser DevTools shows the downloaded woff file; the online tool fonteditor (fonteditor.org) visualizes the font's cmap and glyphs.

## 17.2 Parsing Fonts with fontTools

`fontTools` is the standard Python library for parsing font files:

```bash
pip install fonttools
```

```python
from fontTools.ttLib import TTFont

font = TTFont('file(1).woff')
cmap = font['cmap'].getBestCmap()   # {codepoint: glyph name}, e.g. {0xE000: 'glyph00001', ...}
glyphs = font.getGlyphOrder()       # ordered glyph names, in the font's internal order
font.saveXML('font.xml')            # export as readable XML for manual inspection
```

| Attribute / method | Meaning |
|---|---|
| `font['cmap'].getBestCmap()` | Returns the `{codepoint: glyph name}` mapping |
| `font.getGlyphOrder()` | Returns the ordered list of glyph names |
| `font.saveXML(path)` | Exports XML to compare glyphs against code points |

> **Note:** `getGlyphOrder()[0]` is usually `.notdef` (the undefined glyph), which is not a real content glyph and must be excluded when aligning.

## 17.3 Restoring the Font Mapping

Once you have the cmap and the glyph order, you need a "plaintext order" to align with it. The plaintext order comes from visual comparison (matching rendered characters to code points one by one) or from the glyph outlines in the font XML.

```python
from fontTools.ttLib import TTFont

font = TTFont('file(1).woff')
cmap = font['cmap'].getBestCmap()
glyphs = [g for g in font.getGlyphOrder() if g != '.notdef']

# Plaintext characters, aligned to glyph order by visual comparison (example: digits 0-9)
plain_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Build {plaintext: encoded entity}
plain_to_encoded = {}
for i, glyph_name in enumerate(glyphs):
    for code, name in cmap.items():
        if name == glyph_name:
            plain_to_encoded[plain_chars[i]] = f'&#x{code:04x}'
            break

# Flip the mapping and bulk-replace encoded entities in the HTML
encoded_to_plain = {v: k for k, v in plain_to_encoded.items()}
for enc, plain in encoded_to_plain.items():
    html = html.replace(enc, plain)
```

> **Correction:** The source materials use an inner `else: unicode_mapping[char] = 'no mapping found'` whose logic is muddled — every non-match writes a placeholder string — and `getGlyphOrder()[0]` is `.notdef`, which can misalign with `font_list[0]=""`. The correct approach, as above: **drop `.notdef` first, then align plaintext to the glyph order one by one, and only write a mapping when a code point actually matches**.

## 17.4 ob Obfuscation Overview

"ob obfuscation" turns normal JS into unreadable code. Common techniques:

- **String array + rotation**: all strings are extracted into an array, scrambled with `push` / `shift`, then indexed by hex offsets.
- **Hex-indexed access**: something like `_0x147eba[_0x22abec(0x280)]` means "take the element at 0x280".
- **Control-flow flattening**: if/else is flattened into a switch table, hiding the jump logic.

Common obfuscators: javascript-obfuscator, jsjiami (same family as "accelerated-le"), jsl (the accelerated-le online version).

> **Key idea:** ob obfuscation does not change program semantics, only the cost of reading it. When reversing you don't need to "fully restore" the source — you just need the obfuscated JS to **run and produce the cookie/parameter you want**.

## 17.5 Decrypting ob Strings (base64 + RC4)

The most eye-catching part of obfuscated code is the pile of hex strings, which are usually base64-decoded and then RC4-decrypted. After extracting a decryption function such as `_0x40ad`, you can re-implement it in Python:

```python
import base64

def rc4(key: bytes, data: bytes) -> bytes:
    S = list(range(256))
    j = 0
    for i in range(256):                      # KSA
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = []
    for ch in data:                           # PRGA
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(ch ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

def decrypt_string(b64_cipher: str, key: bytes) -> str:
    return rc4(key, base64.b64decode(b64_cipher)).decode('utf-8', errors='ignore')
```

> **Key idea:** RC4 is a stream symmetric cipher; decryption and encryption are the same function (XOR symmetry). Once you have the key from the JS, batch-decrypt all obfuscated strings and the code becomes much more readable.

## 17.6 Embedded SHA-256 and the Accelerated-le Flow

Some accelerated-le versions embed a custom SHA-256 (a `hash` function) in the obfuscated JS to generate `__jsl_clearance_s`. It is recognizable by the SHA-256 constants:

| Constant | Value | Meaning |
|---|---|---|
| K constants | `0x428a2f98` … | the 64 per-round SHA-256 constants |
| H initial values | `0x6a09e667` … | the 8 initial SHA-256 hash values |

A `go()` function then brute-forces some input until the hash matches the returned `ct` value, producing the cookie.

> **Key idea:** Seeing `0x428a2f98` / `0x6a09e667` almost always means a SHA-256 implementation. You don't need to rewrite it — Python's `hashlib.sha256` does the job; the key question is "what input is hashed, and what condition must match".

## 17.7 The Full Accelerated-le Flow (Three Requests)

The accelerated-le (jsjiami/jsl) flow is typically a "521 three-way handshake":

| Step | Response | Result |
|---|---|---|
| First request | 521 + set-cookie | `__jsluid_s` (identity cookie) |
| Second request | 521 + ob obfuscated JS | running the JS produces `__jsl_clearance_s` (clearance cookie) |
| Third request | 200 data | carry the full cookie to fetch the data |

The routine for handling the obfuscated JS:

1. `re.findall` to extract the JS inside `<script>`.
2. `re.sub` to remove distracting/detection code.
3. Prepend `window=global;document={};` to patch the environment.
4. Run it with `nodejs.compile(...).call(...)` and grab the cookie.

```python
import re, requests
from local_node import LocalNode

class Spider(LocalNode):
    def __init__(self):
        self.url = '<target page>'
        self.headers = {'User-Agent': '<UA>'}
        self.session = requests.Session()
        self.insert_js_1 = 'window=global;document={};'
        self.insert_js_2 = ';function get_cookie(){return document.cookie;}'

    def first_request(self):          # 521 -> __jsluid_s
        r = self.session.get(self.url, headers=self.headers)
        for k, v in r.cookies.items():
            self.__jsluid_s = f'{k}={v}'
        js = re.findall('cookie=(.*?);location', r.text, re.S)[0]
        clearance = self.nodejs.eval(js).split(';')[0]
        self.headers['Cookie'] = f'{clearance};{self.__jsluid_s}'

    def two_request(self):            # 521 -> ob JS -> __jsl_clearance_s
        r = self.session.get(self.url, headers=self.headers)
        js = re.findall('<script>(.*?)</script>', r.text, re.S)[0]
        js = re.sub(r"if\(_0x\w+\['wt'\]\)\{.*?else.*?\}.*?setTimeout.*?function\(\)\{",
                    '', js, re.S)
        new_js = self.insert_js_1 + js + self.insert_js_2
        cookie = self.nodejs.compile(new_js).call('get_cookie').split(';')[0]
        self.headers['Cookie'] = f'{self.__jsluid_s};{cookie}'
```

> **Correction:** The source materials are inconsistent with class name `Spider` / `Spdier` and method name `three_requests` / `third_reqeusts`; `class Spdier(LocalNode)` should be `Spider`. The code above uses the correct spellings.

Some sites (such as the full CNVD case) insert a captcha step between the requests: `first_request → two_request → get_img (fetch captcha image) → post_img (submit the recognized answer) → third_request (fetch data)`. See 17.8 for captcha recognition.

## 17.8 Recognizing Captchas with a Solving Platform (jfbym)

Some accelerated-le versions also pop a captcha, which must be handed to a solving platform. Using jfbym as an example:

```python
import base64, requests
from jsonpath import jsonpath

def verify(b=None, str_type=None, token=None):
    url = "http://api.jfbym.com/api/YmServer/customApi"
    data = {"token": token, "type": str_type, "image": b}
    return requests.post(url, json=data).json()

# 1) Get the base64 captcha image from the API response
img_b64 = jsonpath(resp.json(), '$..image')[0]
with open('img.png', 'wb') as f:
    f.write(base64.b64decode(img_b64))

# 2) Submit it to the solving platform
ver = verify(b=img_b64, str_type='10118', token='<your token>')
print(ver)
```

> **Note:** The solving platform's `token` and `type` are account-sensitive, redacted above as `<your token>`. `type` corresponds to different captcha kinds (e.g. `10118` for a certain click/character captcha).

## 17.9 Bypassing Browser Environment Detection

Obfuscated JS often contains an environment-detection function (such as `_0x13ea9a()`) that detects headless browsers or whether DevTools is open. Running the JS directly in Node, outside a browser, fails or stalls because `window` / `document` are missing.

Two ways to cope:

- **Patch the environment**: prepend `window=global;document={};` and similar empty objects so the JS can run far enough to produce the cookie.
- **Headless browser + stealth**: use Puppeteer / Playwright with a stealth plugin to masquerade as a real browser.

> **Key idea:** Environment detection usually only affects whether execution can continue, not the final cookie generation. Prefer patching the environment to run the obfuscated JS; fall back to a headless browser when patching is not enough.

**Summary Mnemonic**

- **Font anti-crawler:** cmap is the codebook — `getBestCmap` for code points, `getGlyphOrder` for glyphs, drop `.notdef` before aligning.
- **Font restore:** `{plaintext: encoded entity}` → flip to `{encoded entity: plaintext}` → bulk `replace`.
- **ob obfuscation:** string array + rotation + hex indexing; base64 + RC4 decrypt the strings first.
- **Accelerated-le:** 521 three-request flow — `__jsluid_s` → run JS to get `__jsl_clearance_s` → fetch data.
- **Patch environment:** `window=global;document={};` makes obfuscated JS runnable in Node.

[<- Previous: js reverse engineering](16-js-reverse-engineering.md) | [Next: real-world projects ->](18-real-world-projects.md)
