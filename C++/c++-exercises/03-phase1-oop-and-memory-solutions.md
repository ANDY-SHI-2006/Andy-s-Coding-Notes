# Solutions: Phase 1 -- OOP and Memory (Chapters 10--12)

---

## Solution 10.1

**Approach:** Encapsulate width and height with private members, public getters/setters, and utility methods.

```cpp
#include <iostream>

class Rectangle {
    double width;
    double height;

public:
    Rectangle(double w = 1.0, double h = 1.0) : width(w), height(h) {}

    double getWidth() const { return width; }
    double getHeight() const { return height; }
    void setWidth(double w) { width = w; }
    void setHeight(double h) { height = h; }

    double area() const { return width * height; }
    double perimeter() const { return 2 * (width + height); }
};

int main() {
    Rectangle r1(3.0, 4.0);
    Rectangle r2(5.0, 5.0);
    std::cout << "r1 area: " << r1.area() << ", perimeter: " << r1.perimeter() << "\n";
    std::cout << "r2 area: " << r2.area() << ", perimeter: " << r2.perimeter() << "\n";
    return 0;
}
```

---

## Solution 10.2

**Approach:** Add copy constructor and destructor. The destructor is called twice: once for the original, once for the copy.

```cpp
#include <iostream>

class Rectangle {
    double width, height;

public:
    Rectangle(double w = 1.0, double h = 1.0) : width(w), height(h) {
        std::cout << "Constructor called\n";
    }
    Rectangle(const Rectangle& other) : width(other.width), height(other.height) {
        std::cout << "Copy constructor called\n";
    }
    ~Rectangle() {
        std::cout << "Destructor called (" << width << "x" << height << ")\n";
    }
    double area() const { return width * height; }
};

int main() {
    Rectangle r1(3.0, 4.0);   // Constructor
    Rectangle r2 = r1;        // Copy constructor
    std::cout << "r2 area: " << r2.area() << "\n";
    // Both destructors called when main() exits
    return 0;
}
```

**Key points:** Destructor appears twice because there are two objects. Each object is destroyed when it goes out of scope.

---

## Solution 10.3

**Approach:** Encapsulate balance, validate withdrawals.

```cpp
#include <iostream>

class BankAccount {
    double balance;

public:
    BankAccount(double initial) : balance(initial) {
        if (initial < 0) balance = 0;
    }

    bool deposit(double amount) {
        if (amount < 0) return false;
        balance += amount;
        return true;
    }

    bool withdraw(double amount) {
        if (amount < 0 || amount > balance) return false;
        balance -= amount;
        return true;
    }

    double getBalance() const { return balance; }
};

int main() {
    BankAccount acc(100.0);
    std::cout << "Initial: " << acc.getBalance() << "\n";
    acc.deposit(50.0);
    std::cout << "After deposit: " << acc.getBalance() << "\n";
    acc.withdraw(30.0);
    std::cout << "After withdrawal: " << acc.getBalance() << "\n";
    std::cout << "Overdraft attempt: " << (acc.withdraw(200.0) ? "success" : "rejected") << "\n";
    return 0;
}
```

---

## Solution 10.4

**Approach:** Use abstract base class with pure virtual functions. Store derived objects via base pointers.

```cpp
#include <iostream>
#include <vector>
#include <cmath>

class Shape {
public:
    virtual double area() const = 0;
    virtual double perimeter() const = 0;
    virtual ~Shape() = default;
};

class Circle : public Shape {
    double radius;
public:
    Circle(double r) : radius(r) {}
    double area() const override { return M_PI * radius * radius; }
    double perimeter() const override { return 2 * M_PI * radius; }
};

class Rectangle : public Shape {
    double w, h;
public:
    Rectangle(double w, double h) : w(w), h(h) {}
    double area() const override { return w * h; }
    double perimeter() const override { return 2 * (w + h); }
};

class Triangle : public Shape {
    double base, height;
public:
    Triangle(double b, double h) : base(b), height(h) {}
    double area() const override { return 0.5 * base * height; }
    double perimeter() const override { return 3 * base; } // Simplified
};

int main() {
    std::vector<Shape*> shapes;
    shapes.push_back(new Circle(5.0));
    shapes.push_back(new Rectangle(3.0, 4.0));
    shapes.push_back(new Triangle(4.0, 3.0));

    for (auto* s : shapes) {
        std::cout << "Area: " << s->area() << "\n";
    }

    for (auto* s : shapes) delete s;
    return 0;
}
```

**Key points:** Virtual functions enable runtime polymorphism. Without `virtual`, `s->area()` would call `Shape::area()` (which doesn't exist).

---

## Solution 10.5

**Approach:** Without virtual destructor, deleting a derived object through a base pointer only calls the base destructor.

```cpp
#include <iostream>

class ShapeBad {
public:
    ~ShapeBad() { std::cout << "~ShapeBad\n"; }
};

class CircleBad : public ShapeBad {
    double* data;
public:
    CircleBad() { data = new double[100]; }
    ~CircleBad() { delete[] data; std::cout << "~CircleBad\n"; }
};

class ShapeGood {
public:
    virtual ~ShapeGood() { std::cout << "~ShapeGood\n"; }
};

class CircleGood : public ShapeGood {
    double* data;
public:
    CircleGood() { data = new double[100]; }
    ~CircleGood() { delete[] data; std::cout << "~CircleGood\n"; }
};

int main() {
    ShapeBad* b1 = new CircleBad();
    delete b1;  // Only ~ShapeBad called! Memory leak!

    ShapeGood* b2 = new CircleGood();
    delete b2;  // ~CircleGood then ~ShapeGood called. Correct!

    return 0;
}
```

**Key points:** Any class intended to be a base class should have a virtual destructor.

---

## Solution 10.6

**Approach:** Use inheritance with `override` and `final`. `final` prevents further overriding.

```cpp
#include <iostream>
#include <string>

class Person {
protected:
    std::string name;
    int age;
public:
    Person(const std::string& n, int a) : name(n), age(a) {}
    virtual void printInfo() const {
        std::cout << "Name: " << name << ", Age: " << age << "\n";
    }
    virtual ~Person() = default;
};

class Student : public Person {
    double gpa;
    std::string major;
public:
    Student(const std::string& n, int a, double g, const std::string& m)
        : Person(n, a), gpa(g), major(m) {}
    void printInfo() const override {
        std::cout << "Name: " << name << ", Age: " << age
                  << ", GPA: " << gpa << ", Major: " << major << "\n";
    }
};

class Teacher : public Person {
    std::string subject;
    double salary;
public:
    Teacher(const std::string& n, int a, const std::string& s, double sal)
        : Person(n, a), subject(s), salary(sal) {}
    void printInfo() const override final {  // Cannot be overridden further
        std::cout << "Name: " << name << ", Age: " << age
                  << ", Subject: " << subject << ", Salary: " << salary << "\n";
    }
};

int main() {
    Student s("Alice", 20, 3.8, "CS");
    Teacher t("Bob", 45, "Math", 75000);
    s.printInfo();
    t.printInfo();
    return 0;
}
```

---

## Solution 10.7

**Approach:** Use `virtual public` inheritance to ensure only one `Person` subobject.

```cpp
#include <iostream>
#include <string>

class Person {
public:
    std::string name;
    Person(const std::string& n) : name(n) {
        std::cout << "Person constructor\n";
    }
};

class Student : virtual public Person {
public:
    Student(const std::string& n) : Person(n) {
        std::cout << "Student constructor\n";
    }
};

class Employee : virtual public Person {
public:
    Employee(const std::string& n) : Person(n) {
        std::cout << "Employee constructor\n";
    }
};

class WorkingStudent : public Student, public Employee {
public:
    WorkingStudent(const std::string& n)
        : Person(n), Student(n), Employee(n) {
        std::cout << "WorkingStudent constructor\n";
    }
};

int main() {
    WorkingStudent ws("Alice");
    std::cout << "Name: " << ws.name << "\n";  // No ambiguity!
    return 0;
}
```

**Key points:** Without `virtual`, `ws.name` would be ambiguous (two `Person` bases). Virtual inheritance shares one base subobject.

---

## Solution 10.8

**Approach:** Create a class hierarchy with virtual `attack()` and `heal()` methods. Simulate turns.

```cpp
#include <iostream>
#include <string>
#include <memory>
#include <vector>

class Character {
protected:
    std::string name;
    int hp;
    int maxHp;
public:
    Character(const std::string& n, int h) : name(n), hp(h), maxHp(h) {}
    virtual ~Character() = default;

    virtual void attack(Character& target) = 0;
    virtual void takeDamage(int dmg) {
        hp -= dmg;
        if (hp < 0) hp = 0;
    }
    bool isAlive() const { return hp > 0; }
    void printStatus() const {
        std::cout << name << " HP: " << hp << "/" << maxHp << "\n";
    }
};

class Warrior : public Character {
public:
    Warrior(const std::string& n) : Character(n, 150) {}
    void attack(Character& target) override {
        std::cout << name << " strikes with sword!\n";
        target.takeDamage(25);
    }
};

class Mage : public Character {
    int mana;
public:
    Mage(const std::string& n) : Character(n, 80), mana(100) {}
    void attack(Character& target) override {
        if (mana >= 20) {
            std::cout << name << " casts fireball!\n";
            target.takeDamage(35);
            mana -= 20;
        } else {
            std::cout << name << " is out of mana!\n";
        }
    }
};

class Healer : public Character {
public:
    Healer(const std::string& n) : Character(n, 100) {}
    void attack(Character& target) override {
        std::cout << name << " cannot attack!\n";
    }
    void heal(Character& target) {
        std::cout << name << " heals " << target.name << "!\n";
        target.takeDamage(-20);  // Negative damage = healing
        if (target.hp > target.maxHp) target.hp = target.maxHp;
    }
};

int main() {
    std::vector<std::unique_ptr<Character>> team1;
    team1.push_back(std::make_unique<Warrior>("Warrior1"));
    team1.push_back(std::make_unique<Mage>("Mage1"));

    std::vector<std::unique_ptr<Character>> team2;
    team2.push_back(std::make_unique<Warrior>("Warrior2"));
    team2.push_back(std::make_unique<Healer>("Healer1"));

    for (int turn = 1; turn <= 5; ++turn) {
        std::cout << "\n--- Turn " << turn << " ---\n";
        team1[0]->attack(*team2[0]);
        team2[0]->attack(*team1[0]);
        dynamic_cast<Healer*>(team2[1].get())->heal(*team2[0]);
        team1[1]->attack(*team2[0]);

        for (auto& c : team1) c->printStatus();
        for (auto& c : team2) c->printStatus();
    }

    return 0;
}
```

---

## Solution 11.1

**Approach:** Use `std::vector` algorithms: `minmax_element`, `sort`, `remove_if`.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>

int main() {
    std::vector<int> vec(20);
    std::mt19937 gen(std::random_device{}());
    std::uniform_int_distribution<> dist(1, 100);

    for (int& x : vec) x = dist(gen);

    std::cout << "Original: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";

    auto [minIt, maxIt] = std::minmax_element(vec.begin(), vec.end());
    std::cout << "Min: " << *minIt << ", Max: " << *maxIt << "\n";

    std::sort(vec.begin(), vec.end(), std::greater<>());
    std::cout << "Sorted (desc): ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";

    vec.erase(std::remove_if(vec.begin(), vec.end(),
                             [](int x) { return x % 2 == 0; }), vec.end());
    std::cout << "After removing evens: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";

    return 0;
}
```

**Key points:** `erase-remove_if` idiom efficiently removes elements. `std::greater<>()` for descending sort.

---

## Solution 11.2

**Approach:** Use `std::istringstream` to split by whitespace, then reverse print.

```cpp
#include <iostream>
#include <sstream>
#include <vector>
#include <string>

int main() {
    std::string sentence;
    std::cout << "Enter a sentence: ";
    std::getline(std::cin, sentence);

    std::istringstream iss(sentence);
    std::vector<std::string> words;
    std::string word;
    while (iss >> word) {
        words.push_back(word);
    }

    std::cout << "Reversed: ";
    for (auto it = words.rbegin(); it != words.rend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";

    return 0;
}
```

---

## Solution 11.3

**Approach:** Read file, normalize words, count with `std::map`, then sort by frequency.

```cpp
#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <algorithm>
#include <cctype>
#include <string>

std::string normalize(const std::string& word) {
    std::string result;
    for (char c : word) {
        if (std::isalpha(c)) result += std::tolower(c);
    }
    return result;
}

int main() {
    std::ifstream file("text.txt");
    if (!file) { std::cerr << "Cannot open file\n"; return 1; }

    std::map<std::string, int> freq;
    std::string word;
    while (file >> word) {
        auto norm = normalize(word);
        if (!norm.empty()) ++freq[norm];
    }

    std::vector<std::pair<std::string, int>> sorted(freq.begin(), freq.end());
    std::sort(sorted.begin(), sorted.end(),
              [](auto& a, auto& b) { return a.second > b.second; });

    std::cout << "Top 5 words:\n";
    for (size_t i = 0; i < std::min(size_t(5), sorted.size()); ++i) {
        std::cout << sorted[i].first << ": " << sorted[i].second << "\n";
    }

    return 0;
}
```

---

## Solution 11.4

**Approach:** Insert 100,000 random integers into both set types and compare timing.

```cpp
#include <iostream>
#include <set>
#include <unordered_set>
#include <chrono>
#include <random>

int main() {
    const int N = 100'000;
    std::mt19937 gen(42);
    std::uniform_int_distribution<> dist(1, N * 10);

    std::set<int> s;
    std::unordered_set<int> us;

    auto start1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) s.insert(dist(gen));
    auto end1 = std::chrono::high_resolution_clock::now();

    auto start2 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) us.insert(dist(gen));
    auto end2 = std::chrono::high_resolution_clock::now();

    auto ms1 = std::chrono::duration_cast<std::chrono::milliseconds>(end1 - start1);
    auto ms2 = std::chrono::duration_cast<std::chrono::milliseconds>(end2 - start2);

    std::cout << "std::set: " << ms1.count() << " ms (O(log n) per insert)\n";
    std::cout << "std::unordered_set: " << ms2.count() << " ms (O(1) average)\n";
    return 0;
}
```

**Key points:** `unordered_set` is typically faster for insertion but uses more memory and has worst-case O(n) if hash collisions occur.

---

## Solution 11.5

**Approach:** Use a stack. Push operands, pop two for operators.

```cpp
#include <iostream>
#include <stack>
#include <sstream>
#include <string>

int main() {
    std::string expr;
    std::cout << "Enter RPN expression (e.g., '3 4 + 2 *'): ";
    std::getline(std::cin, expr);

    std::stack<double> stk;
    std::istringstream iss(expr);
    std::string token;

    while (iss >> token) {
        if (token == "+" || token == "-" || token == "*" || token == "/") {
            if (stk.size() < 2) { std::cerr << "Invalid expression\n"; return 1; }
            double b = stk.top(); stk.pop();
            double a = stk.top(); stk.pop();
            if (token == "+") stk.push(a + b);
            else if (token == "-") stk.push(a - b);
            else if (token == "*") stk.push(a * b);
            else if (b != 0) stk.push(a / b);
        } else {
            stk.push(std::stod(token));
        }
    }

    if (stk.size() == 1) {
        std::cout << "Result: " << stk.top() << "\n";
    } else {
        std::cerr << "Invalid expression\n";
    }
    return 0;
}
```

---

## Solution 11.6

**Approach:** Use a min-heap of size K. This is O(N log K) vs O(N log N) for full sort.

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <chrono>
#include <random>

int main() {
    const int N = 1'000'000;
    const int K = 10;

    std::mt19937 gen(42);
    std::uniform_int_distribution<> dist(1, N);
    std::vector<int> data(N);
    for (int& x : data) x = dist(gen);

    // Method 1: Priority queue
    auto start1 = std::chrono::high_resolution_clock::now();
    std::priority_queue<int, std::vector<int>, std::greater<>> minHeap;
    for (int x : data) {
        minHeap.push(x);
        if (minHeap.size() > K) minHeap.pop();
    }
    auto end1 = std::chrono::high_resolution_clock::now();

    // Method 2: Full sort
    auto start2 = std::chrono::high_resolution_clock::now();
    auto sorted = data;
    std::sort(sorted.begin(), sorted.end(), std::greater<>());
    auto end2 = std::chrono::high_resolution_clock::now();

    auto ms1 = std::chrono::duration_cast<std::chrono::milliseconds>(end1 - start1);
    auto ms2 = std::chrono::duration_cast<std::chrono::milliseconds>(end2 - start2);

    std::cout << "Priority queue (O(N log K)): " << ms1.count() << " ms\n";
    std::cout << "Full sort (O(N log N)): " << ms2.count() << " ms\n";
    return 0;
}
```

**Key points:** For K << N, the priority queue approach is much faster. Full sort is simpler if you need all elements sorted.

---

## Solution 11.7

**Approach:** Load dictionary into `unordered_set`, then check each word. Normalize to lowercase.

```cpp
#include <iostream>
#include <fstream>
#include <unordered_set>
#include <string>
#include <algorithm>
#include <cctype>

std::string toLower(const std::string& s) {
    std::string r = s;
    for (char& c : r) c = std::tolower(c);
    return r;
}

int main() {
    std::unordered_set<std::string> dict;
    std::ifstream dictFile("dictionary.txt");
    std::string word;
    while (dictFile >> word) dict.insert(toLower(word));

    std::ifstream textFile("text.txt");
    while (textFile >> word) {
        auto norm = toLower(word);
        // Strip punctuation from ends
        while (!norm.empty() && !std::isalpha(norm.back())) norm.pop_back();
        while (!norm.empty() && !std::isalpha(norm.front())) norm.erase(0, 1);

        if (!norm.empty() && !dict.count(norm)) {
            std::cout << "Misspelled: " << norm << "\n";
        }
    }

    return 0;
}
```

---

## Solution 12.1

**Approach:** Use `new[]` and `delete[]`. Never mix `new` with `delete[]` or vice versa.

```cpp
#include <iostream>

int main() {
    int* arr = new int[10];

    for (int i = 0; i < 10; ++i) {
        arr[i] = i + 1;
    }

    for (int i = 0; i < 10; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << "\n";

    delete[] arr;  // Must use delete[] for arrays!
    return 0;
}
```

**Key points:** `new[]` must be paired with `delete[]`. Using `delete` on an array is undefined behavior.

---

## Solution 12.2

**Approach:** `int arr[n]` is a VLA (Variable Length Array), which is not standard C++. Use `new[]` or `std::vector`.

```cpp
#include <iostream>

// Fixed version using new[]
int* createArray(int n) {
    int* arr = new int[n];
    for (int i = 0; i < n; ++i) arr[i] = i;
    return arr;
}

// Better version using std::vector
#include <vector>
std::vector<int> createArrayBetter(int n) {
    std::vector<int> arr(n);
    for (int i = 0; i < n; ++i) arr[i] = i;
    return arr;
}

int main() {
    int* arr = createArray(5);
    for (int i = 0; i < 5; ++i) std::cout << arr[i] << " ";
    std::cout << "\n";
    delete[] arr;

    auto vec = createArrayBetter(5);
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";

    return 0;
}
```

**Key points:** VLAs are a C99 feature, not standard C++. The original `arr` is a local array on the stack; returning it gives a dangling pointer.

---

## Solution 12.3

**Approach:** Allocate new memory, copy all elements.

```cpp
#include <iostream>

int* cloneArray(const int* src, int size) {
    int* dest = new int[size];
    for (int i = 0; i < size; ++i) {
        dest[i] = src[i];
    }
    return dest;
}

int main() {
    int original[] = {1, 2, 3, 4, 5};
    int* clone = cloneArray(original, 5);

    original[0] = 99;  // Modify original

    std::cout << "Original[0]: " << original[0] << "\n";
    std::cout << "Clone[0]: " << clone[0] << "\n";  // Still 1

    delete[] clone;
    return 0;
}
```

---

## Solution 12.4

**Approach:** Implement basic linked list operations.

```cpp
#include <iostream>

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

void push_front(Node*& head, int value) {
    Node* newNode = new Node(value);
    newNode->next = head;
    head = newNode;
}

void print_list(Node* head) {
    while (head) {
        std::cout << head->data << " -> ";
        head = head->next;
    }
    std::cout << "null\n";
}

void free_list(Node*& head) {
    while (head) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
}

int main() {
    Node* head = nullptr;
    push_front(head, 3);
    push_front(head, 2);
    push_front(head, 1);
    print_list(head);
    free_list(head);
    return 0;
}
```

---

## Solution 12.5

**Approach:** Allocate array of pointers, then each row.

```cpp
#include <iostream>

int** createMatrix(int rows, int cols) {
    int** matrix = new int*[rows];
    for (int i = 0; i < rows; ++i) {
        matrix[i] = new int[cols];
    }
    return matrix;
}

void freeMatrix(int** matrix, int rows) {
    for (int i = 0; i < rows; ++i) {
        delete[] matrix[i];
    }
    delete[] matrix;
}

int main() {
    int rows = 3, cols = 4;
    int** m = createMatrix(rows, cols);

    int val = 1;
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            m[i][j] = val++;

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j)
            std::cout << m[i][j] << "\t";
        std::cout << "\n";
    }

    freeMatrix(m, rows);
    return 0;
}
```

**Key points:** Free in reverse order of allocation: rows first, then the pointer array.

---

## Solution 12.6

**Approach:** Show how each null value resolves in overload resolution.

```cpp
#include <iostream>

void foo(int x) { std::cout << "foo(int): " << x << "\n"; }
void foo(char* p) { std::cout << "foo(char*)\n"; }
void foo(std::nullptr_t p) { std::cout << "foo(nullptr_t)\n"; }

int main() {
    foo(0);           // foo(int) -- 0 is an int literal
    // foo(NULL);     // Ambiguous or foo(int) depending on definition
    foo(nullptr);     // foo(nullptr_t) -- perfect match
    return 0;
}
```

**Key points:** `NULL` is typically `0` or `(void*)0`, causing ambiguity. `nullptr` has its own type and always resolves correctly.

---

## Solution 12.7

**Approach:** Pre-allocate a large block, manage free chunks with a linked list.

```cpp
#include <iostream>
#include <chrono>
#include <vector>

class MemoryPool {
    struct Block {
        Block* next;
    };
    char* memory;
    size_t chunkSize;
    size_t numChunks;
    Block* freeList;

public:
    MemoryPool(size_t chunkSize, size_t numChunks)
        : chunkSize(std::max(chunkSize, sizeof(Block))),
          numChunks(numChunks) {
        memory = new char[this->chunkSize * numChunks];
        freeList = nullptr;
        for (size_t i = 0; i < numChunks; ++i) {
            Block* block = reinterpret_cast<Block*>(memory + i * this->chunkSize);
            block->next = freeList;
            freeList = block;
        }
    }

    void* allocate() {
        if (!freeList) return nullptr;
        Block* block = freeList;
        freeList = freeList->next;
        return block;
    }

    void deallocate(void* ptr) {
        if (!ptr) return;
        Block* block = static_cast<Block*>(ptr);
        block->next = freeList;
        freeList = block;
    }

    ~MemoryPool() { delete[] memory; }
};

struct SmallObject {
    int data[16];
};

int main() {
    const int N = 1'000'000;

    // Pool test
    MemoryPool pool(sizeof(SmallObject), N);
    auto start1 = std::chrono::high_resolution_clock::now();
    std::vector<void*> ptrs;
    for (int i = 0; i < N; ++i) {
        ptrs.push_back(pool.allocate());
    }
    for (void* p : ptrs) pool.deallocate(p);
    auto end1 = std::chrono::high_resolution_clock::now();

    // new/delete test
    auto start2 = std::chrono::high_resolution_clock::now();
    std::vector<SmallObject*> objs;
    for (int i = 0; i < N; ++i) {
        objs.push_back(new SmallObject());
    }
    for (auto* p : objs) delete p;
    auto end2 = std::chrono::high_resolution_clock::now();

    auto ms1 = std::chrono::duration_cast<std::chrono::milliseconds>(end1 - start1);
    auto ms2 = std::chrono::duration_cast<std::chrono::milliseconds>(end2 - start2);

    std::cout << "Pool: " << ms1.count() << " ms\n";
    std::cout << "new/delete: " << ms2.count() << " ms\n";
    return 0;
}
```

**Key points:** Memory pools avoid system call overhead and fragmentation. They are much faster for many small allocations.

---

## Solution 10.9

**Approach:** Use reference counting. On write, check count; if > 1, make a private copy.

```cpp
#include <iostream>
#include <cstring>

class CowString {
    struct SharedBuffer {
        char* data;
        int refCount;
        SharedBuffer(const char* str) : refCount(1) {
            data = new char[std::strlen(str) + 1];
            std::strcpy(data, str);
        }
        ~SharedBuffer() { delete[] data; }
    };
    SharedBuffer* buffer;

    void detach() {
        if (buffer->refCount > 1) {
            --buffer->refCount;
            buffer = new SharedBuffer(buffer->data);
        }
    }

public:
    CowString(const char* str = "") : buffer(new SharedBuffer(str)) {}
    CowString(const CowString& other) : buffer(other.buffer) {
        ++buffer->refCount;
    }
    ~CowString() {
        if (--buffer->refCount == 0) delete buffer;
    }

    CowString& operator=(const CowString& other) {
        if (this != &other) {
            if (--buffer->refCount == 0) delete buffer;
            buffer = other.buffer;
            ++buffer->refCount;
        }
        return *this;
    }

    char operator[](size_t index) const { return buffer->data[index]; }
    char& operator[](size_t index) {
        detach();  // Copy on write!
        return buffer->data[index];
    }

    const char* c_str() const { return buffer->data; }
    int getRefCount() const { return buffer->refCount; }
};

int main() {
    CowString s1("Hello");
    CowString s2 = s1;  // Share buffer
    std::cout << "Shared refs: " << s1.getRefCount() << "\n";

    s2[0] = 'J';  // Copy on write!
    std::cout << "After write, s1 refs: " << s1.getRefCount() << "\n";
    std::cout << "s1: " << s1.c_str() << "\n";
    std::cout << "s2: " << s2.c_str() << "\n";

    return 0;
}
```

**Key points:** COW saves memory when strings are copied but not modified. It adds overhead on the first write.

---

## Solution 12.8

**Approach:** Each byte stores 8 bits. Use bit masks for set/clear/get.

```cpp
#include <iostream>
#include <cstring>

class BitSet {
    unsigned char* data;
    size_t numBits;
    size_t numBytes;

    size_t byteIndex(size_t bit) const { return bit / 8; }
    size_t bitOffset(size_t bit) const { return bit % 8; }

public:
    BitSet(size_t n) : numBits(n) {
        numBytes = (n + 7) / 8;
        data = new unsigned char[numBytes]();
    }
    ~BitSet() { delete[] data; }

    void set(size_t index) {
        if (index >= numBits) return;
        data[byteIndex(index)] |= (1 << bitOffset(index));
    }

    void clear(size_t index) {
        if (index >= numBits) return;
        data[byteIndex(index)] &= ~(1 << bitOffset(index));
    }

    bool get(size_t index) const {
        if (index >= numBits) return false;
        return (data[byteIndex(index)] >> bitOffset(index)) & 1;
    }

    size_t count() const {
        size_t c = 0;
        for (size_t i = 0; i < numBits; ++i)
            if (get(i)) ++c;
        return c;
    }
};

int main() {
    BitSet bs(1'000'000);
    bs.set(0);
    bs.set(999'999);
    std::cout << "Bit 0: " << bs.get(0) << "\n";
    std::cout << "Bit 999999: " << bs.get(999999) << "\n";
    std::cout << "Count: " << bs.count() << "\n";
    return 0;
}
```

**Key points:** 1,000,000 bits = ~122 KB. A `bool` array would use ~1 MB (typically 1 byte per bool).
