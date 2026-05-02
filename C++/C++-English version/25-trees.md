[← Previous: Recursion](24-recursion.md) | [Next: Heap and Priority Queue →](26-heap-priority-queue.md)

# 25 Trees

A tree is a hierarchical data structure consisting of nodes connected by edges, with no cycles. Trees are fundamental for representing hierarchical data and enabling efficient searching.

## 25.1 Tree Basics

### Terminology

| Term | Definition |
|------|------------|
| **Root** | Topmost node with no parent |
| **Parent** | Node directly above another node |
| **Child** | Node directly below another node |
| **Siblings** | Nodes with the same parent |
| **Leaf** | Node with no children |
| **Internal Node** | Node with at least one child |
| **Edge** | Connection between two nodes |
| **Path** | Sequence of edges between nodes |
| **Height** | Longest path from node to leaf |
| **Depth** | Distance from root to node |
| **Level** | All nodes at the same depth |
| **Subtree** | Tree formed by a node and its descendants |

### Tree Node Structure

```cpp
struct TreeNode {
    int data;
    TreeNode* firstChild;   // First child
    TreeNode* nextSibling;  // Next sibling
    
    TreeNode(int val) : data(val), 
        firstChild(nullptr), nextSibling(nullptr) {}
};
```

Or with children list:

```cpp
struct TreeNode {
    int data;
    vector<TreeNode*> children;
    
    TreeNode(int val) : data(val) {}
};
```

## 25.2 Binary Trees

A binary tree is a tree where each node has at most two children (left and right).

### Binary Tree Node

```cpp
struct BinaryTreeNode {
    int data;
    BinaryTreeNode* left;
    BinaryTreeNode* right;
    
    BinaryTreeNode(int val) : data(val), 
        left(nullptr), right(nullptr) {}
};
```

### Types of Binary Trees

| Type | Property |
|------|----------|
| **Full** | Every node has 0 or 2 children |
| **Complete** | All levels filled except possibly last, filled left to right |
| **Perfect** | All internal nodes have 2 children, all leaves same depth |
| **Balanced** | Height difference between subtrees ≤ 1 |
| **Degenerate** | Each node has only one child (like linked list) |

## 25.3 Binary Tree Traversals

### Depth-First Traversals

```cpp
// Preorder: Root → Left → Right
void preorder(BinaryTreeNode* root) {
    if (!root) return;
    cout << root->data << " ";    // Visit root
    preorder(root->left);          // Traverse left
    preorder(root->right);         // Traverse right
}

// Inorder: Left → Root → Right
void inorder(BinaryTreeNode* root) {
    if (!root) return;
    inorder(root->left);           // Traverse left
    cout << root->data << " ";    // Visit root
    inorder(root->right);          // Traverse right
}

// Postorder: Left → Right → Root
void postorder(BinaryTreeNode* root) {
    if (!root) return;
    postorder(root->left);         // Traverse left
    postorder(root->right);        // Traverse right
    cout << root->data << " ";    // Visit root
}
```

### Breadth-First (Level Order)

```cpp
void levelOrder(BinaryTreeNode* root) {
    if (!root) return;
    
    queue<BinaryTreeNode*> q;
    q.push(root);
    
    while (!q.empty()) {
        BinaryTreeNode* curr = q.front();
        q.pop();
        cout << curr->data << " ";
        
        if (curr->left) q.push(curr->left);
        if (curr->right) q.push(curr->right);
    }
}
```

### Traversal Applications

| Traversal | Use Case |
|-----------|----------|
| Preorder | Copy tree, prefix expression |
| Inorder | BST sorting (yields sorted order) |
| Postorder | Delete tree, postfix expression |
| Level Order | BFS, find shortest path |

## 25.4 Binary Search Trees (BST)

BST property: Left subtree values < root < right subtree values.

### BST Operations

```cpp
class BST {
    BinaryTreeNode* root;
    
    BinaryTreeNode* insert(BinaryTreeNode* node, int val) {
        if (!node) return new BinaryTreeNode(val);
        
        if (val < node->data)
            node->left = insert(node->left, val);
        else if (val > node->data)
            node->right = insert(node->right, val);
        
        return node;
    }
    
    BinaryTreeNode* search(BinaryTreeNode* node, int val) {
        if (!node || node->data == val) return node;
        
        if (val < node->data)
            return search(node->left, val);
        return search(node->right, val);
    }
    
    BinaryTreeNode* findMin(BinaryTreeNode* node) {
        while (node && node->left)
            node = node->left;
        return node;
    }
    
    BinaryTreeNode* remove(BinaryTreeNode* node, int val) {
        if (!node) return nullptr;
        
        if (val < node->data)
            node->left = remove(node->left, val);
        else if (val > node->data)
            node->right = remove(node->right, val);
        else {
            // Node found
            if (!node->left) {
                BinaryTreeNode* temp = node->right;
                delete node;
                return temp;
            }
            if (!node->right) {
                BinaryTreeNode* temp = node->left;
                delete node;
                return temp;
            }
            
            // Two children: find inorder successor
            BinaryTreeNode* temp = findMin(node->right);
            node->data = temp->data;
            node->right = remove(node->right, temp->data);
        }
        return node;
    }
    
public:
    BST() : root(nullptr) {}
    void insert(int val) { root = insert(root, val); }
    bool search(int val) { return search(root, val) != nullptr; }
    void remove(int val) { root = remove(root, val); }
};
```

### BST Complexity

| Operation | Average | Worst (degenerate) |
|-----------|---------|-------------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

## 25.5 Self-Balancing BSTs

### AVL Tree

Height-balanced BST: difference between subtrees ≤ 1.

```cpp
struct AVLNode {
    int data, height;
    AVLNode *left, *right;
    
    AVLNode(int val) : data(val), height(1), 
        left(nullptr), right(nullptr) {}
};

int height(AVLNode* node) {
    return node ? node->height : 0;
}

int balanceFactor(AVLNode* node) {
    return height(node->left) - height(node->right);
}

void updateHeight(AVLNode* node) {
    node->height = 1 + max(height(node->left), 
                           height(node->right));
}

// Right rotation
AVLNode* rotateRight(AVLNode* y) {
    AVLNode* x = y->left;
    AVLNode* T2 = x->right;
    
    x->right = y;
    y->left = T2;
    
    updateHeight(y);
    updateHeight(x);
    
    return x;
}

// Left rotation
AVLNode* rotateLeft(AVLNode* x) {
    AVLNode* y = x->right;
    AVLNode* T2 = y->left;
    
    y->left = x;
    x->right = T2;
    
    updateHeight(x);
    updateHeight(y);
    
    return y;
}

AVLNode* insert(AVLNode* node, int val) {
    if (!node) return new AVLNode(val);
    
    if (val < node->data)
        node->left = insert(node->left, val);
    else if (val > node->data)
        node->right = insert(node->right, val);
    else
        return node;  // Duplicate
    
    updateHeight(node);
    
    int balance = balanceFactor(node);
    
    // Left Left
    if (balance > 1 && val < node->left->data)
        return rotateRight(node);
    
    // Right Right
    if (balance < -1 && val > node->right->data)
        return rotateLeft(node);
    
    // Left Right
    if (balance > 1 && val > node->left->data) {
        node->left = rotateLeft(node->left);
        return rotateRight(node);
    }
    
    // Right Left
    if (balance < -1 && val < node->right->data) {
        node->right = rotateRight(node->right);
        return rotateLeft(node);
    }
    
    return node;
}
```

### Red-Black Tree

Self-balancing BST with color properties ensuring O(log n) operations.

**Properties:**
1. Every node is either red or black
2. Root is black
3. All leaves (NIL) are black
4. Red nodes have black children
5. All paths from node to leaves have same black count

Used in `std::map` and `std::set`.

## 25.6 Tree Properties and Algorithms

### Tree Height

```cpp
int treeHeight(BinaryTreeNode* root) {
    if (!root) return -1;  // or 0 for leaf height = 1
    return 1 + max(treeHeight(root->left), 
                   treeHeight(root->right));
}
```

### Count Nodes

```cpp
int countNodes(BinaryTreeNode* root) {
    if (!root) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}
```

### Check if Balanced

```cpp
bool isBalanced(BinaryTreeNode* root) {
    if (!root) return true;
    
    int leftH = treeHeight(root->left);
    int rightH = treeHeight(root->right);
    
    return abs(leftH - rightH) <= 1 &&
           isBalanced(root->left) &&
           isBalanced(root->right);
}

// Optimized O(n) version
int checkHeight(BinaryTreeNode* root) {
    if (!root) return 0;
    
    int leftH = checkHeight(root->left);
    if (leftH == -1) return -1;
    
    int rightH = checkHeight(root->right);
    if (rightH == -1) return -1;
    
    if (abs(leftH - rightH) > 1) return -1;
    
    return 1 + max(leftH, rightH);
}
```

### Lowest Common Ancestor (LCA)

```cpp
BinaryTreeNode* findLCA(BinaryTreeNode* root, int n1, int n2) {
    if (!root) return nullptr;
    
    if (root->data == n1 || root->data == n2)
        return root;
    
    BinaryTreeNode* leftLCA = findLCA(root->left, n1, n2);
    BinaryTreeNode* rightLCA = findLCA(root->right, n1, n2);
    
    if (leftLCA && rightLCA) return root;
    
    return leftLCA ? leftLCA : rightLCA;
}
```

## 25.7 Expression Trees

Binary trees representing arithmetic expressions.

```cpp
// Infix: (3 + 4) * 5
// Postfix: 3 4 + 5 *

int evaluate(BinaryTreeNode* root) {
    if (!root) return 0;
    
    if (!root->left && !root->right)
        return root->data;  // Operand
    
    int leftVal = evaluate(root->left);
    int rightVal = evaluate(root->right);
    
    switch (root->data) {
        case '+': return leftVal + rightVal;
        case '-': return leftVal - rightVal;
        case '*': return leftVal * rightVal;
        case '/': return leftVal / rightVal;
    }
    return 0;
}
```

## 25.8 Trie (Prefix Tree)

Tree for storing strings with common prefixes.

```cpp
struct TrieNode {
    TrieNode* children[26];
    bool isEndOfWord;
    
    TrieNode() : isEndOfWord(false) {
        for (int i = 0; i < 26; i++)
            children[i] = nullptr;
    }
};

class Trie {
    TrieNode* root;
    
public:
    Trie() { root = new TrieNode(); }
    
    void insert(const string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!curr->children[idx])
                curr->children[idx] = new TrieNode();
            curr = curr->children[idx];
        }
        curr->isEndOfWord = true;
    }
    
    bool search(const string& word) {
        TrieNode* node = findNode(word);
        return node && node->isEndOfWord;
    }
    
    bool startsWith(const string& prefix) {
        return findNode(prefix) != nullptr;
    }
    
private:
    TrieNode* findNode(const string& str) {
        TrieNode* curr = root;
        for (char c : str) {
            int idx = c - 'a';
            if (!curr->children[idx]) return nullptr;
            curr = curr->children[idx];
        }
        return curr;
    }
};
```

## 25.9 Segment Tree

For range queries and updates.

```cpp
class SegmentTree {
    vector<int> tree;
    int n;
    
    void build(vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2*node, start, mid);
            build(arr, 2*node+1, mid+1, end);
            tree[node] = tree[2*node] + tree[2*node+1];
        }
    }
    
    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        
        int mid = (start + end) / 2;
        return query(2*node, start, mid, l, r) +
               query(2*node+1, mid+1, end, l, r);
    }
    
public:
    SegmentTree(vector<int>& arr) {
        n = arr.size();
        tree.resize(4 * n);
        build(arr, 1, 0, n-1);
    }
    
    int query(int l, int r) { return query(1, 0, n-1, l, r); }
};
```

## 25.10 Summary

### Tree Types Comparison

| Tree Type | Search | Insert | Delete | Balanced? |
|-----------|--------|--------|--------|-----------|
| Binary Tree | O(n) | O(n) | O(n) | No |
| BST | O(log n) avg | O(log n) avg | O(log n) avg | No |
| AVL | O(log n) | O(log n) | O(log n) | Yes |
| Red-Black | O(log n) | O(log n) | O(log n) | Yes |
| Trie | O(L) | O(L) | O(L) | N/A |

*L = string length*

### Key Concepts

1. **Binary Tree**: At most 2 children per node
2. **BST**: Left < Root < Right enables O(log n) search
3. **Self-balancing**: Rotations maintain O(log n) operations
4. **Traversals**: Pre/In/Post-order, Level-order
5. **Applications**: Searching, expression evaluation, autocomplete, range queries

[← Previous: Recursion](24-recursion.md) | [Next: Heap and Priority Queue →](26-heap-priority-queue.md)
