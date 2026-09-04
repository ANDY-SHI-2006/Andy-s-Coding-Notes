[<- Previous: anti-crawler](09-anti-crawler.md) | [Next: multitasking ->](11-multitasking.md)

# 10 Captcha

Chapter 9 explained that captchas are one of the most common anti-crawler measures. This chapter covers "how to recognize them": starting from the concept and purpose of captchas, it presents four approaches, focusing on OCR (Tesseract), image preprocessing, and the Baidu OCR cloud platform, plus decoding platforms and manual recognition.

## 10.1 Concept and Purpose of Captchas

CAPTCHA (Completely Automated Public Turing test to tell Computers and Humans Apart) is the full name for the captcha. It uses graphics or text that humans can read easily but machines struggle to recognize automatically, separating people from scripts.

Captchas are used to:

- prevent brute-force password cracking.
- prevent vote/ticket farming.
- prevent spam comments.
- prevent malicious page refreshing and traffic inflation.

## 10.2 Use Cases and Approaches

Captchas typically appear at registration, login, and when requests are too frequent.

There are four ways to handle an image captcha:

| Approach | Description | Best for |
|---|---|---|
| Manual input (`input`) | Show the image and type it by hand | A few, debugging |
| OCR engine | Recognize text programmatically | Simple, clear captchas |
| Decoding platform | Paid platform with human solvers | Hard captchas, high volume |
| Manual recognition | Download and read it yourself | One-off tasks |

## 10.3 OCR and Tesseract

OCR (Optical Character Recognition) extracts text from image files automatically. The most common free OCR engine in the Python ecosystem is Google's Tesseract.

### 10.3.1 Installing Tesseract

Installation per platform:

```bash
# macOS
brew install --with-training-tools tesseract

# Linux
sudo apt-get install tesseract-ocr
```

On Windows, download the official installer (e.g. `tesseract-ocr-w64-setup`) and then:

- Add the install directory (e.g. `C:\Program Files\Tesseract-OCR`) to PATH.
- If you use a Chinese language pack, set `TESSDATA_PREFIX` to the tessdata directory.

### 10.3.2 Installing Python Libraries and Running pytesseract

```bash
pip install pillow        # PIL: image processing
pip install pytesseract   # calls the Tesseract engine
```

```python
from PIL import Image
import pytesseract

# point to the actual Tesseract executable (common Windows path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = Image.open('captcha.png')          # open an image (path is required)
result = pytesseract.image_to_string(img)
print(result.strip())
```

> **Correction:** The source wrote `im = Image.open()` without a file path, which raises `TypeError`. The correct form is `Image.open('captcha.png')` (or any image path).

## 10.4 Image Preprocessing

Captchas often carry noise and interference lines, so raw OCR accuracy is low. Grayscale, binarize, and denoise first, then OCR — accuracy improves greatly.

### 10.4.1 Grayscale and Binarization

```python
from PIL import Image

def binarizing(img, threshold=140):
    """Grayscale then threshold: pixels below the threshold go black(0), others white(255)"""
    img = img.convert('L')           # convert to grayscale
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0      # below threshold → black
            else:
                pixdata[x, y] = 255    # at/above threshold → white
    return img
```

> **Correction:** The source comment said "pixels above the threshold are black", which contradicts the code. The code is `if pixdata[x, y] < threshold: pixdata[x, y] = 0`, meaning **pixels below the threshold are black** — fix the comment accordingly.

### 10.4.2 Denoising (Removing Isolated Specks)

```python
def depoint(img):
    """Remove isolated specks: count white pixels in each pixel's 8-neighborhood;
    treat pixels with too few white neighbors as noise and set them white"""
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            # count white pixels among the 8 neighbors (4 edges + 4 diagonals)
            if pixdata[x, y - 1] > 245: count += 1
            if pixdata[x, y + 1] > 245: count += 1
            if pixdata[x - 1, y] > 245: count += 1
            if pixdata[x + 1, y] > 245: count += 1
            if pixdata[x - 1, y - 1] > 245: count += 1
            if pixdata[x - 1, y + 1] > 245: count += 1
            if pixdata[x + 1, y - 1] > 245: count += 1
            if pixdata[x + 1, y + 1] > 245: count += 1
            # too few white neighbors (isolated black speck) → set white
            if count > 4:
                pixdata[x, y] = 255
    return img
```

Full preprocessing + recognition flow:

```python
img = Image.open('captcha.png')
img = binarizing(img, threshold=140)   # binarize
img = depoint(img)                     # denoise
result = pytesseract.image_to_string(img)
print(result.strip())
```

## 10.5 Baidu OCR Cloud Platform

Tesseract struggles with hard captchas (distorted, overlapping, interference lines). Baidu OCR offers a cloud recognition API with better results. First register an application in the Baidu AI Cloud console to get an `AppKey`/`SecretKey`.

### 10.5.1 Getting an access_token

Baidu Cloud APIs require exchanging `client_id`/`client_secret` for an `access_token` first:

```python
import requests

token_url = 'https://aip.baidubce.com/oauth/2.0/token'
params = {
    'grant_type': 'client_credentials',
    'client_id': '<your client_id>',
    'client_secret': '<your client_secret>',
}
resp = requests.get(token_url, params=params, timeout=10)
access_token = resp.json().get('access_token')
```

> **Note:** `client_id`, `client_secret`, and `access_token` are sensitive credentials — they are masked as `<placeholders>` here. Load them from a config file or environment variables, never hard-code them into committed code.

### 10.5.2 Recognizing with AipOcr

The `baidu-aip` SDK wraps the token exchange; just pass the three keys:

```bash
pip install baidu-aip
```

```python
from aip import AipOcr

APP_ID = '<your APP_ID>'
API_KEY = '<your API_KEY>'
SECRET_KEY = '<your SECRET_KEY>'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)   # the SDK manages the token for you

with open('captcha.jpg', 'rb') as fp:
    image = fp.read()

options = {
    'detect_direction': 'true',      # detect image orientation
    'language_type': 'CHN_ENG',      # Chinese + English
}
res = client.basicGeneral(image, options)

# extract the recognized text from the result
if 'words_result' in res and res['words_result']:
    code = res['words_result'][0]['words']
    print('recognized:', code)
```

> **Key idea:** Baidu OCR returns JSON: `res['words_result']` is a list whose items each contain a `words` field; the first item is usually the captcha text. If you get an `error_code`, look it up (commonly an expired token or insufficient quota).

## 10.6 Decoding Platforms

For hard captchas at high volume, you can pay a decoding platform (human solvers). For example, Feifei Decoding (`http://www.fateadm.com/`) lets you upload the captcha image and returns the text recognized by a human. Such platforms usually provide an HTTP API or SDK, and require a registered account with a balance.

## 10.7 Manual Recognition

The simplest brute-force approach: display the image and type it yourself.

```python
from PIL import Image

img = Image.open('captcha.png')
img.show()                    # pop up the image window
code = input('enter the captcha: ')   # type it manually
print('you entered:', code)
```

> **Note:** `input()` blocks the program waiting for input, so it is only suitable for debugging and a handful of captchas, not large-scale automation.

## 10.8 Common Errors

| Error | Cause | Fix |
|---|---|---|
| `TesseractNotFoundError` | Tesseract engine not found | Set `pytesseract.pytesseract.tesseract_cmd` to the real path |
| `TypeError: open() missing required argument` | `Image.open()` called without a path | Pass a path: `Image.open('captcha.png')` |
| Garbled or empty result | No preprocessing, or missing language pack | Binarize/denoise first; check the language pack |

```python
import pytesseract
from pytesseract import TesseractNotFoundError

try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    result = pytesseract.image_to_string(img)
except TesseractNotFoundError:
    print('Tesseract not found; check the install path and set tesseract_cmd')
```

> **Key idea:** `TesseractNotFoundError` means Python cannot find tesseract.exe. Fix it by writing the install path into `pytesseract.pytesseract.tesseract_cmd`, or by adding the install directory to PATH.

## Summary Mnemonic

- **CAPTCHA:** a fully automated Turing test to tell computers and humans apart; blocks brute-force, farming, spam, and page-refreshing.
- **Four approaches:** manual `input` / OCR (Tesseract) / decoding platform / manual `Image.show()`.
- **OCR three steps:** `Image.open('captcha.png')` → `image_to_string(img)` → `.strip()`.
- **Preprocessing:** `convert('L')` grayscale → below-threshold to black (binarize) → 8-neighborhood count to drop isolated specks.
- **Baidu OCR:** `AipOcr(APP_ID, API_KEY, SECRET_KEY)` + `basicGeneral(image, options)`; read `words_result[0]['words']`.
- **Errors:** `TesseractNotFoundError` → set `tesseract_cmd`; `Image.open()` needs a path.

[<- Previous: anti-crawler](09-anti-crawler.md) | [Next: multitasking ->](11-multitasking.md)
