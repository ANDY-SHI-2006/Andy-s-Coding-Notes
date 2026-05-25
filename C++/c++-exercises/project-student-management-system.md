# Capstone Project: Student Management System

## Overview

This project is designed to consolidate concepts from **all four phases** of the C++ notes. You will build a command-line student management system incrementally, starting from a minimal working version and adding features one by one.

## Learning Objectives

By completing this project, you will demonstrate mastery of:
- **Phase 1:** Variables, control flow, functions, OOP, pointers, STL
- **Phase 2:** Data structures (lists, trees, hash tables), sorting, file I/O
- **Phase 3:** Templates, exceptions, smart pointers, lambdas, move semantics
- **Phase 4:** Multi-file organization, build systems, multithreading (optional)

---

## Phase A: Core System (Minimal Viable Product)

### Requirements

Implement a `Student` class with:
- `id` (int), `name` (string), `gpa` (double)
- Constructor, getters, setters
- `toString()` method for display

Implement a simple in-memory database using `std::vector<Student>`:
- `addStudent(Student)` — add to vector
- `removeStudent(int id)` — remove by ID
- `findStudent(int id)` — return pointer or optional
- `listAllStudents()` — print all students
- `saveToFile(const std::string& filename)` — write to text file
- `loadFromFile(const std::string& filename)` — read from text file

### Deliverables

- Single `.cpp` file that compiles and runs
- Command-line menu (1=Add, 2=Remove, 3=Find, 4=List, 5=Save, 6=Load, 0=Exit)
- Data persists across sessions via file I/O

---

## Phase B: OOP and Data Structures

### Requirements

Refactor the system:

1. **Replace `std::vector` with a custom `StudentList`**
   - Implement using a singly linked list (from Chapter 14)
   - Maintain students sorted by ID
   - `insert` must find the correct position

2. **Add a `Course` class**
   - `courseCode`, `courseName`, `maxCapacity`
   - `enrollStudent(int studentId)` — check capacity
   - `getEnrolledStudents()` — return list of student IDs

3. **Add enrollment relationships**
   - A student can enroll in multiple courses
   - A course has multiple enrolled students
   - Use `std::map<int, std::vector<int>>` or your own data structure

4. **Implement search by name**
   - Case-insensitive substring search
   - Return all matching students

### Deliverables

- `Student` and `Course` classes with proper encapsulation
- Custom linked list implementation for student storage
- Search functionality
- Updated CLI menu

---

## Phase C: Algorithms and Analysis

### Requirements

1. **Add sorting options**
   - Sort by ID (default)
   - Sort by name (alphabetical)
   - Sort by GPA (descending)
   - Allow user to choose sorting algorithm: bubble, merge, or quicksort
   - Measure and display time taken for each sort

2. **Add grade statistics**
   - Class average GPA
   - Median GPA
   - Standard deviation
   - Honor roll (top 10% by GPA)

3. **Implement a BST index**
   - Build a binary search tree keyed by student ID
   - Use it to accelerate `findStudent` from $O(n)$ to $O(\log n)$
   - Compare search times with and without the index

### Deliverables

- Multiple sorting algorithms with timing
- Statistical analysis
- BST-based indexing
- Performance comparison report

---

## Phase D: Modern C++ and Engineering

### Requirements

1. **Split into multiple files**
   - `student.hpp` / `student.cpp`
   - `course.hpp` / `course.cpp`
   - `database.hpp` / `database.cpp`
   - `utils.hpp` / `utils.cpp`
   - `main.cpp`
   - `CMakeLists.txt`

2. **Use smart pointers**
   - Replace raw pointers with `std::unique_ptr` or `std::shared_ptr`
   - Ensure no memory leaks

3. **Add exception handling**
   - `StudentNotFoundError`
   - `CourseFullError`
   - `InvalidDataError`
   - All file operations must handle I/O errors

4. **Use templates**
   - Make your linked list a template `TList<T>`
   - Store both `Student` and `Course` objects

5. **Add regex validation**
   - Validate student IDs (format: `S\d{6}`)
   - Validate names (alphabetic characters and spaces only)
   - Validate course codes (format: `CS\d{3}`)

6. **(Optional) Add multithreading**
   - Background auto-save every 30 seconds
   - Parallel sorting using `std::async`

### Deliverables

- Multi-file project with CMake build
- No raw pointers (smart pointers only)
- Comprehensive exception handling
- Template-based data structures
- Input validation with regex
- Clean separation of concerns

---

## Bonus Challenges

### Challenge 1: Persistence Layer 🔴
Replace text file storage with a simple binary format. Implement serialization using `std::ofstream` with `write()` / `read()`. Handle endianness and versioning.

### Challenge 2: Undo/Redo System 🔴
Implement a command pattern with undo/redo. Every operation (add, remove, edit) is stored as a command object. Maintain two stacks: undo and redo.

### Challenge 3: REST API Simulation 🔴
Instead of a CLI menu, read commands from a text file ("batch mode") where each line is a command like `ADD {"id":1,"name":"Alice","gpa":3.8}`. Parse JSON-like input using string manipulation.

### Challenge 4: Memory-Efficient Large Dataset 🔴
Load 1,000,000 students from a file. Optimize memory usage by:
- Using `std::string_view` for names (if names repeat)
- Custom memory pool for `Student` objects
- Lazy loading of course enrollment data

---

## Evaluation Checklist

| Feature | Phase A | Phase B | Phase C | Phase D |
|---------|---------|---------|---------|---------|
| Compiles without warnings | ✅ | ✅ | ✅ | ✅ |
| No memory leaks | ✅ | ✅ | ✅ | ✅ |
| Proper error handling | — | — | ✅ | ✅ |
| Multi-file structure | — | — | — | ✅ |
| CMake build | — | — | — | ✅ |
| Smart pointers | — | — | — | ✅ |
| Templates | — | — | — | ✅ |
| Regex validation | — | — | — | ✅ |
| Unit tests | — | — | — | ✅ |

---

## Suggested Timeline

| Week | Focus |
|------|-------|
| 1 | Complete Phase A (single-file CLI) |
| 2 | Complete Phase B (OOP + data structures) |
| 3 | Complete Phase C (algorithms + analysis) |
| 4 | Complete Phase D (engineering + modern C++) |
| 5 | Polish, test, and attempt bonus challenges |

> **Tip:** Do not attempt to write the entire system at once. Start with Phase A, ensure it works perfectly, then incrementally add features. The refactoring in Phase D is intentionally challenging — it simulates real-world legacy code modernization.
