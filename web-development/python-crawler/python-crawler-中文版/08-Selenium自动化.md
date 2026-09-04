[← 上一篇：XPath解析](07-XPath解析.md) | [下一篇：反爬虫与应对 →](09-反爬虫与应对.md)

# 8 Selenium自动化

Requests 只能拿到服务器返回的 HTML，遇到由 JavaScript 渲染的动态页面就无能为力。Selenium 通过驱动真实浏览器执行 JS、模拟点击输入，让爬虫"像人一样操作浏览器"。本章分两部分：8.1–8.7 是基础（安装、定位、交互），8.8–8.14 是进阶（等待、切换、反检测、异常与实战）。

## 8.1 安装与 ChromeDriver 配置

```bash
pip install selenium
```

Selenium 本身只是"指挥棒"，还需要一个与 Chrome 版本匹配的浏览器驱动 chromedriver 才能真正驱动浏览器。推荐从 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下载与本地 Chrome 版本一致的 chromedriver，放到 PATH 里（或脚本同目录）。

```python
from selenium import webdriver

driver = webdriver.Chrome()   # 自动查找 PATH 中的 chromedriver
```

> **注意：** chromedriver 版本必须与 Chrome 大版本一致，否则启动报 `SessionNotCreatedException`。若 chromedriver 不在 PATH，可用 `webdriver.Chrome(service=Service('/path/to/chromedriver'))` 显式指定路径。

## 8.2 基础使用与浏览器对象

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')   # 打开页面
print(driver.page_source)             # 当前页面源码（含 JS 渲染结果）
print(driver.current_url)             # 当前 URL
print(driver.get_cookies())           # 当前 cookie
driver.close()                        # 关闭当前标签页/窗口
driver.quit()                         # 退出浏览器进程
```

不同浏览器只需换构造函数：

```python
driver = webdriver.Chrome()
driver = webdriver.Firefox()
driver = webdriver.Safari()
```

> **勘误：** 源课件里的 `webdriver.PhantomJS()` 是无头浏览器旧方案，已在 Selenium 4 中移除。如需无头模式请用 Chrome 的 headless 参数（见 8.12 反检测配置），不要再用 PhantomJS。

## 8.3 元素定位

Selenium 4 统一通过 `By` 类指定定位策略：

```python
from selenium.webdriver.common.by import By

element = driver.find_element(By.ID, 'kw')      # 定位单个元素
elements = driver.find_elements(By.XPATH, '//a') # 定位多个元素，返回列表
```

### 8.3.1 单元素定位

| 定位策略 | 写法 | 说明 |
|---|---|---|
| `By.ID` | `find_element(By.ID, 'kw')` | 按 id 属性 |
| `By.NAME` | `find_element(By.NAME, 'wd')` | 按 name 属性 |
| `By.XPATH` | `find_element(By.XPATH, '//div/a')` | 按 XPath 表达式 |
| `By.TAG_NAME` | `find_element(By.TAG_NAME, 'input')` | 按标签名 |
| `By.CLASS_NAME` | `find_element(By.CLASS_NAME, 'btn')` | 按 class 属性 |
| `By.CSS_SELECTOR` | `find_element(By.CSS_SELECTOR, '#kw')` | 按 CSS 选择器 |

### 8.3.2 链接文字定位

```python
driver.find_element(By.LINK_TEXT, '新闻')          # 完整超链接文字
driver.find_element(By.PARTIAL_LINK_TEXT, '新闻')  # 部分文字即可
```

> **核心要点：** `LINK_TEXT` 要求与 `<a>` 标签内的可见文字完全一致，`PARTIAL_LINK_TEXT` 只要包含即可。

### 8.3.3 多元素定位

```python
# find_elements 返回元素列表，可遍历
links = driver.find_elements(By.CSS_SELECTOR, 'a.title')
for link in links:
    print(link.text)
```

> **注意：** `find_element` 找不到元素会抛 `NoSuchElementException`；`find_elements` 找不到则返回空列表（不抛异常）。

> **勘误：** Selenium 4 移除了旧版 API `find_element_by_id('kw')`、`find_elements_by_name(...)` 等写法。统一改为 `find_element(By.ID, 'kw')`、`find_elements(By.NAME, ...)`。

## 8.4 元素交互

```python
from selenium.webdriver.common.keys import Keys

box = driver.find_element(By.ID, 'kw')
box.send_keys('python')          # 输入文字
box.clear()                      # 清空输入框
box.send_keys(Keys.ENTER)        # 回车（也可用 Keys.RETURN）
box.click()                      # 点击元素
```

`Keys` 常用键：`Keys.ENTER`/`Keys.RETURN`（回车）、`Keys.TAB`、`Keys.ESCAPE`、`Keys.CONTROL`/`Keys.COMMAND`（可配合 `send_keys(Keys.CONTROL, 'a')` 实现组合键）。

## 8.5 动作链 ActionChains

对于拖拽、悬停等复合操作，用 `ActionChains` 串起多个动作后 `perform()` 一次性执行：

```python
from selenium.webdriver import ActionChains

A = driver.find_element(By.ID, 'source')
B = driver.find_element(By.ID, 'target')

actions = ActionChains(driver)
actions.drag_and_drop(A, B)   # 把 A 拖到 B
actions.perform()             # 执行动作链
```

`ActionChains` 还支持 `move_to_element`（悬停）、`double_click`（双击）、`context_click`（右键）等。

## 8.6 获取元素信息

```python
el = driver.find_element(By.ID, 'link')
print(el.text)                        # 元素可见文本
print(el.get_attribute('href'))       # 获取属性值
print(el.get_attribute('class'))
```

- `.text`：取元素渲染后的文本。
- `get_attribute(name)`：取任意 HTML 属性（如 `href`、`src`、`class`、`style`）。

## 8.7 执行 JavaScript

用 `execute_script` 让浏览器执行任意 JS，常用于滚动页面：

```python
# 滚动到底部（触发懒加载）
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

# 滚动回顶部
driver.execute_script('window.scrollTo(0, 0)')
```

相关概念：

| 属性 | 含义 |
|---|---|
| `scrollHeight` | 元素内容的总高度（含不可见部分） |
| `scrollTop` | 已向下滚动的距离 |
| `scrollWidth` | 元素内容的总宽度 |
| `scrollLeft` | 已向右滚动的距离 |

## 8.8 显式等待 WebDriverWait 与 EC

页面异步加载时元素未必立即出现，`WebDriverWait` 会轮询等待直到条件满足或超时：

```python
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)   # 最多等 10 秒
# 注意：EC 的定位参数是元组形式 (By.ID, 'result')
wait.until(EC.presence_of_element_located((By.ID, 'result')))
```

`expected_conditions`（EC）常用方法：

| 方法 | 含义 |
|---|---|
| `title_is` / `title_contains` | 标题等于 / 包含某文本 |
| `presence_of_element_located` | 元素出现在 DOM |
| `visibility_of_element_located` | 元素可见 |
| `visibility_of` | 已定位元素可见 |
| `presence_of_all_elements_located` | 至少一个匹配元素出现 |
| `text_to_be_present_in_element` | 元素文本包含某内容 |
| `frame_to_be_available_and_switch_to_it` | iframe 可用并切进去 |
| `invisibility_of_element_located` | 元素不可见 |
| `element_to_be_clickable` | 元素可点击 |
| `staleness_of` | 元素已从 DOM 移除 |
| `element_to_be_selected` | 元素被选中 |
| `element_located_to_be_selected` | 定位到的元素被选中 |
| `element_selection_state_to_be` | 元素选中状态为指定值 |
| `element_located_selection_state_to_be` | 定位元素的选中状态 |
| `alert_is_present` | 弹出 alert 框 |

> **核心要点：** `EC` 方法统一接收"定位元组" `(By.X, 'value')`，即 `presence_of_element_located((By.ID, 'x'))` 里是**双层括号**。

## 8.9 iframe 与选项卡切换

页面里的 iframe 是独立上下文，必须先切进去才能定位内部元素：

```python
driver.switch_to.frame('iframeResult')   # 传 iframe 的 id 或 name
# ... 此时可以定位 iframe 内部元素 ...
driver.switch_to.default_content()       # 切回主文档
```

多标签页/窗口用 `window_handles` 管理：

```python
driver.execute_script('window.open()')   # 新开一个标签页
handles = driver.window_handles          # 所有窗口/标签页的 ID 列表
driver.switch_to.window(handles[1])      # 切换到第二个标签页
driver.switch_to.window(handles[0])      # 切回第一个
```

## 8.10 前进后退

```python
driver.back()       # 后退
driver.forward()    # 前进
```

## 8.11 异常处理

```python
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.ID, 'result')))
except TimeoutException:
    print('等待超时')
except NoSuchElementException:
    print('元素不存在')
finally:
    driver.close()   # 无论成败都关闭浏览器，避免残留进程
```

> **注意：** 用 `try/except/finally` 保证异常时也能 `driver.close()`，否则会积累大量 Chrome 进程占用内存。

## 8.12 反检测配置（ChromeOptions）

网站能通过 `navigator.webdriver` 等特征识别 Selenium。用 `ChromeOptions` 做基础伪装并复用登录态：

```python
from selenium.webdriver import ChromeOptions

options = ChromeOptions()
# 去掉 "Chrome 正受到自动测试软件控制" 提示
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
# 指定用户数据目录，复用登录态（下次启动无需重新登录）
options.add_argument(r'--user-data-dir=C:\path\to\your\chrome\profile')

driver = webdriver.Chrome(options=options)
```

> **核心要点：** `--user-data-dir` 指向一个已有 Chrome 用户数据目录后，Selenium 会复用其中的 cookie 和登录态，是爬取需登录网站（如淘宝）的常用手段。

## 8.13 实战：百度搜索

完整流程：打开百度 → 定位输入框 → 输入关键词 → 回车 → 等待结果 → 取源码：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
try:
    driver.get('https://www.baidu.com')
    box = driver.find_element(By.ID, 'kw')      # 搜索输入框
    box.send_keys('python')                     # 输入关键词
    box.send_keys(Keys.ENTER)                   # 回车搜索
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(driver.page_source)                   # 拿到渲染后的源码
finally:
    driver.close()
```

## 8.14 实战：淘宝爬虫（Tb_spider）

淘宝必须登录、数据由 JS 渲染，requests 直接抓不到，需要 Selenium 复用登录态 + 把 `page_source` 交给 BeautifulSoup 解析 + JSON 落盘。

```python
import json
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class TbSpider:
    def __init__(self, keyword):
        options = ChromeOptions()
        options.add_argument(r'--user-data-dir=C:\path\to\your\chrome\profile')
        self.driver = webdriver.Chrome(options=options)
        self.keyword = keyword
        self.items = []

    def get_tb(self):
        """打开搜索页并翻页抓取"""
        url = f'https://s.taobao.com/search?q={self.keyword}'
        self.driver.get(url)
        # 简单翻页示例：滚动到底触发加载，实际项目按需循环
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        self.get_html()

    def get_html(self):
        """把 page_source 交给 BeautifulSoup 解析"""
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        # 注意类名不要带多余空格（源课件类名末尾多了一个空格）
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
    s = TbSpider('手机')
    s.run()
```

> **勘误：** 源 `Tb_spider.py` 有两处问题：① CSS 选择器 `.title--ASSt27UY `（类名末尾多了一个空格）会匹配失败，应去掉末尾空格；② `run()` 内直接调用全局 `s.get_tb()`/`s.get_html()`（隐式依赖 `if __name__ == '__main__'` 里的实例 `s`），应改为 `self.get_tb()` / `self.get_html()`。

> **注意：** 上述代码是教学骨架。真实淘宝有严格的反爬与登录校验，抓取请遵守目标网站的 robots 协议与相关法律法规，并控制频率。

## 记忆口诀

- **启动：** `webdriver.Chrome()` → `get(url)` → `page_source` → `close()`。
- **定位：** `find_element(By.ID/NAME/XPATH/TAG_NAME/CLASS_NAME/CSS_SELECTOR, ...)`，多元素用 `find_elements`。
- **链接定位：** `By.LINK_TEXT` 全等、`By.PARTIAL_LINK_TEXT` 部分匹配。
- **交互：** `send_keys` 输入、`clear` 清空、`click` 点击、`Keys.ENTER` 回车。
- **动作链：** `ActionChains(driver).drag_and_drop(A, B).perform()`。
- **切换：** `switch_to.frame` 进 iframe、`switch_to.window` 切标签页、`window_handles` 列窗口。
- **等待：** `WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'x')))`，定位参数是元组。
- **JS：** `execute_script('window.scrollTo(0, document.body.scrollHeight)')` 滚动到底。
- **反检测：** `ChromeOptions` 的 `excludeSwitches` + `useAutomationExtension=False` + `--user-data-dir` 复用登录态。
- **旧 API 已废：** `find_element_by_id` → `find_element(By.ID, ...)`；`PhantomJS` 已移除。

[← 上一篇：XPath解析](07-XPath解析.md) | [下一篇：反爬虫与应对 →](09-反爬虫与应对.md)
