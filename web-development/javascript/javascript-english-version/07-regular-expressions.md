[<- Previous: classes and storage](06-classes-and-storage.md) | [Next: data fetching ->](08-data-fetching.md)

# 7 Strings, Arrays, Dates, and Regular Expressions

Core built-in objects and methods for manipulating text, collections, time, and pattern matching.

## 7.1 String Methods

### 7.1.1 Reading and Searching

```javascript
let text = "Hello, World!";

text.length;              // 13
text[0];                  // "H"
text.charAt(0);           // "H"
text.charCodeAt(0);       // 72 (Unicode code point)

text.indexOf("World");    // 7  (first occurrence)
text.lastIndexOf("l");    // 10 (last occurrence)
text.includes("World");   // true
text.startsWith("Hello"); // true
text.endsWith("!");       // true
```

### 7.1.2 Extracting Substrings

```javascript
let text = "Hello, World!";

text.slice(0, 5);         // "Hello" (start, end)
text.slice(7);            // "World!" (start to end)
text.slice(-6);           // "World!" (negative = from end)

text.substring(0, 5);     // "Hello" (same as slice, no negatives)
text.substr(7, 5);        // "World" (start, length) — deprecated
```

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
let parts = csv.split(",");     // ["Alice", "25", "Engineer"]

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

arr.push(4);            // [1, 2, 3, 4] — add to end
arr.pop();              // [1, 2, 3] — remove from end
arr.unshift(0);         // [0, 1, 2, 3] — add to start
arr.shift();            // [1, 2, 3] — remove from start

arr.splice(1, 1);       // [1, 3] — remove 1 item at index 1
arr.splice(1, 0, "a");  // [1, "a", 3] — insert at index 1
arr.splice(1, 1, "b");  // [1, "b", 3] — replace at index 1
```

### 7.2.3 Iteration

```javascript
let numbers = [1, 2, 3, 4, 5];

// forEach — execute for each element
numbers.forEach(num => console.log(num));

// map — transform each element, return new array
let doubled = numbers.map(num => num * 2);    // [2, 4, 6, 8, 10]

// filter — keep elements that pass the test
let evens = numbers.filter(num => num % 2 === 0);  // [2, 4]

// reduce — reduce to a single value
let sum = numbers.reduce((total, num) => total + num, 0);  // 15

// some — does ANY element pass?
let hasEven = numbers.some(num => num % 2 === 0);   // true

// every — do ALL elements pass?
let allPositive = numbers.every(num => num > 0);    // true
```

### 7.2.4 Other Useful Methods

```javascript
let arr = [3, 1, 4, 1, 5];

arr.sort((a, b) => a - b);     // [1, 1, 3, 4, 5] — numeric sort
arr.reverse();                  // [5, 4, 3, 1, 1]
arr.concat([9, 2]);             // [5, 4, 3, 1, 1, 9, 2]
arr.slice(1, 3);                // [4, 3] — extract portion
arr.join("-");                  // "5-4-3-1-1"
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

// Locale-specific formatting
date.toLocaleDateString("en-US");   // "12/25/2024"
date.toLocaleDateString("zh-CN");   // "2024/12/25"

date.toLocaleTimeString("en-US");   // "10:30:00 AM"

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

---

## 7.5 Best Practices

| Do | Don't |
|----|-------|
| Use `slice` instead of `substr` (deprecated) | Use `substr` in new code |
| Use `===` with `indexOf` results (`!== -1`) | Forget that `indexOf` returns `-1` when not found |
| Use spread `[...arr]` before `sort`/`reverse` if you need original | Mutate original arrays unintentionally |
| Use `toLocaleDateString` for user-facing dates | Use `toString()` for user-facing dates (format varies) |
| Test regex patterns with tools like regex101.com | Write complex regex without testing |
| Use `map`/`filter`/`reduce` for data transformation | Use `for` loops when array methods are cleaner |

**Summary Mnemonic**
- **Array methods** = "Map transforms, Filter selects, Reduce combines"

[<- Previous: classes and storage](06-classes-and-storage.md) | [Next: data fetching ->](08-data-fetching.md)
