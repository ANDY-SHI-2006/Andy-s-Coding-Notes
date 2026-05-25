[← Previous: Regular Expressions](33-regular-expressions.md) | [Return to Index](README.md)

# 34 C++20 Features

C++20 is a major release that brings significant quality-of-life improvements. This chapter covers the most impactful features for day-to-day programming.

## 34.1 The Spaceship Operator `<=>`

### 34.1.1 Three-Way Comparison

The spaceship operator replaces all six comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`) with a single declaration:

```cpp
struct Point {
    int x, y;
    auto operator<=>(const Point&) const = default;  // Generates all 6 comparisons
};

Point a{1, 2}, b{3, 4};
a < b;   // true
a == b;  // false
a >= b;  // false
```

The operator returns one of three values:
- `std::strong_ordering::less` — left < right
- `std::strong_ordering::equal` — left == right
- `std::strong_ordering::greater` — left > right

> **See also:** Chapter 30 (OOP Advanced) for custom `operator<=>` implementations.

## 34.2 Ranges (`<ranges>`)

### 34.2.1 Pipeline-Style Operations

Ranges bring lazy, composable algorithms similar to Python generators or LINQ:

```cpp
#include <ranges>
#include <vector>
#include <iostream>

std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

auto result = nums
    | std::views::filter([](int n) { return n % 2 == 0; })  // Keep evens
    | std::views::transform([](int n) { return n * n; })    // Square them
    | std::views::take(3);                                   // First 3 only

for (int n : result) {
    std::cout << n << " ";  // 4 16 36
}
```

> **Key Point:** Ranges are **lazy** — no computation happens until you iterate. The pipeline is evaluated on-demand.

### 34.2.2 Common Range Views

| View | Purpose |
|------|---------|
| `views::filter(pred)` | Keep elements satisfying predicate |
| `views::transform(fn)` | Apply function to each element |
| `views::take(n)` | First n elements |
| `views::drop(n)` | Skip first n elements |
| `views::reverse` | Iterate in reverse order |
| `views::iota(start, end)` | Generate sequence [start, end) |

## 34.3 Coroutines

### 34.3.1 Suspendable Functions

Coroutines are functions that can suspend execution and resume later — useful for generators, async I/O, and lazy evaluation:

```cpp
#include <coroutine>

// A simple generator coroutine
generator<int> count_up_to(int n) {
    for (int i = 0; i < n; ++i) {
        co_yield i;  // Suspend, return value, resume on next call
    }
}

for (int value : count_up_to(5)) {
    std::cout << value << " ";  // 0 1 2 3 4
}
```

> **Caution:** Coroutines are powerful but complex. The compiler transforms `co_await`, `co_yield`, and `co_return` into state machine code. For most use cases, `std::async` or ranges are simpler alternatives.

## 34.4 Designated Initializers

C++20 brings C-style designated initializers — explicit, order-independent struct initialization:

```cpp
struct Config {
    int width = 1920;
    int height = 1080;
    bool fullscreen = false;
};

Config cfg = {
    .width = 2560,
    .height = 1440,
    .fullscreen = true
};
```

> **Advantage:** Code is self-documenting. You see the field name at the initialization site, not just the value.

## 34.5 `std::format`

Python-style formatting comes to C++:

```cpp
#include <format>

std::string msg = std::format("Hello, {}! You have {} messages.", "Alice", 5);
// "Hello, Alice! You have 5 messages."

std::string hex = std::format("0x{:08X}", 255);  // "0x000000FF"
std::string pi = std::format("{:.2f}", 3.14159); // "3.14"
```

| Format | Result |
|--------|--------|
| `{:d}` | Integer |
| `{:f}` | Fixed-point float |
| `{:e}` | Scientific notation |
| `{:x}` / `{:X}` | Hexadecimal |
| `{:08d}` | Zero-padded, 8 digits |
| `{:.2f}` | 2 decimal places |

> **Note:** `std::format` is defined in `<format>` (C++20). As of early 2024, compiler support is still maturing — `fmt::format` from the {fmt} library is a widely used pre-standard alternative.

## 34.6 Modules (Preview)

Modules replace `#include` with a faster, more robust import system:

```cpp
// math.ixx — module interface unit
export module math;

export int square(int x) { return x * x; }

// main.cpp — module consumer
import math;

int main() {
    std::cout << square(5);  // 25
}
```

| `#include` | `import` |
|-----------|---------|
| Textual substitution | Compiled binary interface |
| Slow (re-parse headers) | Fast (no re-parsing) |
| Macros leak | No macro leakage |
| Fragile (include order matters) | Order-independent |

> **Status:** Modules are a major long-term improvement, but tooling (build systems, IDE support) is still catching up as of 2024.

## 34.7 Summary

| Feature | What It Solves | When to Use |
|---------|---------------|-------------|
| `<=>` | Boilerplate of 6 comparison operators | Any class that needs ordering |
| Ranges | Composable, lazy data processing | Pipeline-style transformations |
| Coroutines | Suspendable/resumable functions | Generators, async state machines |
| Designated initializers | Self-documenting struct initialization | Structs with many optional fields |
| `std::format` | Type-safe, readable string formatting | Any formatted output |
| Modules | Faster builds, no macro leakage | Large projects (tooling permitting) |

> **Key Concept:** C++20 doesn't add features you couldn't do before — it makes common patterns **shorter, safer, and faster to compile**. The spaceship operator and ranges alone eliminate hundreds of lines of boilerplate in a typical codebase.
