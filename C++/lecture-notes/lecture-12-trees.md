# Lecture 12: Trees

> **Source**: Data Structure and Programming Methodology  
> **Instructor**: Dr. Peidong Liu, Faculty of Engineering, Westlake University  
> **Semester**: Spring 2026  
> **Corresponding Course Chapter**: [Ch 19 Trees](../c++-english-version/phase2-data-structures-algorithms/19-trees.md)

---

## Table of Contents

1. [Tree Fundamentals](#1-tree-fundamentals)
2. [Types of Trees](#2-types-of-trees)
3. [Tree Implementation](#3-tree-implementation)
4. [Recursive Properties](#4-recursive-properties)
5. [Binary Tree Traversals](#5-binary-tree-traversals)
6. [Expression Trees](#6-expression-trees)
7. [Binary Search Trees (BST)](#7-binary-search-trees-bst)
8. [Applications of BST](#8-applications-of-bst)

---

## 1. Tree Fundamentals

### Definitions

- **Node**: A data object in a tree (the circles).
- **Edge**: A link between two nodes.
- **Root**: The topmost node; the only node without a parent.
- **Parent / Child**: If there is an edge from A to B, A is the parent of B, and B is a child of A.
- **Siblings**: Nodes that share the same parent.
- **Ancestor / Descendant**: Node X is an ancestor of Y if X is a parent of Y, or X is a parent of some Z and Z is an ancestor of Y.
- **Leaf**: A node with no children.
- **Subtree**: A tree formed by a node and all of its descendants.

### Key Properties

| Property | Definition |
|----------|------------|
| **Level** | Number of nodes on the path from the root to the node. Root is at level 1. |
| **Height** | Maximum level among all nodes in the tree. |
| **Size** | Total number of nodes in the tree. |

> **Recursive Insight**: A tree is either empty, or a node with a set of subtrees, each of which is itself a tree.

### Applications

- **File systems**: Directories and subdirectories form a natural hierarchy.
- **Organization charts**: Manager → Employee relationships.
- **Arithmetic expressions**: Operators and operands can be represented hierarchically.

---

## 2. Types of Trees

### General Trees

An **n-ary tree** is a tree in which each node can have at most `n` children.

### Binary Trees

A **binary tree** is a tree in which each node has at most **2 children**.

#### Special Binary Trees

| Type | Definition |
|------|------------|
| **Full Binary Tree** | Every node has either 0 or 2 children. |
| **Complete Binary Tree** | All levels are fully filled except possibly the last, which is filled from left to right. |
| **Balanced Binary Tree** | For any node, the height difference between its left and right subtrees is at most 1. |

> **Note**: Every complete binary tree is balanced, but not every balanced tree is complete.

---

## 3. Tree Implementation

### Reference-Based (Pointer-Based)

```cpp
class TreeNode {
private:
    TreeItemType item;
    TreeNode *left;
    TreeNode *right;
    friend class BinaryTree;
};

class BinaryTree {
private:
    TreeNode *root;
};
```

### Array-Based (Static Representation)

```cpp
class TreeNode {
private:
    TreeItemType item;
    int left;   // index of left child
    int right;  // index of right child
};

class BinaryTree {
private:
    TreeNode tree[MAX_SIZE];
    int root;
    int free; // index of next free slot
};
```

### Array Representation of a Complete Binary Tree

For a complete binary tree stored in an array (0-indexed or 1-indexed), the parent-child relationships can be computed directly:

| Indexing | Parent of `i` | Left Child | Right Child |
|----------|---------------|------------|-------------|
| **0-indexed** | `(i - 1) / 2` | `2i + 1` | `2i + 2` |
| **1-indexed** | `i / 2` | `2i` | `2i + 1` |

This is the basis for the heap data structure (see Chapter 20).

---

## 4. Recursive Properties

### Height of a Tree

```
height(T):
    if T is empty:
        return 0
    else:
        return 1 + max(height(T.left), height(T.right))
```

### Size of a Tree

```
size(T):
    if T is empty:
        return 0
    else:
        return 1 + size(T.left) + size(T.right)
```

Both algorithms follow the **divide-and-conquer** paradigm: solve the problem for the left subtree, solve it for the right subtree, and combine the results.

---

## 5. Binary Tree Traversals

Traversal visits every node in a tree exactly once.

### Pre-order Traversal

Root → Left → Right

```
preorder(T):
    if T is not empty:
        process T.item
        preorder(T.left)
        preorder(T.right)
```

### In-order Traversal

Left → Root → Right

```
inorder(T):
    if T is not empty:
        inorder(T.left)
        process T.item
        inorder(T.right)
```

> **Key Property**: In-order traversal of a BST yields keys in **sorted ascending order**.

### Post-order Traversal

Left → Right → Root

```
postorder(T):
    if T is not empty:
        postorder(T.left)
        postorder(T.right)
        process T.item
```

### Level-order Traversal (BFS)

Visit nodes level by level, from left to right.

```
levelOrder(T):
    if T is empty:
        return
    Q = new Queue
    Q.enqueue(T.root)
    while Q is not empty:
        curr = Q.dequeue()
        process curr.item
        if curr.left is not empty:
            Q.enqueue(curr.left)
        if curr.right is not empty:
            Q.enqueue(curr.right)
```

**Time Complexity**: `O(n)` for all traversals.  
**Space Complexity**: `O(h)` for recursive traversals (call stack), `O(n)` for level-order (queue).

---

## 6. Expression Trees

An **expression tree** represents an arithmetic expression:
- **Leaf nodes** store operands.
- **Internal nodes** and the **root** store operators.

### Example

Expression: `(3 + 4) * 5`

```
        *
       / \
      +   5
     / \
    3   4
```

### Evaluating an Expression Tree

```
eval(T):
    if T is empty:
        return 0
    if T is a leaf:
        return value of T
    else if T.item is "+":
        return eval(T.left) + eval(T.right)
    else if T.item is "*":
        return eval(T.left) * eval(T.right)
    // extend for -, /, etc.
```

> **Question**: Do we need to consider operator priorities when evaluating an expression tree?  
> **Answer**: No — the tree structure itself encodes precedence. Operators closer to the root are evaluated later.

### Constructing an Expression Tree

Given a fully parenthesized infix expression, the operator with the **lowest precedence** (or the last operator outside parentheses) becomes the root. Its left and right sub-expressions become the left and right subtrees, respectively.

---

## 7. Binary Search Trees (BST)

A **Binary Search Tree** organizes data such that:
- All keys in the **left subtree** are **smaller** than the root.
- All keys in the **right subtree** are **larger** than the root.

### Searching

**Iterative:**

```
search(x, T):
    while T is not empty:
        if T.item == x:
            return T
        else if T.item > x:
            T = T.left
        else:
            T = T.right
    return null
```

**Recursive:**

```
search(x, T):
    if T is empty:
        return null
    if x == T.item:
        return T
    else if x < T.item:
        return search(x, T.left)
    else:
        return search(x, T.right)
```

### Finding Minimum / Maximum

```
findMin(T):
    while T.left is not empty:
        T = T.left
    return T.item
```

The maximum is found by following right children until a leaf.

### Insertion

```
insert(x, T):
    if T is empty:
        return new TreeNode(x)
    else if x < T.item:
        T.left = insert(x, T.left)
    else if x > T.item:
        T.right = insert(x, T.right)
    else:
        ERROR // duplicate key
    return T
```

### Deletion

Deletion has three cases:

#### Case 1: Node is a leaf
Simply remove it.

#### Case 2: Node has one child
Replace the node with its child.

#### Case 3: Node has two children
1. Find the **minimum element in the right subtree** (or maximum in the left).
2. Replace the node's value with that minimum.
3. Recursively delete the minimum from the right subtree.

```
delete(x, T):
    if T is empty:
        return T
    if x < T.item:
        T.left = delete(x, T.left)
    else if x > T.item:
        T.right = delete(x, T.right)
    else: // x == T.item
        if T.left is empty:
            return T.right
        else if T.right is empty:
            return T.left
        else:
            T.item = findMin(T.right)
            T.right = delete(T.item, T.right)
    return T
```

### Time Complexity

| Operation | Time |
|-----------|------|
| Search | `O(h)` |
| Insert | `O(h)` |
| Delete | `O(h)` |
| Find Min/Max | `O(h)` |

Where `h` is the height of the tree.

> **Important**: `h` is **not always** `O(log n)`. If keys are inserted in sorted order, the tree degenerates into a linked list with `h = O(n)`. This motivates self-balancing trees such as AVL and Red-Black trees (see Chapter 19).

---

## 8. Applications of BST

### Saving and Restoring a BST

#### Restore Original Shape

Use **pre-order traversal** to save the tree to a file, then rebuild by inserting nodes in that order.

#### Restore to a Balanced Shape

Use **in-order traversal** to save sorted keys to a file, then recursively rebuild:
1. Take the **middle element** as the root.
2. Recursively build the left subtree from the left half.
3. Recursively build the right subtree from the right half.

This produces a **height-balanced BST** with `h = O(log n)`.

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| Tree definition | Recursive structure of nodes and edges |
| Binary tree types | Full, complete, balanced |
| Implementation | Pointers for flexibility, arrays for complete trees |
| Traversals | Pre/In/Post (DFS) and Level-order (BFS with queue) |
| Expression tree | Leaves = operands, internal nodes = operators |
| BST property | Left < Root < Right |
| BST operations | Search, insert, delete all `O(h)` |
| Balanced rebuild | In-order → sorted array → middle-as-root recursion |

---

## Further Reading

- **Course Chapter**: [Ch 19 Trees](../c++-english-version/phase2-data-structures-algorithms/19-trees.md) — C++ implementations, AVL trees, and heap-based priority queues.
- **Course Chapter**: [Ch 20 Heap and Priority Queue](../c++-english-version/phase2-data-structures-algorithms/20-heap-priority-queue.md) — Array-based complete binary trees in practice.
