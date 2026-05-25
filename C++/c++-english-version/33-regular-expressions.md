[← Previous: Multi-Threading](32-multi-threading.md) | [Next: C++20 Features →](34-cpp20-features.md)

# 33 Regular Expressions

The `<regex>` library (C++11) provides pattern matching for strings — useful for validation, parsing, and text extraction.

## 33.1 Basic Syntax

### 33.1.1 Creating a Regex Object

```cpp
#include <regex>
#include <string>

std::regex email_pattern(R"([\w\.-]+@[\w\.-]+\.\w+)");
```

> **Tip:** Use raw string literals `R"(...)`" to avoid escaping backslashes.

### 33.1.2 Common Regex Patterns

| Pattern | Matches |
|---------|---------|
| `\d` | Any digit `[0-9]` |
| `\w` | Any word character `[a-zA-Z0-9_]` |
| `\s` | Any whitespace |
| `.` | Any character (except newline) |
| `*` | Zero or more of preceding |
| `+` | One or more of preceding |
| `?` | Zero or one of preceding |
| `^` | Start of string |
| `$` | End of string |
| `[abc]` | Any character in set |
| `(a\|b)` | a or b |

## 33.2 Matching and Searching

### 33.2.1 `std::regex_match` — Full String Match

```cpp
std::regex digit_pattern(R"(^\d+$)");

std::regex_match("12345", digit_pattern);  // true
std::regex_match("12a45", digit_pattern);  // false — 'a' breaks the match
```

### 33.2.2 `std::regex_search` — Partial Match

```cpp
std::regex word_pattern(R"(\b\w{5,}\b)");  // Words with 5+ letters

std::string text = "The quick brown fox";
std::smatch match;

if (std::regex_search(text, match, word_pattern)) {
    std::cout << match[0];  // "quick" — first match found
}
```

### 33.2.3 `std::regex_replace` — Substitution

```cpp
std::string phone = "Call me at 123-456-7890";
std::regex phone_pattern(R"(\d{3}-\d{3}-\d{4})");

std::string result = std::regex_replace(phone, phone_pattern, "XXX-XXX-XXXX");
// Result: "Call me at XXX-XXX-XXXX"
```

## 33.3 Capturing Groups

Extract specific parts of a match using parentheses:

```cpp
std::regex date_pattern(R"((\d{4})-(\d{2})-(\d{2}))");
std::string date_str = "2024-03-15";
std::smatch match;

if (std::regex_match(date_str, match, date_pattern)) {
    std::cout << "Year: " << match[1];   // "2024"
    std::cout << "Month: " << match[2];  // "03"
    std::cout << "Day: " << match[3];    // "15"
}
```

## 33.4 Iterating Over All Matches

```cpp
std::string text = "Emails: alice@example.com, bob@test.org";
std::regex email_pattern(R"([\w\.-]+@[\w\.-]+\.\w+)");

auto begin = std::sregex_iterator(text.begin(), text.end(), email_pattern);
auto end = std::sregex_iterator();

for (auto it = begin; it != end; ++it) {
    std::cout << (*it)[0] << "\n";  // alice@example.com, then bob@test.org
}
```

## 33.5 Regex Flags

```cpp
std::regex pattern("hello", std::regex::icase);  // Case-insensitive match
std::regex_match("HELLO", pattern);              // true
```

| Flag | Effect |
|------|--------|
| `std::regex::icase` | Case-insensitive matching |
| `std::regex::optimize` | Optimize for repeated matching (slower construction) |
| `std::regex::ECMAScript` | Default syntax (most flexible) |

## 33.6 Summary

| Task | Function |
|------|----------|
| Does entire string match pattern? | `std::regex_match` |
| Does pattern appear anywhere in string? | `std::regex_search` |
| Replace all matches with new text | `std::regex_replace` |
| Extract all matches iteratively | `std::sregex_iterator` |
| Extract sub-patterns | Capturing groups `()` + `match[n]` |

> **Key Concept:** Regular expressions are powerful but can be slow for complex patterns. For simple tasks (e.g., checking if a string starts with a prefix), prefer string methods like `starts_with()` (C++20) or `find()`.
