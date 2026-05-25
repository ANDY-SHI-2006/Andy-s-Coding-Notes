# Solutions: Capstone Project -- Student Management System

This solution provides a reference implementation for the Student Management System project. It demonstrates all four phases in a progressive, incremental manner.

---

## Phase A: Core System (Single File)

**Approach:** Start with a minimal, working CLI application using basic C++ features.

```cpp
// student_mgmt_v1.cpp
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iomanip>

class Student {
    int id;
    std::string name;
    double gpa;

public:
    Student(int i = 0, const std::string& n = "", double g = 0.0)
        : id(i), name(n), gpa(g) {}

    int getId() const { return id; }
    std::string getName() const { return name; }
    double getGpa() const { return gpa; }
    void setGpa(double g) { gpa = g; }

    std::string toString() const {
        std::ostringstream oss;
        oss << "ID: " << id << ", Name: " << name << ", GPA: " << std::fixed << std::setprecision(2) << gpa;
        return oss.str();
    }
};

class StudentDatabase {
    std::vector<Student> students;

public:
    void addStudent(const Student& s) { students.push_back(s); }

    bool removeStudent(int id) {
        for (auto it = students.begin(); it != students.end(); ++it) {
            if (it->getId() == id) {
                students.erase(it);
                return true;
            }
        }
        return false;
    }

    const Student* findStudent(int id) const {
        for (const auto& s : students)
            if (s.getId() == id) return &s;
        return nullptr;
    }

    void listAll() const {
        for (const auto& s : students)
            std::cout << s.toString() << "\n";
    }

    void saveToFile(const std::string& filename) const {
        std::ofstream file(filename);
        for (const auto& s : students)
            file << s.getId() << "," << s.getName() << "," << s.getGpa() << "\n";
    }

    void loadFromFile(const std::string& filename) {
        students.clear();
        std::ifstream file(filename);
        std::string line;
        while (std::getline(file, line)) {
            std::istringstream iss(line);
            int id; std::string name; double gpa;
            char comma;
            iss >> id >> comma;
            std::getline(iss, name, ',');
            iss >> gpa;
            students.emplace_back(id, name, gpa);
        }
    }

    size_t size() const { return students.size(); }
};

void showMenu() {
    std::cout << "\n1. Add Student\n2. Remove Student\n3. Find Student\n"
              << "4. List All\n5. Save\n6. Load\n0. Exit\nChoice: ";
}

int main() {
    StudentDatabase db;
    int choice;
    do {
        showMenu();
        std::cin >> choice;
        std::cin.ignore();

        if (choice == 1) {
            int id; std::string name; double gpa;
            std::cout << "ID: "; std::cin >> id;
            std::cin.ignore();
            std::cout << "Name: "; std::getline(std::cin, name);
            std::cout << "GPA: "; std::cin >> gpa;
            db.addStudent(Student(id, name, gpa));
        } else if (choice == 2) {
            int id; std::cout << "ID to remove: "; std::cin >> id;
            std::cout << (db.removeStudent(id) ? "Removed.\n" : "Not found.\n");
        } else if (choice == 3) {
            int id; std::cout << "ID to find: "; std::cin >> id;
            auto* s = db.findStudent(id);
            std::cout << (s ? s->toString() : "Not found") << "\n";
        } else if (choice == 4) {
            db.listAll();
        } else if (choice == 5) {
            db.saveToFile("students.txt");
        } else if (choice == 6) {
            db.loadFromFile("students.txt");
        }
    } while (choice != 0);

    return 0;
}
```

---

## Phase B: OOP and Data Structures

**Approach:** Replace vector with sorted linked list, add Course class.

```cpp
// student.hpp
#ifndef STUDENT_HPP
#define STUDENT_HPP
#include <string>

class Student {
    int id;
    std::string name;
    double gpa;
public:
    Student(int i = 0, const std::string& n = "", double g = 0.0);
    int getId() const;
    std::string getName() const;
    double getGpa() const;
    void setGpa(double g);
    std::string toString() const;
    bool operator<(const Student& other) const;
};

#endif
```

```cpp
// student.cpp
#include "student.hpp"
#include <sstream>
#include <iomanip>

Student::Student(int i, const std::string& n, double g) : id(i), name(n), gpa(g) {}
int Student::getId() const { return id; }
std::string Student::getName() const { return name; }
double Student::getGpa() const { return gpa; }
void Student::setGpa(double g) { gpa = g; }

std::string Student::toString() const {
    std::ostringstream oss;
    oss << "ID: " << id << ", Name: " << name
        << ", GPA: " << std::fixed << std::setprecision(2) << gpa;
    return oss.str();
}

bool Student::operator<(const Student& other) const {
    return id < other.id;
}
```

```cpp
// student_list.hpp
#ifndef STUDENT_LIST_HPP
#define STUDENT_LIST_HPP
#include "student.hpp"

struct StudentNode {
    Student data;
    StudentNode* next;
    StudentNode(const Student& s) : data(s), next(nullptr) {}
};

class StudentList {
    StudentNode* head;
    size_t count;
public:
    StudentList();
    ~StudentList();
    void insert(const Student& s);  // Maintains sorted order by ID
    bool remove(int id);
    const Student* find(int id) const;
    void printAll() const;
    size_t size() const;
    StudentNode* getHead() const { return head; }
};

#endif
```

```cpp
// student_list.cpp
#include "student_list.hpp"
#include <iostream>

StudentList::StudentList() : head(nullptr), count(0) {}

StudentList::~StudentList() {
    while (head) {
        StudentNode* temp = head;
        head = head->next;
        delete temp;
    }
}

void StudentList::insert(const Student& s) {
    StudentNode* node = new StudentNode(s);
    if (!head || s < head->data) {
        node->next = head;
        head = node;
    } else {
        StudentNode* curr = head;
        while (curr->next && curr->next->data < s)
            curr = curr->next;
        node->next = curr->next;
        curr->next = node;
    }
    ++count;
}

bool StudentList::remove(int id) {
    if (!head) return false;
    if (head->data.getId() == id) {
        StudentNode* temp = head;
        head = head->next;
        delete temp;
        --count;
        return true;
    }
    StudentNode* curr = head;
    while (curr->next && curr->next->data.getId() != id)
        curr = curr->next;
    if (!curr->next) return false;
    StudentNode* temp = curr->next;
    curr->next = temp->next;
    delete temp;
    --count;
    return true;
}

const Student* StudentList::find(int id) const {
    for (StudentNode* curr = head; curr; curr = curr->next)
        if (curr->data.getId() == id) return &curr->data;
    return nullptr;
}

void StudentList::printAll() const {
    for (StudentNode* curr = head; curr; curr = curr->next)
        std::cout << curr->data.toString() << "\n";
}

size_t StudentList::size() const { return count; }
```

```cpp
// course.hpp
#ifndef COURSE_HPP
#define COURSE_HPP
#include <string>
#include <vector>

class Course {
    std::string code;
    std::string name;
    int maxCapacity;
    std::vector<int> enrolledIds;
public:
    Course(const std::string& c, const std::string& n, int cap);
    bool enrollStudent(int studentId);
    const std::vector<int>& getEnrolledStudents() const;
    std::string getCode() const;
    int getCapacity() const;
    int getEnrollmentCount() const;
};

#endif
```

---

## Phase C: Algorithms and Analysis

**Approach:** Add sorting, statistics, and BST indexing.

```cpp
// sorting.hpp
#ifndef SORTING_HPP
#define SORTING_HPP
#include <vector>
#include "student.hpp"
#include <functional>

using Comparator = std::function<bool(const Student&, const Student&)>;

void bubbleSort(std::vector<Student>& arr, Comparator comp);
void mergeSort(std::vector<Student>& arr, int left, int right, Comparator comp);
void quickSort(std::vector<Student>& arr, int left, int right, Comparator comp);

#endif
```

```cpp
// bst_index.hpp
#ifndef BST_INDEX_HPP
#define BST_INDEX_HPP
#include "student.hpp"

struct BSTNode {
    int id;
    const Student* student;
    BSTNode* left;
    BSTNode* right;
    BSTNode(int i, const Student* s) : id(i), student(s), left(nullptr), right(nullptr) {}
};

class BSTIndex {
    BSTNode* root;
    void insert(BSTNode*& node, int id, const Student* s);
    const Student* search(BSTNode* node, int id) const;
    void clear(BSTNode* node);
public:
    BSTIndex() : root(nullptr) {}
    ~BSTIndex() { clear(root); }
    void insert(int id, const Student* s);
    const Student* find(int id) const;
};

#endif
```

```cpp
// statistics.hpp
#ifndef STATISTICS_HPP
#define STATISTICS_HPP
#include <vector>
#include "student.hpp"

struct Stats {
    double average;
    double median;
    double stdDev;
};

Stats computeStats(const std::vector<Student>& students);
std::vector<Student> getHonorRoll(const std::vector<Student>& students, double topPercent);

#endif
```

---

## Phase D: Modern C++ and Engineering

**Approach:** Multi-file project with CMake, smart pointers, exceptions, templates, and regex.

```cpp
// exceptions.hpp
#ifndef EXCEPTIONS_HPP
#define EXCEPTIONS_HPP
#include <stdexcept>
#include <string>

class StudentNotFoundError : public std::runtime_error {
public:
    StudentNotFoundError(int id) : std::runtime_error("Student not found: " + std::to_string(id)) {}
};

class CourseFullError : public std::runtime_error {
public:
    CourseFullError(const std::string& code) : std::runtime_error("Course full: " + code) {}
};

class InvalidDataError : public std::invalid_argument {
public:
    InvalidDataError(const std::string& msg) : std::invalid_argument(msg) {}
};

#endif
```

```cpp
// validator.hpp
#ifndef VALIDATOR_HPP
#define VALIDATOR_HPP
#include <string>
#include <regex>

inline bool isValidStudentId(const std::string& id) {
    return std::regex_match(id, std::regex(R"(S\d{6})"));
}

inline bool isValidName(const std::string& name) {
    return std::regex_match(name, std::regex(R"([A-Za-z\s]+)"));
}

inline bool isValidCourseCode(const std::string& code) {
    return std::regex_match(code, std::regex(R"(CS\d{3})"));
}

#endif
```

```cpp
// tlist.hpp -- Template linked list
#ifndef TLIST_HPP
#define TLIST_HPP
#include <memory>

template <typename T>
class TList {
    struct Node {
        T data;
        std::unique_ptr<Node> next;
        Node(const T& d) : data(d), next(nullptr) {}
    };
    std::unique_ptr<Node> head;
    size_t count;

public:
    TList() : head(nullptr), count(0) {}

    void push_front(const T& value) {
        auto node = std::make_unique<Node>(value);
        node->next = std::move(head);
        head = std::move(node);
        ++count;
    }

    bool remove(const T& value) {
        if (!head) return false;
        if (head->data == value) {
            head = std::move(head->next);
            --count;
            return true;
        }
        Node* curr = head.get();
        while (curr->next && !(curr->next->data == value))
            curr = curr->next;
        if (!curr->next) return false;
        curr->next = std::move(curr->next->next);
        --count;
        return true;
    }

    size_t size() const { return count; }

    class Iterator {
        Node* curr;
    public:
        Iterator(Node* n) : curr(n) {}
        T& operator*() { return curr->data; }
        Iterator& operator++() { curr = curr->next.get(); return *this; }
        bool operator!=(const Iterator& other) const { return curr != other.curr; }
    };

    Iterator begin() { return Iterator(head.get()); }
    Iterator end() { return Iterator(nullptr); }
};

#endif
```

```cpp
// database.hpp
#ifndef DATABASE_HPP
#define DATABASE_HPP
#include <vector>
#include <memory>
#include <map>
#include "student.hpp"
#include "course.hpp"
#include "bst_index.hpp"
#include "exceptions.hpp"

class Database {
    std::vector<std::unique_ptr<Student>> students;
    std::map<std::string, std::unique_ptr<Course>> courses;
    BSTIndex index;
    mutable std::string lastError;

public:
    void addStudent(std::unique_ptr<Student> student);
    void removeStudent(int id);
    const Student* findStudent(int id) const;
    std::vector<const Student*> searchByName(const std::string& query) const;
    void listAllStudents() const;
    void saveToFile(const std::string& filename) const;
    void loadFromFile(const std::string& filename);

    void addCourse(std::unique_ptr<Course> course);
    void enrollStudentInCourse(int studentId, const std::string& courseCode);

    size_t getStudentCount() const;
    const std::vector<std::unique_ptr<Student>>& getAllStudents() const;
};

#endif
```

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.15)
project(StudentManagement)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")

add_executable(student_mgmt
    main.cpp
    student.cpp
    student_list.cpp
    course.cpp
    database.cpp
    sorting.cpp
    bst_index.cpp
    statistics.cpp
    validator.cpp
)

# Optional: enable testing
enable_testing()
add_subdirectory(tests)
```

---

## Bonus Challenge 1: Binary Persistence

```cpp
// serialization.hpp
#ifndef SERIALIZATION_HPP
#define SERIALIZATION_HPP
#include <fstream>
#include "student.hpp"

// Simple binary format: [version:4][count:4][records...]
// Each record: [id:4][nameLen:4][name:nameLen][gpa:8]

const int FORMAT_VERSION = 1;

void saveBinary(const std::vector<Student*>& students, const std::string& filename);
std::vector<std::unique_ptr<Student>> loadBinary(const std::string& filename);

#endif
```

---

## Bonus Challenge 2: Undo/Redo System

```cpp
// command.hpp
#ifndef COMMAND_HPP
#define COMMAND_HPP
#include <memory>
#include <stack>
#include "database.hpp"

class Command {
public:
    virtual void execute(Database& db) = 0;
    virtual void undo(Database& db) = 0;
    virtual ~Command() = default;
};

class AddStudentCommand : public Command {
    std::unique_ptr<Student> student;
public:
    AddStudentCommand(std::unique_ptr<Student> s) : student(std::move(s)) {}
    void execute(Database& db) override { db.addStudent(std::make_unique<Student>(*student)); }
    void undo(Database& db) override { db.removeStudent(student->getId()); }
};

class CommandManager {
    std::stack<std::unique_ptr<Command>> undoStack;
    std::stack<std::unique_ptr<Command>> redoStack;
public:
    void execute(std::unique_ptr<Command> cmd, Database& db);
    void undo(Database& db);
    void redo(Database& db);
    bool canUndo() const { return !undoStack.empty(); }
    bool canRedo() const { return !redoStack.empty(); }
};

#endif
```

---

## Bonus Challenge 3: Batch Mode

```cpp
// batch_parser.hpp
#ifndef BATCH_PARSER_HPP
#define BATCH_PARSER_HPP
#include <string>
#include <vector>
#include <map>

std::map<std::string, std::string> parseJsonLike(const std::string& json);

#endif
```

```cpp
// batch_parser.cpp
#include "batch_parser.hpp"
#include <sstream>
#include <regex>

std::map<std::string, std::string> parseJsonLike(const std::string& json) {
    std::map<std::string, std::string> result;
    std::regex pattern(R"((\w+)\s*:\s*"?([^",\}]*)"?)");
    auto begin = std::sregex_iterator(json.begin(), json.end(), pattern);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; ++it)
        result[(*it)[1]] = (*it)[2];
    return result;
}
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `std::unique_ptr` for ownership | Prevents memory leaks, clear ownership semantics |
| `BSTIndex` for fast lookup | O(log n) search vs O(n) linear scan |
| Template `TList<T>` | Reusable for both Student and Course |
| Exception hierarchy | Specific exceptions enable precise error handling |
| Regex validation | Input sanitization at the boundary |
| CMake build | Cross-platform, standard build tool |
| Command pattern for undo/redo | Classic design pattern, clean separation |

## Testing Strategy

```cpp
// tests/test_database.cpp
#include <cassert>
#include "database.hpp"

void testAddAndFind() {
    Database db;
    db.addStudent(std::make_unique<Student>(1, "Alice", 3.8));
    auto* s = db.findStudent(1);
    assert(s != nullptr);
    assert(s->getName() == "Alice");
}

void testRemove() {
    Database db;
    db.addStudent(std::make_unique<Student>(1, "Bob", 3.5));
    db.removeStudent(1);
    assert(db.findStudent(1) == nullptr);
}

void testSearchByName() {
    Database db;
    db.addStudent(std::make_unique<Student>(1, "Alice Smith", 3.8));
    db.addStudent(std::make_unique<Student>(2, "Bob Jones", 3.5));
    auto results = db.searchByName("Alice");
    assert(results.size() == 1);
    assert(results[0]->getName() == "Alice Smith");
}

int main() {
    testAddAndFind();
    testRemove();
    testSearchByName();
    std::cout << "All tests passed!\n";
    return 0;
}
```
