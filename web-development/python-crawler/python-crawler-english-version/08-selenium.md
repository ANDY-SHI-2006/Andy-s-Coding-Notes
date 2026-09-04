[<- Previous: xpath](07-xpath.md) | [Next: anti-crawler ->](09-anti-crawler.md)

# 8 Selenium

Requests can only fetch the HTML the server returns, which is useless for pages rendered by JavaScript. Selenium drives a real browser to execute JS, simulate typing and clicking, and lets a crawler "operate the browser like a human". This chapter has two parts: 8.1–8.7 cover the basics (installation, locating, interaction), and 8.8–8.14 cover the advanced topics (waiting, switching, anti-detection, exceptions, and real-world examples).

## 8.1 Installation and ChromeDriver Setup

```bash
pip install selenium
```

Selenium is only the "conductor"; it also needs a browser driver (chromedriver) matching your Chrome version to actually control the browser. Download a chromedriver matching your installed Chrome from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) and put it on PATH (or next to your script).

```python
from selenium import webdriver

driver = webdriver.Chrome()   # auto-discovers chromedriver on PATH
```

> **Note:** The chromedriver major version must match your Chrome, or startup fails with `SessionNotCreatedException`. If chromedriver is not on PATH, point to it explicitly with `webdriver.Chrome(service=Service('/path/to/chromedriver'))`.

## 8.2 Basic Usage and Browser Objects

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')   # open a page
print(driver.page_source)             # rendered page source (includes JS output)
print(driver.current_url)             # current URL
print(driver.get_cookies())           # current cookies
driver.close()                        # close the current tab/window
driver.quit()                         # exit the whole browser process
```

For other browsers, just swap the constructor:

```python
driver = webdriver.Chrome()
driver = webdriver.Firefox()
driver = webdriver.Safari()
```

> **Correction:** `webdriver.PhantomJS()` in the source is the old headless approach and was removed in Selenium 4. Use Chrome's headless flag instead (see 8.12 anti-detection) — do not use PhantomJS.

## 8.3 Locating Elements

Selenium 4 uses the `By` class for all locating strategies:

```python
from selenium.webdriver.common.by import By

element = driver.find_element(By.ID, 'kw')       # locate a single element
elements = driver.find_elements(By.XPATH, '//a') # locate many; returns a list
```

### 8.3.1 Single-Element Locators

| Strategy | Usage | Meaning |
|---|---|---|
| `By.ID` | `find_element(By.ID, 'kw')` | by the `id` attribute |
| `By.NAME` | `find_element(By.NAME, 'wd')` | by the `name` attribute |
| `By.XPATH` | `find_element(By.XPATH, '//div/a')` | by an XPath expression |
| `By.TAG_NAME` | `find_element(By.TAG_NAME, 'input')` | by tag name |
| `By.CLASS_NAME` | `find_element(By.CLASS_NAME, 'btn')` | by the `class` attribute |
| `By.CSS_SELECTOR` | `find_element(By.CSS_SELECTOR, '#kw')` | by a CSS selector |

### 8.3.2 Link Text Locators

```python
driver.find_element(By.LINK_TEXT, 'News')          # exact hyperlink text
driver.find_element(By.PARTIAL_LINK_TEXT, 'News')  # partial text is enough
```

> **Key idea:** `LINK_TEXT` must match the visible text inside the `<a>` tag exactly; `PARTIAL_LINK_TEXT` only needs a substring.

### 8.3.3 Multiple Elements

```python
# find_elements returns a list you can iterate over
links = driver.find_elements(By.CSS_SELECTOR, 'a.title')
for link in links:
    print(link.text)
```

> **Note:** `find_element` raises `NoSuchElementException` when nothing matches; `find_elements` returns an empty list instead (no exception).

> **Correction:** Selenium 4 removed the old API such as `find_element_by_id('kw')` and `find_elements_by_name(...)`. Use `find_element(By.ID, 'kw')` and `find_elements(By.NAME, ...)` instead.

## 8.4 Element Interaction

```python
from selenium.webdriver.common.keys import Keys

box = driver.find_element(By.ID, 'kw')
box.send_keys('python')          # type text
box.clear()                      # clear the input
box.send_keys(Keys.ENTER)        # press Enter (Keys.RETURN is equivalent)
box.click()                      # click the element
```

Common `Keys`: `Keys.ENTER`/`Keys.RETURN` (Enter), `Keys.TAB`, `Keys.ESCAPE`, and `Keys.CONTROL`/`Keys.COMMAND` (usable for combos like `send_keys(Keys.CONTROL, 'a')`).

## 8.5 Action Chains (ActionChains)

For compound actions like drag-and-drop or hover, chain several actions and run them with `perform()`:

```python
from selenium.webdriver import ActionChains

A = driver.find_element(By.ID, 'source')
B = driver.find_element(By.ID, 'target')

actions = ActionChains(driver)
actions.drag_and_drop(A, B)   # drag A onto B
actions.perform()             # run the chain
```

`ActionChains` also supports `move_to_element` (hover), `double_click`, and `context_click` (right-click).

## 8.6 Reading Element Information

```python
el = driver.find_element(By.ID, 'link')
print(el.text)                        # visible text
print(el.get_attribute('href'))       # attribute value
print(el.get_attribute('class'))
```

- `.text`: the rendered text of the element.
- `get_attribute(name)`: any HTML attribute (`href`, `src`, `class`, `style`, ...).

## 8.7 Executing JavaScript

Use `execute_script` to run arbitrary JS in the browser, most often to scroll:

```python
# scroll to the bottom (triggers lazy loading)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

# scroll back to the top
driver.execute_script('window.scrollTo(0, 0)')
```

Related concepts:

| Property | Meaning |
|---|---|
| `scrollHeight` | total content height (including hidden part) |
| `scrollTop` | how far the content has been scrolled down |
| `scrollWidth` | total content width |
| `scrollLeft` | how far the content has been scrolled right |

## 8.8 Explicit Wait: WebDriverWait and EC

On async pages, elements may not appear immediately. `WebDriverWait` polls until a condition is met or times out:

```python
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)   # wait up to 10 seconds
# note: EC locator arguments are a tuple (By.ID, 'result')
wait.until(EC.presence_of_element_located((By.ID, 'result')))
```

Common `expected_conditions` (EC) methods:

| Method | Meaning |
|---|---|
| `title_is` / `title_contains` | title equals / contains text |
| `presence_of_element_located` | element is present in the DOM |
| `visibility_of_element_located` | element is visible |
| `visibility_of` | an already-located element is visible |
| `presence_of_all_elements_located` | at least one matching element is present |
| `text_to_be_present_in_element` | element text contains something |
| `frame_to_be_available_and_switch_to_it` | iframe is ready and switches into it |
| `invisibility_of_element_located` | element is invisible |
| `element_to_be_clickable` | element is clickable |
| `staleness_of` | element has been removed from the DOM |
| `element_to_be_selected` | element is selected |
| `element_located_to_be_selected` | the located element is selected |
| `element_selection_state_to_be` | element's selection state equals a value |
| `element_located_selection_state_to_be` | located element's selection state |
| `alert_is_present` | an alert box is shown |

> **Key idea:** EC methods take a "locator tuple" `(By.X, 'value')`. In `presence_of_element_located((By.ID, 'x'))` the locator is wrapped in **double parentheses**.

## 8.9 Switching iframes and Tabs

An iframe is a separate context; you must switch into it before locating its inner elements:

```python
driver.switch_to.frame('iframeResult')   # pass the iframe's id or name
# ... now you can locate elements inside the iframe ...
driver.switch_to.default_content()       # switch back to the main document
```

Manage multiple tabs/windows with `window_handles`:

```python
driver.execute_script('window.open()')   # open a new tab
handles = driver.window_handles          # list of all window/tab IDs
driver.switch_to.window(handles[1])      # switch to the second tab
driver.switch_to.window(handles[0])      # switch back to the first
```

## 8.10 Back and Forward

```python
driver.back()       # go back
driver.forward()    # go forward
```

## 8.11 Exception Handling

```python
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.ID, 'result')))
except TimeoutException:
    print('timed out')
except NoSuchElementException:
    print('element not found')
finally:
    driver.close()   # close the browser no matter what, to avoid stray processes
```

> **Note:** Use `try/except/finally` so `driver.close()` runs even on error; otherwise leftover Chrome processes accumulate and consume memory.

## 8.12 Anti-Detection Configuration (ChromeOptions)

Websites can detect Selenium via `navigator.webdriver` and other signals. Use `ChromeOptions` for basic disguise and login-state reuse:

```python
from selenium.webdriver import ChromeOptions

options = ChromeOptions()
# remove the "Chrome is being controlled by automated software" banner
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
# point to a user data directory to reuse the login session
options.add_argument(r'--user-data-dir=C:\path\to\your\chrome\profile')

driver = webdriver.Chrome(options=options)
```

> **Key idea:** When `--user-data-dir` points to an existing Chrome profile, Selenium reuses its cookies and login state — the standard trick for crawling login-gated sites such as Taobao.

## 8.13 Example: Baidu Search

Full flow: open Baidu → locate the input → type a keyword → press Enter → wait for results → grab the source:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get('https://www.baidu.com')
    box = driver.find_element(By.ID, 'kw')      # search input
    box.send_keys('python')                     # type the keyword
    box.send_keys(Keys.ENTER)                   # press Enter to search
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(driver.page_source)                   # rendered source
finally:
    driver.close()
```

## 8.14 Example: Taobao Spider (Tb_spider)

Taobao requires login and renders data with JS, so plain requests cannot fetch it. Use Selenium with a reused login state, hand `page_source` to BeautifulSoup, and dump the result to JSON.

```python
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup


class TbSpider:
    def __init__(self, keyword):
        options = ChromeOptions()
        options.add_argument(r'--user-data-dir=C:\path\to\your\chrome\profile')
        self.driver = webdriver.Chrome(options=options)
        self.keyword = keyword
        self.items = []

    def get_tb(self):
        """Open the search page and scroll to load items"""
        url = f'https://s.taobao.com/search?q={self.keyword}'
        self.driver.get(url)
        # simple paging example: scroll to bottom to trigger loading
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        self.get_html()

    def get_html(self):
        """Hand page_source to BeautifulSoup for parsing"""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        # the class name must not have a trailing space (the source had one)
        for item in soup.select('.title--ASSt27UY'):
            self.items.append(item.get_text(strip=True))

    def save(self):
        with open('taobao.json', 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

    def run(self):
        self.get_tb()
        self.save()
        self.driver.close()


if __name__ == '__main__':
    s = TbSpider('phone')
    s.run()
```

> **Correction:** The source `Tb_spider.py` has two bugs: (1) the CSS selector `.title--ASSt27UY ` has a trailing space, which breaks matching — remove it; (2) `run()` calls the global `s.get_tb()`/`s.get_html()` (an implicit dependency on the `s` instance in `if __name__ == '__main__'`) — use `self.get_tb()` / `self.get_html()` instead.

> **Note:** The code above is a teaching skeleton. Real Taobao has strict anti-crawler and login checks. Respect the target site's robots.txt and relevant laws, and throttle your requests.

## Summary Mnemonic

- **Start:** `webdriver.Chrome()` → `get(url)` → `page_source` → `close()`.
- **Locate:** `find_element(By.ID/NAME/XPATH/TAG_NAME/CLASS_NAME/CSS_SELECTOR, ...)`; use `find_elements` for many.
- **Link text:** `By.LINK_TEXT` exact, `By.PARTIAL_LINK_TEXT` partial.
- **Interact:** `send_keys` types, `clear` clears, `click` clicks, `Keys.ENTER` presses Enter.
- **Action chains:** `ActionChains(driver).drag_and_drop(A, B).perform()`.
- **Switch:** `switch_to.frame` for iframes, `switch_to.window` for tabs, `window_handles` lists windows.
- **Wait:** `WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'x')))` — the locator is a tuple.
- **JS:** `execute_script('window.scrollTo(0, document.body.scrollHeight)')` scrolls to the bottom.
- **Anti-detection:** `ChromeOptions` with `excludeSwitches`, `useAutomationExtension=False`, and `--user-data-dir` for login reuse.
- **Deprecated API:** `find_element_by_id` → `find_element(By.ID, ...)`; `PhantomJS` is removed.

[<- Previous: xpath](07-xpath.md) | [Next: anti-crawler ->](09-anti-crawler.md)
