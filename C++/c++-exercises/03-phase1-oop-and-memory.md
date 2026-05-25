# Phase 1 — OOP and Memory Exercises (Chapters 10–12)

## Chapter 10: Object-Oriented Programming

### Exercise 10.1 🟢
Design a `Rectangle` class with private members `width` and `height`. Provide:
- A constructor with default values
- Getter and setter methods
- A method `double area()` that returns width × height
- A method `double perimeter()`

Write a `main()` that creates two rectangles and prints their areas.

### Exercise 10.2 🟡
Extend Exercise 10.1 with a copy constructor and a destructor that prints a message when called. Create a rectangle, copy it into another variable, and observe the output. Explain why the destructor message appears twice.

### Exercise 10.3 🟡
Create a `BankAccount` class with:
- Private balance
- Constructor that takes initial balance
- `deposit(double)`, `withdraw(double)`, and `getBalance()` methods
- `withdraw` should reject overdrafts (return false)

Write test code that deposits, withdraws, and attempts an invalid withdrawal.

### Exercise 10.4 🟡
Design an inheritance hierarchy:
- Base class `Shape` with pure virtual `double area()` and `double perimeter()`
- Derived classes `Circle` (radius), `Rectangle` (width, height), `Triangle` (base, height)

Create an array of `Shape*` pointers, populate it with different shapes, and use a loop to print each shape's area. Demonstrate **polymorphism**.

### Exercise 10.5 🟡
Explain what happens if `Shape` in Exercise 10.4 does **not** have a virtual destructor. Write a program that demonstrates the memory leak, then fix it by adding `virtual ~Shape()`.

### Exercise 10.6 🟡
Create a `Person` base class with `name` and `age`. Derive `Student` (adds `gpa` and `major`) and `Teacher` (adds `subject` and `salary`). Write a `printInfo()` method in each class that prints all fields. Use `override` and `final` appropriately.

### Exercise 10.7 🟡
Implement the **Diamond Problem** with classes:
- `Person` (has `name`)
- `Student : virtual public Person`
- `Employee : virtual public Person`
- `WorkingStudent : public Student, public Employee`

Create a `WorkingStudent` object and demonstrate that `name` is stored only once thanks to virtual inheritance.

### Exercise 10.8 🔴
Design a simple **text-based RPG class system**:
- Base `Character` with HP, name, and `attack(Character& target)`
- `Warrior` (high HP, melee attack)
- `Mage` (low HP, spell attack with mana cost)
- `Healer` (can heal allies instead of attacking)

Use virtual functions, inheritance, and polymorphism to simulate a 2v2 battle.

---

## Chapter 11: STL Basics

### Exercise 11.1 🟢
Create a `std::vector<int>`, fill it with 20 random integers between 1 and 100, then:
1. Print all elements
2. Find and print the maximum and minimum
3. Sort it in descending order
4. Remove all even numbers
5. Print the final vector

### Exercise 11.2 🟡
Write a program that reads a sentence from the user, splits it into words using `std::istringstream`, stores them in a `std::vector<std::string>`, and prints them in reverse order.

### Exercise 11.3 🟡
Use `std::map<std::string, int>` to count word frequencies in a text file. Read the file, split into words, and print the top 5 most frequent words.

### Exercise 11.4 🟡
Create a `std::set<int>` and a `std::unordered_set<int>`. Insert 100,000 random integers into both. Measure and compare the insertion time using `<chrono>`. Which is faster? Why?

### Exercise 11.5 🟡
Implement a simple **reverse Polish notation (RPN) calculator** using `std::stack<double>`. Support `+`, `-`, `*`, `/` operators. Example input: `3 4 + 2 *` should produce `14`.

### Exercise 11.6 🟡
Use `std::priority_queue<int>` to find the **top K largest elements** in a vector of 1,000,000 random integers. Compare this approach with sorting the entire array.

### Exercise 11.7 🔴
Write a program that implements a **spell checker** using `std::unordered_set<std::string>`. Load a dictionary file, then check each word in a text file against the dictionary. Print any misspelled words. Use `std::transform` to handle case-insensitivity.

---

## Chapter 12: Pointers and Dynamic Memory

### Exercise 12.1 🟢
Write a program that dynamically allocates an array of 10 integers using `new[]`, fills it with values 1–10, prints them, and then properly deallocates using `delete[]`.

### Exercise 12.2 🟡
Explain the bug in the following code. Fix it:

```cpp
int* createArray(int n) {
    int arr[n];  // C99 VLA — not standard C++
    for (int i = 0; i < n; i++) arr[i] = i;
    return arr;
}
```

### Exercise 12.3 🟡
Write a function `int* cloneArray(const int* src, int size)` that returns a **deep copy** of the source array. Write a `main()` that clones an array, modifies the original, and proves the clone is unaffected.

### Exercise 12.4 🟡
Implement a simple **linked list** (a `Node` struct with `int data` and `Node* next`). Write functions to:
1. `push_front(Node*& head, int value)`
2. `print_list(Node* head)`
3. `free_list(Node*& head)`

Do not use `std::list`.

### Exercise 12.5 🟡
Create a function `int** createMatrix(int rows, int cols)` that allocates a 2D array dynamically. Write a matching `void freeMatrix(int** matrix, int rows)`. Test by filling and printing a 3×4 matrix.

### Exercise 12.6 🟡
Write a program that demonstrates the difference between `NULL`, `0`, and `nullptr` in the context of function overloading:

```cpp
void foo(int x);
void foo(char* p);
void foo(std::nullptr_t p);
```

Call `foo` with each of the three null values and observe which overload is selected.

### Exercise 12.7 🔴
Implement a simple **memory pool allocator**. Create a `MemoryPool` class that:
1. Pre-allocates a large block of memory
2. Provides `void* allocate(size_t)` that hands out fixed-size chunks
3. Provides `void deallocate(void*)` that returns chunks to a free list
4. Tracks allocated vs free chunks

Compare its performance against `new`/`delete` for allocating 1,000,000 small objects.
