[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)

# 4 Variable Basics

变量是C++程序中存储数据的基本单元。本章介绍变量的声明、定义、初始化、类型和存储等核心概念。

## 4.1 Declaration vs Definition

**声明(Declaration)**告诉编译器一个名称和类型存在，**定义(Definition)**则创建实际的变量并分配内存。

| 特性 | 声明 | 定义 |
|------|------|------|
| **目的** | 告知编译器名称和类型 | 创建变量，分配内存 |
| **内存** | 不分配 | 分配 |
| **次数** | 可多次 | 只能一次(ODR规则) |
| **变量示例** | `extern int x;` | `int x = 5;` |
| **函数示例** | `void foo();` | `void foo() { ... }` |

**关键理解**：定义也是一种声明，但声明不一定是定义。

```cpp
extern int globalVar;      // 纯声明
int globalVar = 10;        // 定义（也是声明）

void func();               // 函数声明（原型）
void func() { ... }        // 函数定义
```

### 4.1.1 One Definition Rule (ODR)

C++规定每个变量和函数在整个程序中**只能定义一次**，否则会导致链接错误。

```cpp
// file1.cpp
int shared = 100;          // 定义

// file2.cpp
int shared = 100;          // ❌ 错误！重复定义
extern int shared;         // ✓ 正确！只是声明
```

## 4.2 Variable Definition and Initialization

### 4.2.1 Basic Syntax

定义变量时，可以同时初始化，也可以稍后初始化（但不初始化是危险的）。

```cpp
int a;                    // 定义，未初始化（值不确定！）
int b = 5;                // 定义并初始化为5
int c(5);                 // 直接初始化
int d{5};                 // 列表初始化（C++11，推荐）

// 多变量定义
int x = 1, y = 2, z = 3;  // 都初始化
int m, n, p;              // 都未初始化（避免！）
```

> ⚠️ **警告**：使用未初始化的变量会导致未定义行为，可能产生随机值或程序崩溃。

### 4.2.2 Initialization Methods

C++提供了多种初始化方式，理解它们的区别很重要：

**1. Copy Initialization（拷贝初始化）**
```cpp
int a = 5;           // 使用 = 号
string s = "hello";  // 拷贝赋值风格
```

**2. Direct Initialization（直接初始化）**
```cpp
int a(5);            // 使用圆括号
string s("hello");   // 直接构造
```

**3. List Initialization / Brace Initialization（列表初始化，C++11推荐）**
```cpp
int a{5};            // 使用花括号
int b{};             // 零初始化（b = 0）
vector<int> v{1, 2, 3};  // 初始化列表
```

**为什么选择花括号初始化？**
- **防止窄化转换**：`int x{3.14};` 会编译错误，而 `int x = 3.14;` 只是警告
- **语法统一**：适用于所有类型（基本类型、类、容器）
- **避免歧义**：不会出现"最令人困惑的解析"问题

```cpp
int x = 3.14;        // ✓ 编译通过，x = 3（数据丢失）
int y{3.14};         // ✗ 编译错误！防止意外窄化
```

### 4.2.3 Initialization Best Practices

| 场景 | 推荐写法 | 说明 |
|------|---------|------|
| 基本类型 | `int x{5};` | 花括号初始化，安全 |
| 类类型 | `string s{"hi"};` | 花括号或圆括号 |
| 容器 | `vector<int> v{1, 2, 3};` | 花括号初始化元素 |
| 零初始化 | `int x{};` | 空花括号，值为0 |
| 动态数组 | `auto arr = new int[10]{};` | 分配并零初始化 |

## 4.3 Variable Scope and Lifetime

变量不仅有自己的类型和值，还有**作用域**（在哪里可见）和**生命周期**（何时创建和销毁）。

### 4.3.1 Scope（作用域）

作用域决定了变量在代码的哪些部分可以被访问。

**1. Local Scope（局部作用域）**
```cpp
void func() {
    int x = 10;        // x 只在 func() 内可见
    if (x > 5) {
        int y = 20;    // y 只在 if 块内可见
    }
    // y 在这里不可用
}
// x 在这里不可用
```

**2. Global Scope（全局作用域）**
```cpp
int g_count = 0;       // 全局变量，整个文件可见

void func1() {
    g_count++;         // 可以访问
}

void func2() {
    g_count++;         // 也可以访问
}
```

**3. Block Scope（块作用域）**
```cpp
{
    int temp = 100;    // 只在 {} 块内有效
}
// temp 已销毁，不可访问
```

### 4.3.2 Lifetime（生命周期）

生命周期决定了变量何时被创建和销毁。

| 存储类型 | 创建时机 | 销毁时机 | 示例 |
|---------|---------|---------|------|
| **自动存储期** | 进入作用域 | 离开作用域 | 局部变量 `int x;` |
| **静态存储期** | 程序启动 | 程序结束 | 全局变量，`static`变量 |
| **动态存储期** | 调用 `new` | 调用 `delete` | 堆上对象 |

```cpp
void example() {
    int local{10};              // 自动存储期，每次调用创建/销毁
    static int count{0};        // 静态存储期，只创建一次，保持值
    count++;
    cout << count << endl;
}

// 第一次调用：输出 1
// 第二次调用：输出 2
// 第三次调用：输出 3
```

### 4.3.3 Global vs Local Variables

**局部变量（Local）**：
- 定义在函数或块内部
- 默认不初始化（值随机）
- 函数结束后自动销毁
- 不同函数可以有同名变量，互不干扰

**全局变量（Global）**：
- 定义在所有函数外部
- 自动零初始化（0, false, nullptr）
- 程序结束时销毁
- 可以被整个程序访问（通过 `extern` 声明）

```cpp
int g_value = 100;     // 全局变量

void foo() {
    int local = 10;    // 局部变量
    g_value++;         // 可以访问全局变量
}

void bar() {
    cout << g_value;   // 看到 foo() 修改后的值
}
```

> **建议**：尽量少用全局变量，它们会增加代码的耦合性和理解难度。

## 4.4 Constants: const and constexpr

常量是值不能被修改的变量，C++提供了两种定义常量的方式。

### 4.4.1 const（运行时常量）

`const` 表示变量的值在初始化后不能被修改。

```cpp
const int maxSize = 100;        // 编译时已知
const double pi = 3.14159;      // 编译时已知

const int userInput = getInput();  // 运行时确定，但之后不能改

maxSize = 200;                  // ✗ 编译错误！不能修改const
```

**const 和指针**：
```cpp
const int* ptr;        // 指向常量的指针（值不能改，指针可以改）
int* const ptr;        // 常量指针（指针不能改，值可以改）
const int* const ptr;  // 常量指针指向常量（都不能改）
```

### 4.4.2 constexpr（编译时常量，C++11）

`constexpr` 表示变量的值必须在**编译时**就能确定，可用于数组大小、模板参数等需要编译时常量的地方。

```cpp
constexpr int maxSize = 100;           // ✓ 编译时常量
constexpr int size = maxSize * 2;      // ✓ 可以用于计算

int arr[size];                         // ✓ 可以定义数组

constexpr int userVal = getInput();    // ✗ 错误！必须是编译时可计算
```

**constexpr 函数**：
```cpp
constexpr int square(int x) {          // constexpr函数
    return x * x;
}

constexpr int result = square(5);      // ✓ 编译时计算，result = 25
```

### 4.4.3 const vs constexpr: When to Use?

| 特性 | const | constexpr |
|------|-------|-----------|
| **确定时机** | 编译时或运行时 | 编译时 |
| **使用场景** | 防止意外修改 | 需要编译时常量 |
| **数组大小** | C++11前不可用 | ✓ 可用 |
| **模板参数** | ✗ 不可用 | ✓ 可用 |
| **推荐程度** | 一般常量 | 优先使用（如果可能）|

**选择建议**：
- 如果值在编译时已知 → 使用 `constexpr`
- 如果值运行时才能确定 → 使用 `const`
- 如果只是不想被修改 → 使用 `const`

## 4.5 Type Deduction and Aliases

### 4.5.1 auto（类型推导，C++11）

`auto` 让编译器根据初始化表达式自动推断变量类型。

```cpp
auto i = 5;           // int
auto d = 3.14;        // double
auto s = "hello";     // const char*
auto v = vector<int>{1, 2, 3};  // vector<int>
```

**使用 auto 的场景**：
- 类型名很长时（迭代器）
- 类型很明显时
- 模板编程中

```cpp
// 避免冗长的迭代器类型
for (auto it = container.begin(); it != container.end(); ++it) { ... }

// 范围for循环中
for (const auto& elem : container) { ... }

// Lambda表达式
auto func = [](int x) { return x * x; };
```

**auto 的限制**：
- 必须初始化：`auto x;` 错误！
- 推荐用 `=` 而非花括号：`auto x = 5;` ✓，`auto x{5};` 可能有意外行为

### 4.5.2 Type Aliases（类型别名）

类型别名给现有类型创建新名字，让代码更易读或更易修改。

**C风格：typedef**
```cpp
typedef unsigned int uint;
typedef std::vector<std::string> StringList;
typedef void (*Callback)(int);       // 函数指针类型
```

**现代C++：using（推荐）**
```cpp
using uint = unsigned int;
using StringList = std::vector<std::string>;
using Callback = void(*)(int);       // 更清晰
```

**为什么用类型别名？**
- **简化长类型名**：`std::map<std::string, std::vector<int>>` → `StringToIntVectorMap`
- **平台无关代码**：`using int32 = int;`（在32位系统），之后可改为 `int32_t`
- **易于修改**：改别名定义，所有使用处自动更新

## 4.6 Summary and Best Practices

### 本章核心要点

1. **声明 vs 定义**：声明告知存在，定义创建实体分配内存
2. **ODR规则**：每个变量/函数只能定义一次
3. **初始化**：优先使用花括号 `{}`，防止窄化转换
4. **作用域**：理解局部、全局、块作用域的区别
5. **常量**：优先使用 `constexpr`（编译时常量），其次 `const`
6. **类型推导**：`auto` 简化代码，但保持代码可读性
7. **类型别名**：`using` 优于 `typedef`，更清晰

### 快速参考表

| 场景 | 推荐写法 |
|------|---------|
| 基本变量定义 | `int x{5};` |
| 零初始化 | `int x{};` |
| 编译时常量 | `constexpr int max = 100;` |
| 运行时常量 | `const int val = getValue();` |
| 复杂类型迭代器 | `auto it = container.begin();` |
| 类型别名 | `using MyInt = int;` |
| 全局变量（尽量少用） | `int g_count = 0;` |
| 静态局部变量 | `static int counter{0};` |

---

[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)
