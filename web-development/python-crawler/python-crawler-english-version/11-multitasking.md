[<- Previous: Captcha Recognition](10-captcha.md) | [Next: Scrapy Basics ->](12-scrapy-basics.md)

# 11 Multitasking Crawler

A crawler spends most of its time waiting for network responses, not computing. When you crawl serially in a single thread, the program idles on every request, and a few dozen pages can take minutes. Multitasking lets you fire multiple requests at once, overlapping the wait times and dramatically boosting throughput. This chapter is organized around four blocks: process/thread fundamentals, multiprocessing, asyncio coroutines + aiohttp, and inter-process communication with task-type selection.

## 11.1 Process and Thread Fundamentals

### 11.1.1 Process

A **process** is one execution of a program. When you run a `.py` file, the operating system allocates a private block of memory for it, including the address space, data stack, and other resources needed for execution. The OS manages all processes uniformly and fairly allocates CPU time among them.

The defining trait of a process is **isolation**: each process owns its own memory space, so processes **cannot share information directly**. They must exchange data through IPC (Inter-Process Communication) mechanisms.

### 11.1.2 Thread

A **thread** is a sub-task inside a process and the smallest unit of CPU scheduling. A process can contain many threads, which **share the process's runtime environment (memory, file handles, and so on)**.

Every thread's life cycle has three phases:

| Phase | Description |
|-------|-------------|
| Start | The thread is created and launched |
| Sequential execution | The thread's code runs |
| End | The code finishes and the thread exits |

While running, a thread may be **preempted (interrupted)** — the OS hands the CPU to another thread — or it may **suspend itself (sleep)** by yielding through operations like `sleep`, letting other threads run first.

### 11.1.3 Multi-process vs Multi-thread

| Aspect | Multi-process | Multi-thread |
|--------|---------------|--------------|
| Resource unit | The OS runs several tasks | One process does several things at once |
| Memory space | Independent, not shared | Shared within the process |
| Communication | Needs IPC (Queue, Pipe, etc.) | Shares variables directly (needs locks) |
| Stability | One crash does not affect others | One thread crash can kill the whole process |
| Best for | CPU-bound or isolated tasks | IO-bound, frequently interacting tasks |

Main benefits of multi-threading:

- **Run long tasks in the background:** the main thread keeps responding while a worker thread does the heavy lifting.
- **UI progress bars:** a worker thread runs the job while the main thread updates the progress bar without freezing the UI.
- **Possible speedup:** IO-bound tasks speed up through overlapped waiting (CPU-bound tasks are limited by the GIL).

### 11.1.4 Concurrency vs Parallelism

Two easily confused concepts:

| Concept | Definition | Intuition |
|---------|------------|-----------|
| Concurrency | Task count **exceeds** CPU cores; a single core rapidly rotates between tasks | Simultaneous at the macro level, interleaved at the micro level |
| Parallelism | Task count is **less than or equal to** CPU cores; multiple cores execute at once | Genuinely simultaneous |

> **Key idea:** Concurrency is "taking turns"; parallelism is "working together". A single-core CPU can still achieve concurrency (fast switching), but only a multi-core CPU can achieve true parallelism.

### 11.1.5 The GIL (Global Interpreter Lock)

The **GIL** is CPython's synchronization mechanism: **at any moment, only one thread executes**. Even if your machine has multiple CPU cores, CPython multi-threading allows only one thread to run bytecode at a time.

> **Key idea:** There is only one GIL. It prevents CPython threads from using multiple cores for CPU-bound work, but it barely matters for IO-bound tasks (threads release the GIL while waiting for IO).

The GIL also exists in other interpreters such as Ruby MRI. It is an interpreter-level lock, not a property of the Python language itself (PyPy and Jython have no GIL).

### 11.1.6 How Multi-threading Executes

In a multi-threaded environment, a thread's execution flow looks like this:

1. Set and acquire the GIL;
2. Run the thread that holds the lock;
3. Execute the designated bytecode, or the thread yields (`sleep`, etc.);
4. Put the thread to sleep;
5. Release the GIL; other threads repeat the cycle.

A thread without the GIL can only **wait** (if the lock-holding thread never releases, others "freeze"). This is why CPython multi-threading can actually be slower than single-threading on pure computation — context switching has its own overhead.

## 11.2 Multi-threading with `threading`

### 11.2.1 The `_thread` and `threading` Modules

Python provides two thread-related modules:

| Module | Role |
|--------|------|
| `_thread` | Low-level module with the most basic thread and lock support |
| `threading` | A wrapper around `_thread` offering higher-level, friendlier thread management |

In daily work you use `threading` directly and almost never touch `_thread`.

### 11.2.2 Creating Threads with `threading.Thread`

The core is `threading.Thread(target=function_name)`, then start it with `start()`:

```python
import threading
import time


def sing(n):
    for i in range(n):
        print('singing', i)
        time.sleep(0.1)   # sleep releases the GIL; good for IO-bound work


def dance(n):
    for i in range(n):
        print('dancing', i)
        time.sleep(0.1)


if __name__ == '__main__':
    # positional args go in a tuple
    t1 = threading.Thread(target=sing, args=(6,))
    # keyword args go in a dict
    t2 = threading.Thread(target=dance, kwargs={'n': 6})

    t1.start()   # start thread 1
    t2.start()   # start thread 2

    t1.join()    # wait for t1 to finish
    t2.join()    # wait for t2 to finish

    print('main thread done')
```

> **Note:** pass only the **function name** to `target`, never `sing()` (that calls the function and passes its return value). Arguments go through the `args` tuple or the `kwargs` dict — you can mix both.

### 11.2.3 Common Methods

| Method | Purpose |
|--------|---------|
| `threading.enumerate()` | Get a **list** of all current thread objects |
| `threading.current_thread()` | Get the **current** thread object |
| `Thread.start()` | Start the thread |
| `Thread.join()` | Block until the thread finishes |
| `Thread.name` | Thread name (defaults `Thread-1`, `Thread-2`, ...) |

```python
import threading
import time


def worker():
    print('current thread:', threading.current_thread().name)
    time.sleep(1)


if __name__ == '__main__':
    threads = [threading.Thread(target=worker) for _ in range(3)]
    for t in threads:
        t.start()
    print('active thread count:', len(threading.enumerate()))
    for t in threads:
        t.join()
```

### 11.2.4 Custom Thread Class

Instead of passing a `target` function, you can **subclass `threading.Thread` and override `run()`**, wrapping the thread's logic into a class:

```python
import threading
import time


class SingThread(threading.Thread):
    def __init__(self, n):
        super().__init__()   # must call the parent __init__ first
        self.n = n

    def run(self):           # called automatically once the thread starts
        for i in range(self.n):
            print('singing', i)
            time.sleep(0.1)


if __name__ == '__main__':
    t = SingThread(5)
    t.start()   # start() internally calls our overridden run()
    t.join()
    print('done')
```

> **Key idea:** in a custom thread class, put the logic in `run()` but still start it with `start()` (never call `run()` directly — that would just run it as a normal function without a new thread).

## 11.3 Multi-processing with `multiprocessing`

### 11.3.1 The `Pool` Process Pool

Multi-processing uses the `multiprocessing` module. `Pool(4)` declares a process pool with four worker processes; you hand tasks to the pool and it schedules them onto idle processes:

```python
from multiprocessing import Pool
import time


def down(n):
    time.sleep(2)          # simulate a slow task
    return n * n


if __name__ == '__main__':
    pool = Pool(4)         # create 4 worker processes
    # submit 12 tasks asynchronously
    results = [pool.apply_async(down, args=(i,)) for i in range(12)]
    pool.close()           # close the pool: no new tasks accepted
    pool.join()            # block until all tasks finish
    out = [r.get() for r in results]   # collect each result
    print(out)
```

> **Note:** multi-processing code must be inside `if __name__ == '__main__':`, otherwise child processes recursively re-import and re-run the code and crash (especially strict on Windows).

### 11.3.2 Synchronous vs Asynchronous Submission

`Pool` offers two ways to submit a task:

| Method | Mode | Return value |
|--------|------|--------------|
| `apply(func, args)` | **Synchronous**: blocks until the task completes | The result directly |
| `apply_async(func, args)` | **Asynchronous**: returns immediately after submitting | An `AsyncResult`; call `.get()` for the result |

Supporting methods:

- `close()`: close the pool — no more task requests are accepted;
- `join()`: block until every task in the pool finishes.

Real crawlers almost always use `apply_async` so tasks run concurrently instead of queuing one by one.

### 11.3.3 Sharing a Queue with `Manager.Queue`

Child processes have **independent memory spaces**, so ordinary variables cannot be shared across processes. To have children report results back to the main process, use `multiprocessing.Manager().Queue()` to create a **cross-process shared queue**: children call `q.put()`, and the main process calls `q.get()` to collect everything:

```python
from multiprocessing import Pool, Manager


def worker(i, q):
    q.put(i * 2)           # child writes into the shared queue


if __name__ == '__main__':
    m = Manager()
    q = m.Queue()          # cross-process shared queue

    pool = Pool(4)
    for i in range(10):
        pool.apply_async(worker, args=(i, q))
    pool.close()
    pool.join()

    # after all tasks finish, drain by the known count
    data = [q.get() for _ in range(10)]
    print(data)            # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

> **Correction:** the source slides used `while not q.empty()` to drain the queue — in a multi-process queue, `empty()` is **unreliable** (a sync delay between processes can make it falsely report empty). The correct approach: if you know the count, drain by count; otherwise use a sentinel value (children `put(None)` when done) or `q.get(timeout=...)`.

## 11.4 asyncio Coroutines + aiohttp

### 11.4.1 Coroutine Concepts

A **coroutine** is sometimes called a "micro-thread". The hierarchy is: **process > thread > coroutine**.

| Aspect | Process / thread | Coroutine |
|--------|------------------|-----------|
| Managed by | The operating system | **The user (program)** |
| Switch cost | Large (kernel-mode switch) | Tiny (user-mode switch) |
| GIL | Limited by the GIL | asyncio is not managed by the GIL, so it runs faster |
| Count | Limited (heavy resources) | Thousands can be created easily |

Three key terms:

| Term | Meaning |
|------|---------|
| `coroutine` | A coroutine object, defined with `async def` |
| `task` | A task wrapping a coroutine, carrying its running state |
| `future` | A future (not-yet-run) task, representing the eventual result of an async operation |

### 11.4.2 Core asyncio API

Define coroutines with `async def`, wait with `await`, and sleep asynchronously with `asyncio.sleep()` (which does not block the event loop):

```python
import asyncio
import time


async def fetch(url):
    print('fetching:', url)
    await asyncio.sleep(2)      # async wait; does not block the event loop
    print('done:', url)


async def main():
    urls = ['a.com', 'b.com', 'c.com']
    # wrap coroutines into tasks (two equivalent ways)
    tasks = [asyncio.ensure_future(fetch(u)) for u in urls]
    await asyncio.gather(*tasks)   # run all tasks concurrently


start = time.time()
asyncio.run(main())                # modern entry point (replaces deprecated get_event_loop)
print('elapsed:', round(time.time() - start, 2), 's')   # about 2s, not 6s
```

Common API reference:

| API | Purpose |
|-----|---------|
| `async def` | Define a coroutine function |
| `await` | Block until an async operation completes |
| `asyncio.sleep(n)` | Sleep n seconds asynchronously |
| `asyncio.ensure_future(coro)` / `loop.create_task(coro)` | Wrap a coroutine into a task |
| `asyncio.gather(*tasks)` | Run multiple tasks concurrently, returning a list of results |
| `asyncio.run(main())` | Entry point (Python 3.7+) |

> **Correction:** the source slides used the deprecated `asyncio.get_event_loop()` and `loop.run_until_complete()`. Since Python 3.10 `get_event_loop()` is deprecated, and in 3.12 it raises `RuntimeError` when no loop is running. The modern style is `asyncio.run(main())` as the entry point and `asyncio.gather(*tasks)` instead of `asyncio.wait(task_list)`.
>
> Another common mistake is a comment reading `pip install asyncio` — **asyncio is part of the standard library** and needs no installation.

### 11.4.3 Asynchronous Requests with aiohttp

`requests` is synchronous, so inside coroutines you need the async HTTP library **aiohttp**:

```bash
pip install aiohttp
```

```python
import asyncio
import aiohttp


async def get(url, session):
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.text()   # fetch response text asynchronously
        return None


async def main():
    urls = ['https://example.com', 'https://example.org']
    # create one session outside and reuse it for all requests
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(get(u, session)) for u in urls]
        return await asyncio.gather(*tasks)


results = asyncio.run(main())
for r in results:
    print(r[:60] if r else 'request failed')
```

> **Key idea:** `aiohttp.ClientSession()` is an async session and is expensive to create; reuse **one session** for the whole task instead of opening `async with aiohttp.ClientSession()` for every request.
>
> **Correction:** in the source slides, `get_data` created a new session per request, and `save_data` used the synchronous `open().write()` to save files — synchronous IO blocks the event loop. The better approach is to reuse the session, and write files with `aiofiles` or `loop.run_in_executor` to offload blocking work to a thread pool.

### 11.4.4 Synchronous vs Asynchronous Page Loading

A crawler receives web data in one of three ways, and identifying which affects your parsing strategy:

| Return mode | Feature | Handling |
|-------------|---------|----------|
| Direct HTML text | Data is already in the HTML | `requests` + parser (XPath/BS4/regex) |
| Ajax async loading | Data usually arrives as JSON | Find the XHR endpoint and request the JSON directly |
| JS rendering | Returns JSON/placeholder; the page is built by JS | Selenium / reverse-engineer the JS |

A trick for pagination: **if the refresh button moves when you paginate, the page loads synchronously (look for the "all" data package); if it stays still, it loads asynchronously (look for the XHR request)**. JSON parsing is covered in Chapter 05 (JsonPath) and saving to Excel in Chapter 06 (data persistence).

## 11.5 Inter-process Communication and Task Selection

### 11.5.1 IO-bound vs CPU-bound

The key to choosing is identifying the task type:

| Task type | Bottleneck | Recommended | Why |
|-----------|------------|-------------|-----|
| IO-bound (network, file IO) | Waiting on IO | **Threads / coroutines** | GIL is released while waiting, so waits overlap |
| CPU-bound (heavy computation) | CPU | **Multi-process** | Multi-process bypasses the GIL and truly uses multiple cores |

Most crawlers are **IO-bound** (waiting for network responses), so threads and coroutines are the workhorses; multi-process comes in only for heavy CPU work such as encryption/decryption or image processing.

### 11.5.2 Selection Summary

| Option | Strengths | Weaknesses | Typical use |
|--------|-----------|------------|-------------|
| `threading` | Simple, easy data sharing | GIL-limited; too many threads add switch overhead | Small-to-medium crawlers with simple logic |
| `multiprocessing` | Bypasses GIL, uses cores, isolated and stable | Heavy resources; needs IPC | CPU-bound or isolated tasks |
| `asyncio` | Huge concurrency in one thread, tiny overhead | Needs async libraries (aiohttp, ...); steeper learning curve | Large-scale, high-concurrency IO-bound crawling |

For **inter-process communication**, `multiprocessing` offers `Manager().Queue()` (shared queue) and `Pipe`; coroutines cooperate through `await` and `asyncio.Queue`. Choose first by task type, then weigh team familiarity and code complexity.

**Summary Mnemonic**

- **Process vs thread** = "A process is a house, threads are the people in it; houses are independent, people share."
- **Concurrency vs parallelism** = "Concurrency is taking turns; parallelism is working together."
- **GIL** = "There is only one lock; CPython runs one thread at a time."
- **Selection** = "IO-bound: threads/coroutines; CPU-bound: multi-process."
- **asyncio** = "`async def` defines, `await` waits, `asyncio.run()` enters, aiohttp makes async requests."

[<- Previous: Captcha Recognition](10-captcha.md) | [Next: Scrapy Basics ->](12-scrapy-basics.md)
