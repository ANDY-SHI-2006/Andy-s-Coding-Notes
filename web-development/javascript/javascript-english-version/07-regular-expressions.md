[<- Previous: classes and storage](06-classes-and-storage.md) | [Next: data fetching ->](08-data-fetching.md)

# 7 Strings, Arrays, Dates, and Regular Expressions

Core built-in objects and methods for manipulating text, collections, time, and pattern matching.

## 7.1 String Methods

### 7.1.1 Reading and Searching

```javascript
let text = "Hello, World!";

text.length;                       // 13
text[0];                           // "H"
text.charAt(0);                    // "H"
text.charCodeAt(0);                // 72 (Unicode code point)
String.fromCharCode(72, 105);      // "Hi"

text.indexOf("World");             // 7  (first occurrence)
text.indexOf("o", 8);              // 10 (start searching from index 8)
text.lastIndexOf("l");             // 10 (last occurrence)
text.includes("World");            // true
text.startsWith("Hello");          // true
text.endsWith("!");                // true

text.concat(" ", "Again");         // "Hello, World! Again" (returns new string)
```

### 7.1.2 Extracting Substrings

```javascript
let text = "Hello, World!";

text.slice(0, 5);         // "Hello" (start, end)
text.slice(7);            // "World!" (start to end)
text.slice(-6);           // "World!" (negative = from end)

text.substring(0, 5);     // "Hello" (start, end)
text.substring(5, 0);     // "Hello" (auto-swaps when start > end)
text.substr(7, 5);        // "World" (start, length) — deprecated
```

> **Note:** `substring` treats negative values as `0` and swaps the arguments if `start > end`. `substr(start, length)` is deprecated; prefer `slice` in new code.

### 7.1.3 Modifying Strings

```javascript
let text = "  Hello, World!  ";

text.trim();              // "Hello, World!" (remove whitespace both ends)
text.trimStart();         // "Hello, World!  "
text.trimEnd();           // "  Hello, World!"

text.toUpperCase();       // "  HELLO, WORLD!  "
text.toLowerCase();       // "  hello, world!  "

text.replace("World", "JavaScript");   // "  Hello, JavaScript!  "
text.replaceAll("l", "L");             // "  HeLLo, WorLd!  "
```

### 7.1.4 Splitting and Joining

```javascript
let csv = "Alice,25,Engineer";
let parts = csv.split(",");            // ["Alice", "25", "Engineer"]
let limited = csv.split(",", 2);       // ["Alice", "25"] (limit fragments)

let words = "Hello World".split(" ");  // ["Hello", "World"]
let chars = "ABC".split("");           // ["A", "B", "C"]

// Join array back to string
let joined = ["Hello", "World"].join(" ");  // "Hello World"
```

### 7.1.5 Template Literals

```javascript
let name = "Alice";
let age = 25;

// Backtick strings support interpolation and multiline
let message = `Hello, ${name}! You are ${age} years old.`;

let html = `
    <div>
        <h1>${name}</h1>
        <p>Age: ${age}</p>
    </div>
`;
```

### 7.1.6 Formatting Numbers

`Number.prototype.toFixed` returns a string with a fixed number of decimal places.

```javascript
let pi = 3.14159;

pi.toFixed(2);        // "3.14"
pi.toFixed(0);        // "3"
(2.5).toFixed(1);     // "2.5"
```

> **Caution:** `toFixed` rounds and always returns a **string**. Convert back with `Number()` or `parseFloat()` if you need to calculate further.

---

## 7.2 Array Methods

### 7.2.1 Reading and Searching

```javascript
let arr = ["Alice", "Bob", "Carol"];

arr.length;                    // 3
arr[0];                        // "Alice"
arr.indexOf("Bob");            // 1
arr.includes("Bob");           // true
arr.find(item => item.startsWith("C"));     // "Carol"
arr.findIndex(item => item === "Bob");      // 1
```

### 7.2.2 Adding and Removing

```javascript
let arr = [1, 2, 3];

let len1 = arr.push(4);     // 4 — new length; arr is now [1, 2, 3, 4]
let last = arr.pop();       // 4 — removed element; arr is now [1, 2, 3]
let len2 = arr.unshift(0);  // 4 — new length; arr is now [0, 1, 2, 3]
let first = arr.shift();    // 0 — removed element; arr is now [1, 2, 3]

arr.splice(1, 1);       // [1, 3] — remove 1 item at index 1
arr.splice(1, 0, "a");  // [1, "a", 3] — insert at index 1
arr.splice(1, 1, "b");  // [1, "b", 3] — replace at index 1
```

### 7.2.3 Iteration

```javascript
let numbers = [1, 2, 3, 4, 5];

// Higher-order callbacks receive (currentValue, index, array)
numbers.forEach((num, i, arr) => console.log(num, i));

// map — transform each element, return new array
let doubled = numbers.map((num, i, arr) => num * 2);    // [2, 4, 6, 8, 10]

// filter — keep elements that pass the test
let evens = numbers.filter((num, i, arr) => num % 2 === 0);  // [2, 4]

// reduce — reduce to a single value
// Callback signature: (accumulator, currentValue, index, array)
let sum = numbers.reduce((acc, cur, idx, arr) => acc + cur, 0);  // 15

// some — does ANY element pass?
let hasEven = numbers.some((num, i, arr) => num % 2 === 0);   // true

// every — do ALL elements pass?
let allPositive = numbers.every((num, i, arr) => num > 0);    // true
```

> **Note:** `forEach` cannot be interrupted with `break` or `continue`. Use a regular `for` loop or `some`/`find` when you need early exit.

### 7.2.4 Other Useful Methods

```javascript
let arr = [3, 1, 4, 1, 5];

// Sort comparison: < 0 → a first; > 0 → b first; 0 → keep order
arr.sort((a, b) => a - b);     // [1, 1, 3, 4, 5] — numeric sort
arr.reverse();                  // [5, 4, 3, 1, 1]
arr.concat([9, 2]);             // [5, 4, 3, 1, 1, 9, 2]
arr.slice(1, 3);                // [4, 3] — extract portion
arr.join("-");                  // "5-4-3-1-1"

Array.isArray(arr);             // true
Array.from("ABC");              // ["A", "B", "C"] (array-like/iterable → array)
Array.from({length: 3}, (_, i) => i); // [0, 1, 2]
```

> **Important:** `sort()` and `reverse()` modify the original array. Use `slice()` first if you need to preserve the original.

```javascript
// Create a sorted copy without modifying original
let sorted = [...arr].sort((a, b) => a - b);
```

---

## 7.3 Dates

### 7.3.1 Creating Dates

```javascript
let now = new Date();                    // Current date and time
let specific = new Date("2024-12-25");   // From string
let fromNumbers = new Date(2024, 11, 25, 10, 30, 0);  // Year, Month(0-11), Day...
let fromTimestamp = new Date(1703502600000);  // From milliseconds
```

### 7.3.2 Reading Date Components

```javascript
let date = new Date();

date.getFullYear();       // 2024
date.getMonth();          // 0-11 (0 = January)
date.getDate();           // 1-31
date.getDay();            // 0-6 (0 = Sunday)
date.getHours();          // 0-23
date.getMinutes();        // 0-59
date.getSeconds();        // 0-59
date.getMilliseconds();   // 0-999
date.getTime();           // Timestamp in milliseconds since 1970-01-01
```

### 7.3.3 Formatting Dates

```javascript
let date = new Date();

// Human-readable formats
date.toDateString();                // "Wed Dec 25 2024"
date.toTimeString();                // "10:30:00 GMT+0800 (...)"
date.toUTCString();                 // "Wed, 25 Dec 2024 02:30:00 GMT"

// Locale-specific formatting
date.toLocaleDateString("en-US");   // "12/25/2024"
date.toLocaleDateString("zh-CN");   // "2024/12/25"
date.toLocaleTimeString("en-US");   // "10:30:00 AM"
date.toLocaleString("zh-CN");       // "2024/12/25 10:30:00"

// ISO format
date.toISOString();                 // "2024-12-25T10:30:00.000Z"
```

### 7.3.4 Date Calculations

```javascript
let date = new Date();

date.setDate(date.getDate() + 7);     // Add 7 days
date.setMonth(date.getMonth() + 1);   // Add 1 month

date.setHours(date.getHours() + 3);   // Add 3 hours

// Difference between two dates
let d1 = new Date("2024-01-01");
let d2 = new Date("2024-12-31");
let diff = d2 - d1;                   // Milliseconds
let days = diff / (1000 * 60 * 60 * 24);  // Convert to days
```

### 7.3.5 Timestamps

Three common ways to get the current timestamp in milliseconds:

```javascript
Date.now();                 // Static method (preferred)
new Date().getTime();       // From a Date instance
+new Date();                // Unary plus coerces Date to number
```

### 7.3.6 Case Snippet: Countdown

Convert a second difference into days, hours, minutes, and seconds with zero-padding.

```javascript
function countdown(targetDate) {
  let diff = Math.max(0, Math.floor((targetDate - Date.now()) / 1000));
  let d = Math.floor(diff / 86400);
  let h = Math.floor((diff / 3600) % 24);
  let m = Math.floor((diff / 60) % 60);
  let s = diff % 60;
  let pad = n => (n < 10 ? "0" + n : n);
  return `${pad(d)}d ${pad(h)}h ${pad(m)}m ${pad(s)}s`;
}

setInterval(() => console.log(countdown(new Date("2025-01-01"))), 1000);
```

- Use `Date.now()` to get the current timestamp.
- Divide by `1000` first, then use `/ 86400`, `/ 3600 % 24`, `/ 60 % 60`, `% 60`.
- Pad single digits with `"0" + n` or `String(n).padStart(2, "0")`.

---

## 7.4 Regular Expressions

Regular expressions (regex) define patterns for searching and manipulating text.

### 7.4.1 Creating a Regex

```javascript
let pattern1 = /abc/;           // Literal syntax
let pattern2 = new RegExp("abc"); // Constructor syntax
```

### 7.4.2 Common Patterns

| Pattern | Matches |
|---------|---------|
| `.` | Any single character except newline |
| `\d` | Any digit (0-9) |
| `\w` | Any word character (a-z, A-Z, 0-9, _) |
| `\s` | Any whitespace |
| `^` | Start of string |
| `$` | End of string |
| `[abc]` | Any character in the set (a, b, or c) |
| `[^abc]` | Any character NOT in the set |
| `a\|b` | a or b |
| `a*` | Zero or more a |
| `a+` | One or more a |
| `a?` | Zero or one a |
| `a{3}` | Exactly 3 a's |
| `a{2,4}` | 2 to 4 a's |
| `a{2,}` | 2 or more a's |
| `[\u4e00-\u9fa5]` | Any common Chinese character |

> **Escaping:** In regex literals, these characters must be escaped with `\` when you mean the literal character: `(`, `)`, `[`, `]`, `{`, `}`, `^`, `$`, `*`, `?`, `\`, `|`, `+`, `.`. Inside a character class `[...]`, only `\`, `]`, `^` (if first), and `-` (between two chars) usually need escaping.

### 7.4.3 Regex Methods

```javascript
let text = "My email is alice@example.com";
let emailPattern = /\w+@\w+\.\w+/;

// test — does the string match?
emailPattern.test(text);        // true

// match — return matches
let match = text.match(emailPattern);   // ["alice@example.com"]

// matchAll — return all matches (with capture groups)
let text2 = "Prices: $10, $20, $30";
let matches = [...text2.matchAll(/\$(\d+)/g)];
// [["$10", "10"], ["$20", "20"], ["$30", "30"]]

// exec — returns a result array with captured groups, updates lastIndex when global
let numberPattern = /(\d{3})-(\d{4})/g;
let result = numberPattern.exec("Tel: 123-4567, 999-8888");
// result[0] = "123-4567", result[1] = "123", result[2] = "4567"

// RegExp.$1 ~ $9 store the last match's capture groups (legacy but still supported)
/^(\d{4})-(\d{2})-(\d{2})$/.test("2024-12-25");
RegExp.$1;   // "2024"
RegExp.$2;   // "12"
RegExp.$3;   // "25"

// replace — replace matches
text.replace(emailPattern, "[hidden]");
// "My email is [hidden]"

// search — find index of first match
text.search(emailPattern);      // 12

// split — split by pattern
"a,b;c".split(/[,;]/);          // ["a", "b", "c"]
```

### 7.4.4 Flags

```javascript
/abc/g    // g = global (find all matches)
/abc/i    // i = ignore case
/abc/m    // m = multiline (^ and $ match line boundaries)
/abc/s    // s = dotall (. matches newlines)
/abc/u    // u = unicode
/abc/y    // y = sticky (match only from lastIndex)
```

### 7.4.5 Common Regex Examples

```javascript
// Email (simplified)
/^\w+@\w+\.\w+$/

// Phone number (e.g., 123-456-7890)
/^\d{3}-\d{3}-\d{4}$/

// URL
/^https?:\/\/.+/

// Strong password (8+ chars, uppercase, lowercase, digit)
/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
```

### 7.4.6 Lookahead and Lookbehind

Assertions match a position, not a character.

| Pattern | Name | Meaning |
|---------|------|---------|
| `(?=...)` | Positive lookahead | followed by `...` |
| `(?!...)` | Negative lookahead | NOT followed by `...` |
| `(?<=...)` | Positive lookbehind | preceded by `...` |
| `(?<!...)` | Negative lookbehind | NOT preceded by `...` |

```javascript
let price = "$100";
/\d+(?=\s*USD)/.test(price);      // false (no "USD" after)
/(?<=\$)\d+/.exec(price);          // ["100"] (preceded by $)
```

### 7.4.7 Greedy vs Lazy Quantifiers

By default, quantifiers are **greedy** (match as much as possible). Add `?` to make them **lazy** (match as little as possible).

```javascript
let html = "<div>one</div><div>two</div>";

html.match(/<div>.*<\/div>/);      // greedy — "<div>one</div><div>two</div>"
html.match(/<div>.*?<\/div>/);     // lazy — "<div>one</div>"
```

| Greedy | Lazy |
|--------|------|
| `+` | `+?` |
| `*` | `*?` |
| `?` | `??` |
| `{n,m}` | `{n,m}?` |

### 7.4.8 Case Snippets

**Text find and highlight**

Wrap every occurrence of a keyword in a `<span>`.

```javascript
const input = document.querySelector("#search");
const box = document.querySelector("#text");

input.addEventListener("input", () => {
  let keyword = input.value.trim();
  if (!keyword) return;
  let pattern = new RegExp(`(${keyword})`, "gi");
  box.innerHTML = box.textContent.replace(pattern, '<span class="highlight">$1</span>');
});
```

- Build the pattern with `RegExp` when the keyword is dynamic.
- Use `$1` in `replace` to insert the captured keyword.
- Remember to sanitize user input if the keyword may contain regex metacharacters.

**Registration form validation**

Validate username, phone, and password on `blur`.

```javascript
const rules = {
  username: /^[a-zA-Z0-9_]{4,16}$/,
  phone: /^1[3-9]\d{9}$/,
  password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
};

function validate(field) {
  let ok = rules[field.name].test(field.value);
  field.nextElementSibling.style.display = ok ? "none" : "block";
}

document.querySelectorAll("input[data-rule]").forEach(input => {
  input.addEventListener("blur", () => validate(input));
});
```

- One regex per field keeps the logic readable.
- Show/hide an error tip next to the input.

---

## 7.5 Math

`Math` is a built-in object that holds numeric constants and utility functions. It is not a constructor.

```javascript
Math.PI;            // 3.141592653589793
Math.E;             // 2.718281828459045

Math.abs(-5);       // 5
Math.ceil(2.1);     // 3
Math.floor(2.9);    // 2
Math.round(2.5);    // 3
Math.trunc(2.9);    // 2 (integer part; prefer over `~~`, which is limited to 32-bit)

Math.max(1, 5, 3);          // 5
Math.max(...[1, 5, 3]);     // 5 (spread an array)
Math.min(1, 5, 3);          // 1

Math.pow(2, 3);     // 8
Math.sqrt(16);      // 4
Math.cbrt(27);      // 3

Math.random();      // 0 <= x < 1
```

Random integer in the inclusive range `[min, max]`:

```javascript
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
```

### 7.5.1 Case Snippet: Random Background Color

```javascript
function randomColor() {
  let r = Math.floor(Math.random() * 256);
  let g = Math.floor(Math.random() * 256);
  let b = Math.floor(Math.random() * 256);
  return `rgb(${r}, ${g}, ${b})`;
}

document.body.style.backgroundColor = randomColor();
```

- `Math.random() * 256` produces a value in `[0, 256)`.
- `Math.floor` turns it into an integer `0-255`.

---

## 7.6 Destructuring Assignment

Destructuring unpacks values from arrays or properties from objects into distinct variables.

```javascript
// Array destructuring
let [a, b] = [1, 2];
let [first, , third] = [1, 2, 3];     // skip the second item
let [head, ...tail] = [1, 2, 3, 4];   // rest collects remaining items

// Default values
let [x = 0, y = 0] = [10];            // x = 10, y = 0

// Object destructuring
let { name, age } = { name: "Alice", age: 25 };
let { name: userName } = { name: "Alice" }; // rename variable

// Nested destructuring
let user = { profile: { score: 90 } };
let { profile: { score } } = user;    // score = 90

// Function parameter destructuring with defaults
function greet({ name = "Guest", age = 0 } = {}) {
  return `Hello, ${name}, age ${age}`;
}
greet({ name: "Bob" });               // "Hello, Bob, age 0"
```

- Array destructuring is positional; object destructuring matches property names.
- Use defaults to avoid `undefined` when a value is missing.
- Rest patterns (`...rest`) collect remaining items into a real array.

---

## 7.7 Best Practices

| Do | Don't |
|----|-------|
| Use `slice` instead of `substr` (deprecated) | Use `substr` in new code |
| Use `===` with `indexOf` results (`!== -1`) | Forget that `indexOf` returns `-1` when not found |
| Use spread `[...arr]` before `sort`/`reverse` if you need original | Mutate original arrays unintentionally |
| Use `toLocaleDateString` for user-facing dates | Use `toString()` for user-facing dates (format varies) |
| Test regex patterns with tools like regex101.com | Write complex regex without testing |
| Use `map`/`filter`/`reduce` for data transformation | Use `for` loops when array methods are cleaner |
| Use `Math.trunc` for removing the decimal part | Use `~~` for large numbers (it truncates to 32-bit) |
| Provide destructuring defaults for optional values | Assume all destructured properties exist |

**Summary Mnemonic**
- **Array methods** = "Map transforms, Filter selects, Reduce combines"
- **Sort compare** = "Negative → a first, positive → b first"
- **Random integer** = `floor(random() * (max - min + 1) + min)`

[<- Previous: classes and storage](06-classes-and-storage.md) | [Next: data fetching ->](08-data-fetching.md)
