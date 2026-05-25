# Solutions: Phase 2 -- Algorithms (Chapters 16--22)

---

## Solution 16.1

**Approach:** Count iterations for each nested loop structure.

| Function | Complexity | Explanation |
|----------|-----------|-------------|
| f1 | **O(n^2)** | n * n iterations |
| f2 | **O(n^2)** | n + (n-1) + ... + 1 = n(n+1)/2 |
| f3 | **O(log n)** | i doubles each time: n/2^k = 1 |
| f4 | **O(n)** | Inner loop is constant (100) |

---

## Solution 16.2

**Simplification:** For n >= 10, n^2 dominates 100n + 50. By Big-O definition, there exists c=2 and n0=100 such that n^2 + 100n + 50 <= 2n^2 for all n >= n0.

**Linear Search Complexity:**
- **Worst case:** O(n) -- target is last element or not present
- **Best case:** O(1) -- target is first element
- **Average case:** O(n) -- target is at position n/2 on average

---

## Solution 16.3

**Approach:** Generate random arrays, sort with each algorithm, measure time.

```cpp
#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>

void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j+1]) {
                std::swap(arr[j], arr[j+1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void insertionSort(std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j+1] = arr[j];
            --j;
        }
        arr[j+1] = key;
    }
}

int main() {
    std::mt19937 gen(42);
    std::vector<int> sizes = {1000, 10000, 100000};

    for (int n : sizes) {
        std::uniform_int_distribution<> dist(1, n);
        std::vector<int> data(n);
        for (int& x : data) x = dist(gen);

        // Bubble sort (skip for large n)
        if (n <= 10000) {
            auto copy = data;
            auto start = std::chrono::high_resolution_clock::now();
            bubbleSort(copy);
            auto end = std::chrono::high_resolution_clock::now();
            auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
            std::cout << "Bubble n=" << n << ": " << ms.count() << " ms\n";
        }

        // Insertion sort
        auto copy2 = data;
        auto start2 = std::chrono::high_resolution_clock::now();
        insertionSort(copy2);
        auto end2 = std::chrono::high_resolution_clock::now();
        auto ms2 = std::chrono::duration_cast<std::chrono::milliseconds>(end2 - start2);
        std::cout << "Insertion n=" << n << ": " << ms2.count() << " ms\n";

        // std::sort
        auto copy3 = data;
        auto start3 = std::chrono::high_resolution_clock::now();
        std::sort(copy3.begin(), copy3.end());
        auto end3 = std::chrono::high_resolution_clock::now();
        auto ms3 = std::chrono::duration_cast<std::chrono::milliseconds>(end3 - start3);
        std::cout << "std::sort n=" << n << ": " << ms3.count() << " ms\n";
    }
    return 0;
}
```

**Expected results:** Bubble sort O(n^2) becomes unusable at n=100,000. std::sort (introsort) is O(n log n) and much faster.

---

## Solution 17.1

**Approach:** Add a `swapped` flag. Nearly-sorted arrays finish in one pass.

```cpp
#include <iostream>
#include <vector>

void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    int totalComparisons = 0, totalSwaps = 0;

    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; ++j) {
            ++totalComparisons;
            if (arr[j] > arr[j+1]) {
                std::swap(arr[j], arr[j+1]);
                ++totalSwaps;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
    std::cout << "Comparisons: " << totalComparisons
              << ", Swaps: " << totalSwaps << "\n";
}

int main() {
    std::vector<int> nearly = {1, 2, 3, 5, 4, 6, 7, 8};
    std::vector<int> reversed = {8, 7, 6, 5, 4, 3, 2, 1};

    std::cout << "Nearly sorted:\n";
    bubbleSort(nearly);  // ~7 comparisons, 1 swap

    std::cout << "Reversed:\n";
    bubbleSort(reversed); // ~28 comparisons, many swaps
    return 0;
}
```

---

## Solution 17.2

**Approach:** Remove nodes and reinsert in sorted position.

```cpp
#include <iostream>

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

Node* sortedInsert(Node* sorted, Node* newNode) {
    if (!sorted || newNode->data < sorted->data) {
        newNode->next = sorted;
        return newNode;
    }
    Node* curr = sorted;
    while (curr->next && curr->next->data < newNode->data)
        curr = curr->next;
    newNode->next = curr->next;
    curr->next = newNode;
    return sorted;
}

Node* insertionSort(Node* head) {
    Node* sorted = nullptr;
    Node* curr = head;
    while (curr) {
        Node* next = curr->next;
        sorted = sortedInsert(sorted, curr);
        curr = next;
    }
    return sorted;
}

void printList(Node* head) {
    while (head) { std::cout << head->data << " "; head = head->next; }
    std::cout << "\n";
}

int main() {
    Node* head = new Node(4);
    head->next = new Node(2);
    head->next->next = new Node(1);
    head->next->next->next = new Node(3);

    head = insertionSort(head);
    printList(head);  // 1 2 3 4
    return 0;
}
```

---

## Solution 17.3

**Approach:** Array: recursive divide and merge. Linked list: find middle with slow/fast pointer.

```cpp
#include <iostream>
#include <vector>

// Array version
void merge(std::vector<int>& arr, int left, int mid, int right) {
    std::vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;
    while (i <= mid && j <= right)
        temp[k++] = (arr[i] <= arr[j]) ? arr[i++] : arr[j++];
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    for (int p = 0; p < k; ++p) arr[left + p] = temp[p];
}

void mergeSort(std::vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

// Linked list version
struct ListNode {
    int data;
    ListNode* next;
    ListNode(int val) : data(val), next(nullptr) {}
};

ListNode* merge(ListNode* l1, ListNode* l2) {
    ListNode dummy(0);
    ListNode* tail = &dummy;
    while (l1 && l2) {
        if (l1->data <= l2->data) { tail->next = l1; l1 = l1->next; }
        else { tail->next = l2; l2 = l2->next; }
        tail = tail->next;
    }
    tail->next = l1 ? l1 : l2;
    return dummy.next;
}

ListNode* mergeSort(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode *slow = head, *fast = head->next;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* mid = slow->next;
    slow->next = nullptr;
    return merge(mergeSort(head), mergeSort(mid));
}
```

**Space complexity:** Array version O(n) auxiliary. Linked list version O(log n) stack space.

---

## Solution 17.4

**Approach:** Three pivot strategies. Median-of-three and random avoid worst case on sorted arrays.

```cpp
#include <iostream>
#include <vector>
#include <random>
#include <algorithm>

int partition(std::vector<int>& arr, int low, int high, int pivotIdx) {
    std::swap(arr[pivotIdx], arr[high]);
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (arr[j] <= pivot) std::swap(arr[++i], arr[j]);
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int low, int high,
               int (*choosePivot)(std::vector<int>&, int, int)) {
    if (low < high) {
        int p = choosePivot(arr, low, high);
        int pi = partition(arr, low, high, p);
        quickSort(arr, low, pi - 1, choosePivot);
        quickSort(arr, pi + 1, high, choosePivot);
    }
}

int firstPivot(std::vector<int>&, int low, int) { return low; }

int randomPivot(std::vector<int>&, int low, int high) {
    static std::mt19937 gen(42);
    return low + gen() % (high - low + 1);
}

int medianOfThree(std::vector<int>& arr, int low, int high) {
    int mid = low + (high - low) / 2;
    if (arr[low] > arr[mid]) std::swap(arr[low], arr[mid]);
    if (arr[low] > arr[high]) std::swap(arr[low], arr[high]);
    if (arr[mid] > arr[high]) std::swap(arr[mid], arr[high]);
    return mid;
}

int main() {
    int n = 10000;
    std::vector<int> sorted(n);
    for (int i = 0; i < n; ++i) sorted[i] = i;

    auto arr1 = sorted, arr2 = sorted, arr3 = sorted;
    quickSort(arr1, 0, n-1, firstPivot);     // O(n^2) on sorted!
    quickSort(arr2, 0, n-1, randomPivot);    // O(n log n)
    quickSort(arr3, 0, n-1, medianOfThree);  // O(n log n)
    return 0;
}
```

**Key points:** First-element pivot on sorted data = O(n^2). Random and median-of-three avoid this.

---

## Solution 17.5

**Approach:** Build max-heap bottom-up, then repeatedly extract max.

```cpp
#include <iostream>
#include <vector>

void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(std::vector<int>& arr) {
    int n = arr.size();
    // Build max heap
    for (int i = n / 2 - 1; i >= 0; --i)
        heapify(arr, n, i);
    // Extract elements
    for (int i = n - 1; i > 0; --i) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

int main() {
    std::vector<int> arr = {12, 11, 13, 5, 6, 7};
    heapSort(arr);
    for (int x : arr) std::cout << x << " ";
    std::cout << "\n";
    return 0;
}
```

---

## Solution 17.6

**Approach:** Count occurrences, then reconstruct. Offset for negative range.

```cpp
#include <iostream>
#include <vector>

void countingSort(std::vector<int>& arr, int minVal, int maxVal) {
    int range = maxVal - minVal + 1;
    std::vector<int> count(range, 0);

    for (int x : arr) ++count[x - minVal];

    int idx = 0;
    for (int i = 0; i < range; ++i)
        while (count[i]-- > 0)
            arr[idx++] = i + minVal;
}

int main() {
    std::vector<int> arr = {3, -1, 2, -3, 0, 1, -2};
    countingSort(arr, -500, 500);  // Using full range for demo
    for (int x : arr) std::cout << x << " ";
    std::cout << "\n";
    return 0;
}
```

---

## Solution 17.7

**Approach:** Mark indices by making values negative. Values that appear twice leave their index positive.

```cpp
#include <iostream>
#include <vector>

std::vector<int> findDuplicates(std::vector<int>& nums) {
    std::vector<int> result;
    for (int i = 0; i < nums.size(); ++i) {
        int idx = std::abs(nums[i]) - 1;
        if (nums[idx] < 0) result.push_back(idx + 1);
        else nums[idx] = -nums[idx];
    }
    return result;
}

int main() {
    std::vector<int> nums = {4, 3, 2, 7, 8, 2, 3, 1};
    auto dup = findDuplicates(nums);
    for (int x : dup) std::cout << x << " ";
    std::cout << "\n";  // 2 3
    return 0;
}
```

---

## Solution 18.1

**Approach:** Recursive power with O(log n) using exponentiation by squaring.

```cpp
#include <iostream>

int power(int base, int exp) {
    if (exp == 0) return 1;
    if (exp < 0) return 0;  // Simplified; return double for real handling
    int half = power(base, exp / 2);
    if (exp % 2 == 0) return half * half;
    return base * half * half;
}

// Trace for power(2, 5):
// power(2,5) -> 2 * power(2,2)^2
//   power(2,2) -> power(2,1)^2
//     power(2,1) -> 2 * power(2,0)^2
//       power(2,0) -> 1
//     = 2 * 1 = 2
//   = 2^2 = 4
// = 2 * 4^2 = 32

int main() {
    std::cout << power(2, 5) << "\n";  // 32
    return 0;
}
```

---

## Solution 18.2

**Approach:** Print after recursive call to reverse order.

```cpp
#include <iostream>
#include <string>

void reversePrint(const std::string& s, int index) {
    if (index >= s.size()) return;
    reversePrint(s, index + 1);  // Go to end first
    std::cout << s[index];        // Print on way back
}

// Trace for "hello":
// reversePrint("hello", 0)
//   reversePrint("hello", 1)
//     reversePrint("hello", 2)
//       reversePrint("hello", 3)
//         reversePrint("hello", 4)
//           reversePrint("hello", 5) -> return
//         print 'o'
//       print 'l'
//     print 'l'
//   print 'e'
// print 'h'

int main() {
    reversePrint("hello", 0);  // olleh
    std::cout << "\n";
    return 0;
}
```

---

## Solution 18.3

**Approach:** Move n-1 disks to auxiliary, move bottom disk, move n-1 to target.

```cpp
#include <iostream>

void hanoi(int n, char from, char aux, char to) {
    if (n == 1) {
        std::cout << "Move disk 1 from " << from << " to " << to << "\n";
        return;
    }
    hanoi(n - 1, from, to, aux);
    std::cout << "Move disk " << n << " from " << from << " to " << to << "\n";
    hanoi(n - 1, aux, from, to);
}

int main() {
    hanoi(3, 'A', 'B', 'C');
    // 7 moves = 2^3 - 1
    // n=1: 1, n=2: 3, n=3: 7, n=4: 15, n=5: 31
    return 0;
}
```

---

## Solution 18.4

**Approach:** Compare outer characters, recurse inward.

```cpp
#include <iostream>
#include <string>

bool isPalindrome(const std::string& s, int left, int right) {
    if (left >= right) return true;
    if (s[left] != s[right]) return false;
    return isPalindrome(s, left + 1, right - 1);
}

bool isPalindrome(const std::string& s) {
    return isPalindrome(s, 0, s.size() - 1);
}

int main() {
    std::cout << std::boolalpha;
    std::cout << isPalindrome("racecar") << "\n";  // true
    std::cout << isPalindrome("hello") << "\n";    // false
    return 0;
}
```

---

## Solution 18.5

**Approach:** Ways[n] = sum of Ways[n-k] for k in 1..K. Memoize.

```cpp
#include <iostream>
#include <vector>

int countWaysMemo(int n, int k, std::vector<int>& memo) {
    if (n == 0) return 1;
    if (n < 0) return 0;
    if (memo[n] != -1) return memo[n];

    int ways = 0;
    for (int step = 1; step <= k; ++step)
        ways += countWaysMemo(n - step, k, memo);
    return memo[n] = ways;
}

int countWays(int n, int k) {
    std::vector<int> memo(n + 1, -1);
    return countWaysMemo(n, k, memo);
}

int main() {
    std::cout << countWays(4, 2) << "\n";  // 5: 1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2
    return 0;
}
```

---

## Solution 18.6

**Approach:** Recursively divide, sort halves, merge.

```
Merge sort tree for [38, 27, 43, 3, 9, 82, 10]:

[38 27 43 3 9 82 10]
        /          \
[38 27 43 3]  [9 82 10]
   /      \      /    \
[38 27] [43 3] [9 82] [10]
 /  \    /  \   /  \    |
[38][27][43][3][9][82][10]
  \  /    \  /   \  /   |
 [27 38] [3 43] [9 82] [10]
      \    /         \   /
   [3 27 38 43]   [9 10 82]
            \      /
      [3 9 10 27 38 43 82]
```

---

## Solution 19.1

**Approach:** Standard BST with recursive insert, search, and remove (handle all 3 cases).

```cpp
#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* insert(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->val) root->left = insert(root->left, val);
    else if (val > root->val) root->right = insert(root->right, val);
    return root;
}

bool search(TreeNode* root, int val) {
    if (!root) return false;
    if (val == root->val) return true;
    return (val < root->val) ? search(root->left, val) : search(root->right, val);
}

TreeNode* findMin(TreeNode* root) {
    while (root->left) root = root->left;
    return root;
}

TreeNode* remove(TreeNode* root, int val) {
    if (!root) return nullptr;
    if (val < root->val) root->left = remove(root->left, val);
    else if (val > root->val) root->right = remove(root->right, val);
    else {
        // Node found
        if (!root->left) {
            TreeNode* temp = root->right;
            delete root;
            return temp;
        }
        if (!root->right) {
            TreeNode* temp = root->left;
            delete root;
            return temp;
        }
        // Two children: replace with inorder successor
        TreeNode* temp = findMin(root->right);
        root->val = temp->val;
        root->right = remove(root->right, temp->val);
    }
    return root;
}

void inorder(TreeNode* root) {
    if (!root) return;
    inorder(root->left);
    std::cout << root->val << " ";
    inorder(root->right);
}

int main() {
    TreeNode* root = nullptr;
    root = insert(root, 5);
    root = insert(root, 3);
    root = insert(root, 7);
    root = insert(root, 1);
    root = insert(root, 4);
    inorder(root); std::cout << "\n";

    root = remove(root, 3);  // One child
    root = remove(root, 1);  // Leaf
    root = remove(root, 5);  // Two children
    inorder(root); std::cout << "\n";
    return 0;
}
```

---

## Solution 19.2

**Approach:** Recursive tree metrics.

```cpp
#include <iostream>
#include <cmath>

struct TreeNode {
    int val;
    TreeNode* left, *right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

int height(TreeNode* root) {
    if (!root) return -1;
    return 1 + std::max(height(root->left), height(root->right));
}

int countNodes(TreeNode* root) {
    if (!root) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}

int countLeaves(TreeNode* root) {
    if (!root) return 0;
    if (!root->left && !root->right) return 1;
    return countLeaves(root->left) + countLeaves(root->right);
}

bool isBalanced(TreeNode* root) {
    if (!root) return true;
    int lh = height(root->left);
    int rh = height(root->right);
    return std::abs(lh - rh) <= 1 && isBalanced(root->left) && isBalanced(root->right);
}

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    std::cout << "Height: " << height(root) << "\n";
    std::cout << "Nodes: " << countNodes(root) << "\n";
    std::cout << "Leaves: " << countLeaves(root) << "\n";
    std::cout << "Balanced: " << isBalanced(root) << "\n";
    return 0;
}
```

---

## Solution 19.3

**Approach:** BFS with queue. Track level size to print each level on its own line.

```cpp
#include <iostream>
#include <queue>

struct TreeNode {
    int val;
    TreeNode* left, *right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

void levelOrder(TreeNode* root) {
    if (!root) return;
    std::queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {
        int levelSize = q.size();
        for (int i = 0; i < levelSize; ++i) {
            TreeNode* node = q.front(); q.pop();
            std::cout << node->val << " ";
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        std::cout << "\n";
    }
}

int main() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    levelOrder(root);
    return 0;
}
```

---

## Solution 19.4

**Approach:** Use BST property. If both values are smaller than root, LCA is in left subtree. If both larger, in right. Otherwise, root is LCA.

```cpp
#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left, *right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* lowestCommonAncestor(TreeNode* root, int p, int q) {
    if (!root) return nullptr;
    if (p < root->val && q < root->val)
        return lowestCommonAncestor(root->left, p, q);
    if (p > root->val && q > root->val)
        return lowestCommonAncestor(root->right, p, q);
    return root;  // p and q are on different sides
}

int main() {
    TreeNode* root = new TreeNode(6);
    root->left = new TreeNode(2);
    root->right = new TreeNode(8);
    root->left->left = new TreeNode(0);
    root->left->right = new TreeNode(4);

    TreeNode* lca = lowestCommonAncestor(root, 2, 4);
    std::cout << "LCA of 2 and 4: " << lca->val << "\n";  // 2
    return 0;
}
```

---

## Solution 19.5

**Approach:** After each insertion/deletion, check balance factor and rotate if needed.

```cpp
#include <iostream>
#include <algorithm>

struct AVLNode {
    int val;
    AVLNode* left, *right;
    int height;
    AVLNode(int v) : val(v), left(nullptr), right(nullptr), height(1) {}
};

int getHeight(AVLNode* n) { return n ? n->height : 0; }
int getBalance(AVLNode* n) { return n ? getHeight(n->left) - getHeight(n->right) : 0; }
void updateHeight(AVLNode* n) { n->height = 1 + std::max(getHeight(n->left), getHeight(n->right)); }

AVLNode* rotateRight(AVLNode* y) {
    AVLNode* x = y->left;
    AVLNode* T2 = x->right;
    x->right = y; y->left = T2;
    updateHeight(y); updateHeight(x);
    return x;
}

AVLNode* rotateLeft(AVLNode* x) {
    AVLNode* y = x->right;
    AVLNode* T2 = y->left;
    y->left = x; x->right = T2;
    updateHeight(x); updateHeight(y);
    return y;
}

AVLNode* insert(AVLNode* node, int val) {
    if (!node) return new AVLNode(val);
    if (val < node->val) node->left = insert(node->left, val);
    else node->right = insert(node->right, val);

    updateHeight(node);
    int balance = getBalance(node);

    if (balance > 1 && val < node->left->val)
        return rotateRight(node);
    if (balance < -1 && val > node->right->val)
        return rotateLeft(node);
    if (balance > 1 && val > node->left->val) {
        node->left = rotateLeft(node->left);
        return rotateRight(node);
    }
    if (balance < -1 && val < node->right->val) {
        node->right = rotateRight(node->right);
        return rotateLeft(node);
    }
    return node;
}

bool isBalanced(AVLNode* root) {
    if (!root) return true;
    return std::abs(getBalance(root)) <= 1 && isBalanced(root->left) && isBalanced(root->right);
}

int main() {
    AVLNode* root = nullptr;
    for (int i = 1; i <= 100; ++i)
        root = insert(root, i);
    std::cout << "Balanced after 100 inserts: " << isBalanced(root) << "\n";
    return 0;
}
```

---

## Solution 20.1

**Approach:** Array-based heap with bubble-up and heapify-down.

```cpp
#include <iostream>
#include <vector>

class MaxHeap {
    std::vector<int> data;

    void bubbleUp(int i) {
        while (i > 0) {
            int parent = (i - 1) / 2;
            if (data[i] <= data[parent]) break;
            std::swap(data[i], data[parent]);
            i = parent;
        }
    }

    void heapifyDown(int i) {
        int n = data.size();
        while (true) {
            int largest = i;
            int left = 2 * i + 1;
            int right = 2 * i + 2;
            if (left < n && data[left] > data[largest]) largest = left;
            if (right < n && data[right] > data[largest]) largest = right;
            if (largest == i) break;
            std::swap(data[i], data[largest]);
            i = largest;
        }
    }

public:
    void insert(int val) {
        data.push_back(val);
        bubbleUp(data.size() - 1);
    }

    int extractMax() {
        if (data.empty()) throw std::runtime_error("Empty heap");
        int maxVal = data[0];
        data[0] = data.back();
        data.pop_back();
        if (!data.empty()) heapifyDown(0);
        return maxVal;
    }

    int peekMax() const {
        if (data.empty()) throw std::runtime_error("Empty heap");
        return data[0];
    }

    void heapify(int index) { heapifyDown(index); }
    int size() const { return data.size(); }
};

int main() {
    MaxHeap heap;
    heap.insert(3);
    heap.insert(1);
    heap.insert(4);
    std::cout << "Max: " << heap.peekMax() << "\n";
    std::cout << "Extract: " << heap.extractMax() << "\n";
    std::cout << "New max: " << heap.peekMax() << "\n";
    return 0;
}
```

---

## Solution 20.2

**Approach:** Bottom-up heapify is O(n) because most nodes are near leaves (small subtrees).

```cpp
#include <iostream>
#include <vector>
#include <chrono>
#include <random>

void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1, r = 2 * i + 2;
    if (l < n && arr[l] > arr[largest]) largest = l;
    if (r < n && arr[r] > arr[largest]) largest = r;
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void buildHeap(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; --i)
        heapify(arr, n, i);
}

int main() {
    const int N = 1'000'000;
    std::mt19937 gen(42);
    std::uniform_int_distribution<> dist(1, N);

    std::vector<int> data(N);
    for (int& x : data) x = dist(gen);

    auto start = std::chrono::high_resolution_clock::now();
    buildHeap(data);
    auto end = std::chrono::high_resolution_clock::now();

    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Build heap O(n): " << ms.count() << " ms\n";
    return 0;
}
```

**Key points:** Bottom-up: O(n). Insert one-by-one: O(n log n). For n=1M, bottom-up is ~10x faster.

---

## Solution 20.3

**Approach:** In-place heap sort (same as Solution 17.5).

```cpp
#include <iostream>
#include <vector>

// See Solution 17.5 for full implementation
// Key idea: build max heap, then swap root with last element and heapify
```

---

## Solution 20.4

**Approach:** Min-heap with custom comparator. For update, remove and re-insert.

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

struct Task {
    std::string name;
    int priority;  // Lower = higher priority
};

class TaskScheduler {
    std::vector<Task> heap;

    void bubbleUp(int i) {
        while (i > 0) {
            int p = (i - 1) / 2;
            if (heap[i].priority >= heap[p].priority) break;
            std::swap(heap[i], heap[p]);
            i = p;
        }
    }

    void heapifyDown(int i) {
        int n = heap.size();
        while (true) {
            int smallest = i;
            int l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && heap[l].priority < heap[smallest].priority) smallest = l;
            if (r < n && heap[r].priority < heap[smallest].priority) smallest = r;
            if (smallest == i) break;
            std::swap(heap[i], heap[smallest]);
            i = smallest;
        }
    }

public:
    void addTask(const std::string& name, int priority) {
        heap.push_back({name, priority});
        bubbleUp(heap.size() - 1);
    }

    Task getNextTask() {
        if (heap.empty()) throw std::runtime_error("No tasks");
        Task t = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        if (!heap.empty()) heapifyDown(0);
        return t;
    }

    void updatePriority(const std::string& name, int newPriority) {
        for (size_t i = 0; i < heap.size(); ++i) {
            if (heap[i].name == name) {
                int old = heap[i].priority;
                heap[i].priority = newPriority;
                if (newPriority < old) bubbleUp(i);
                else heapifyDown(i);
                return;
            }
        }
    }
};

int main() {
    TaskScheduler ts;
    ts.addTask("Email", 3);
    ts.addTask("Critical bug", 1);
    ts.addTask("Meeting", 2);

    auto t = ts.getNextTask();
    std::cout << t.name << " (priority " << t.priority << ")\n";
    return 0;
}
```

---

## Solution 21.1

**Approach:** Array of linked lists for separate chaining.

```cpp
#include <iostream>
#include <string>
#include <vector>

class HashTable {
    struct Node {
        int key;
        std::string value;
        Node* next;
        Node(int k, const std::string& v) : key(k), value(v), next(nullptr) {}
    };
    std::vector<Node*> table;
    int capacity;

    int hash(int key) const { return key % capacity; }

public:
    HashTable(int cap = 101) : capacity(cap), table(cap, nullptr) {}

    void insert(int key, const std::string& value) {
        int idx = hash(key);
        Node* curr = table[idx];
        while (curr) {
            if (curr->key == key) { curr->value = value; return; }
            curr = curr->next;
        }
        Node* node = new Node(key, value);
        node->next = table[idx];
        table[idx] = node;
    }

    std::string search(int key) const {
        int idx = hash(key);
        Node* curr = table[idx];
        while (curr) {
            if (curr->key == key) return curr->value;
            curr = curr->next;
        }
        return "";
    }

    void remove(int key) {
        int idx = hash(key);
        Node** curr = &table[idx];
        while (*curr) {
            if ((*curr)->key == key) {
                Node* temp = *curr;
                *curr = (*curr)->next;
                delete temp;
                return;
            }
            curr = &((*curr)->next);
        }
    }
};

int main() {
    HashTable ht;
    ht.insert(1, "Alice");
    ht.insert(101, "Bob");  // Collision with 1 if capacity=101
    std::cout << ht.search(1) << "\n";
    ht.remove(1);
    return 0;
}
```

---

## Solution 21.2

**Approach:** Linear probing with tombstone for lazy deletion.

```cpp
#include <iostream>
#include <string>
#include <vector>

enum class EntryState { EMPTY, OCCUPIED, DELETED };

struct Entry {
    int key;
    std::string value;
    EntryState state;
    Entry() : key(0), value(""), state(EntryState::EMPTY) {}
};

class OpenAddressingHash {
    std::vector<Entry> table;
    int capacity;
    int size;

    int probe(int key, int i) const { return (key + i) % capacity; }

public:
    OpenAddressingHash(int cap = 101) : capacity(cap), size(0), table(cap) {}

    void insert(int key, const std::string& value) {
        for (int i = 0; i < capacity; ++i) {
            int idx = probe(key, i);
            if (table[idx].state != EntryState::OCCUPIED) {
                table[idx] = {key, value, EntryState::OCCUPIED};
                ++size;
                return;
            }
        }
    }

    std::string search(int key) const {
        for (int i = 0; i < capacity; ++i) {
            int idx = probe(key, i);
            if (table[idx].state == EntryState::EMPTY) return "";
            if (table[idx].state == EntryState::OCCUPIED && table[idx].key == key)
                return table[idx].value;
        }
        return "";
    }

    void remove(int key) {
        for (int i = 0; i < capacity; ++i) {
            int idx = probe(key, i);
            if (table[idx].state == EntryState::EMPTY) return;
            if (table[idx].state == EntryState::OCCUPIED && table[idx].key == key) {
                table[idx].state = EntryState::DELETED;
                --size;
                return;
            }
        }
    }
};
```

---

## Solution 21.3

**Approach:** Measure performance at different load factors.

| Load Factor | Chaining Avg Chain | Linear Probing Avg Probes |
|-------------|-------------------|---------------------------|
| 0.3 | ~1.0 | ~1.2 |
| 0.5 | ~1.5 | ~1.5 |
| 0.7 | ~2.3 | ~2.3 |
| 0.9 | ~10+ | ~5+ (clusters form) |

**Key points:** Chaining degrades gracefully. Linear probing degrades sharply near 1.0 due to clustering.

---

## Solution 21.4

**Approach:** Polynomial rolling hash for strings.

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <algorithm>

class StringHashTable {
    struct Node {
        std::string key;
        int count;
        Node* next;
        Node(const std::string& k) : key(k), count(1), next(nullptr) {}
    };
    std::vector<Node*> table;
    static const int P = 31;
    static const int MOD = 1e9 + 9;

    size_t hash(const std::string& s) const {
        long long h = 0, p_pow = 1;
        for (char c : s) {
            h = (h + (c - 'a' + 1) * p_pow) % MOD;
            p_pow = (p_pow * P) % MOD;
        }
        return h % table.size();
    }

public:
    StringHashTable(int cap = 10007) : table(cap, nullptr) {}

    void insert(const std::string& word) {
        size_t idx = hash(word);
        Node* curr = table[idx];
        while (curr) {
            if (curr->key == word) { ++curr->count; return; }
            curr = curr->next;
        }
        Node* node = new Node(word);
        node->next = table[idx];
        table[idx] = node;
    }

    void printTop(int n) {
        std::vector<Node*> all;
        for (auto* head : table)
            for (Node* curr = head; curr; curr = curr->next)
                all.push_back(curr);

        std::sort(all.begin(), all.end(),
            [](Node* a, Node* b) { return a->count > b->count; });

        for (int i = 0; i < std::min(n, (int)all.size()); ++i)
            std::cout << all[i]->key << ": " << all[i]->count << "\n";
    }
};

int main() {
    StringHashTable ht;
    std::ifstream file("text.txt");
    std::string word;
    while (file >> word) ht.insert(word);
    ht.printTop(20);
    return 0;
}
```

---

## Solution 22.1

**Approach:** Adjacency list using `std::vector<std::vector<int>>`.

```cpp
#include <iostream>
#include <vector>

class Graph {
    std::vector<std::vector<int>> adj;
    bool directed;

public:
    Graph(int n, bool dir = false) : adj(n), directed(dir) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        if (!directed) adj[v].push_back(u);
    }

    void print() const {
        for (int i = 0; i < adj.size(); ++i) {
            std::cout << i << ": ";
            for (int v : adj[i]) std::cout << v << " ";
            std::cout << "\n";
        }
    }

    int size() const { return adj.size(); }
    const std::vector<int>& neighbors(int u) const { return adj[u]; }
};

int main() {
    Graph g(6, false);  // Undirected: 0-1-2 grid
    g.addEdge(0, 1); g.addEdge(0, 3);
    g.addEdge(1, 2); g.addEdge(1, 4);
    g.addEdge(2, 5);
    g.addEdge(3, 4);
    g.addEdge(4, 5);
    g.print();
    return 0;
}
```

---

## Solution 22.2

**Approach:** DFS recursive, DFS iterative (stack), BFS (queue).

```cpp
#include <iostream>
#include <vector>
#include <stack>
#include <queue>

class Graph {
    std::vector<std::vector<int>> adj;
public:
    Graph(int n) : adj(n) {}
    void addEdge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    const std::vector<int>& neighbors(int u) const { return adj[u]; }
    int size() const { return adj.size(); }
};

void dfsRecursive(const Graph& g, int v, std::vector<bool>& visited) {
    visited[v] = true;
    std::cout << v << " ";
    for (int u : g.neighbors(v))
        if (!visited[u]) dfsRecursive(g, u, visited);
}

void dfsIterative(const Graph& g, int start) {
    std::vector<bool> visited(g.size(), false);
    std::stack<int> stk;
    stk.push(start);
    while (!stk.empty()) {
        int v = stk.top(); stk.pop();
        if (visited[v]) continue;
        visited[v] = true;
        std::cout << v << " ";
        for (int u : g.neighbors(v))
            if (!visited[u]) stk.push(u);
    }
}

void bfs(const Graph& g, int start) {
    std::vector<bool> visited(g.size(), false);
    std::queue<int> q;
    q.push(start);
    visited[start] = true;
    while (!q.empty()) {
        int v = q.front(); q.pop();
        std::cout << v << " ";
        for (int u : g.neighbors(v))
            if (!visited[u]) { visited[u] = true; q.push(u); }
    }
}

int main() {
    Graph g(6);
    g.addEdge(0, 1); g.addEdge(0, 3);
    g.addEdge(1, 2); g.addEdge(1, 4);
    g.addEdge(2, 5);
    g.addEdge(3, 4);
    g.addEdge(4, 5);

    std::cout << "DFS recursive: ";
    std::vector<bool> vis(g.size(), false);
    dfsRecursive(g, 0, vis);
    std::cout << "\nDFS iterative: ";
    dfsIterative(g, 0);
    std::cout << "\nBFS: ";
    bfs(g, 0);
    std::cout << "\n";
    return 0;
}
```

---

## Solution 22.3

**Approach:** DFS, track parent. If we revisit a visited node that's not the parent, there's a cycle.

```cpp
#include <iostream>
#include <vector>

class Graph {
    std::vector<std::vector<int>> adj;
public:
    Graph(int n) : adj(n) {}
    void addEdge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    const std::vector<int>& neighbors(int u) const { return adj[u]; }
    int size() const { return adj.size(); }
};

bool hasCycleDFS(const Graph& g, int v, int parent, std::vector<bool>& visited) {
    visited[v] = true;
    for (int u : g.neighbors(v)) {
        if (!visited[u]) {
            if (hasCycleDFS(g, u, v, visited)) return true;
        } else if (u != parent) {
            return true;
        }
    }
    return false;
}

bool hasCycle(const Graph& g) {
    std::vector<bool> visited(g.size(), false);
    for (int i = 0; i < g.size(); ++i)
        if (!visited[i] && hasCycleDFS(g, i, -1, visited))
            return true;
    return false;
}

int main() {
    Graph g1(3);
    g1.addEdge(0, 1); g1.addEdge(1, 2);  // No cycle
    std::cout << std::boolalpha << hasCycle(g1) << "\n";  // false

    Graph g2(3);
    g2.addEdge(0, 1); g2.addEdge(1, 2); g2.addEdge(2, 0);  // Cycle
    std::cout << hasCycle(g2) << "\n";  // true
    return 0;
}
```

---

## Solution 22.4

**Approach:** Dijkstra with priority queue (min-heap).

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <limits>

using Edge = std::pair<int, int>;  // (weight, node)

std::vector<int> dijkstra(const std::vector<std::vector<Edge>>& graph, int start) {
    int n = graph.size();
    std::vector<int> dist(n, std::numeric_limits<int>::max());
    dist[start] = 0;

    std::priority_queue<Edge, std::vector<Edge>, std::greater<>> pq;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [w, v] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    std::vector<std::vector<Edge>> graph(5);
    graph[0] = {{4, 1}, {2, 2}};
    graph[1] = {{1, 3}};
    graph[2] = {{3, 1}, {2, 3}, {4, 4}};
    graph[3] = {{1, 4}};

    auto dist = dijkstra(graph, 0);
    for (int i = 0; i < dist.size(); ++i)
        std::cout << "To " << i << ": " << dist[i] << "\n";
    return 0;
}
```

---

## Solution 22.5

**Approach:** Kahn's algorithm: count in-degrees, process nodes with in-degree 0.

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <string>

std::vector<std::string> topologicalSort(
    const std::vector<std::string>& courses,
    const std::vector<std::pair<int, int>>& prerequisites) {

    int n = courses.size();
    std::vector<std::vector<int>> adj(n);
    std::vector<int> inDegree(n, 0);

    for (auto [pre, course] : prerequisites) {
        adj[pre].push_back(course);
        ++inDegree[course];
    }

    std::queue<int> q;
    for (int i = 0; i < n; ++i)
        if (inDegree[i] == 0) q.push(i);

    std::vector<std::string> result;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        result.push_back(courses[u]);
        for (int v : adj[u]) {
            if (--inDegree[v] == 0) q.push(v);
        }
    }
    return result;
}

int main() {
    std::vector<std::string> courses = {"A", "B", "C", "D"};
    std::vector<std::pair<int, int>> prereq = {{0, 2}, {1, 2}, {2, 3}};
    // C needs A and B; D needs C

    auto order = topologicalSort(courses, prereq);
    for (const auto& c : order) std::cout << c << " ";
    std::cout << "\n";  // A B C D or B A C D
    return 0;
}
```

---

## Solution 16.4

**Approach:** XOR all elements. Pairs cancel out.

```cpp
#include <iostream>
#include <vector>

int findUnique(const std::vector<int>& arr) {
    int result = 0;
    for (int x : arr) result ^= x;
    return result;
}

// Variation: two unique elements
std::pair<int, int> findTwoUnique(const std::vector<int>& arr) {
    int xorAll = 0;
    for (int x : arr) xorAll ^= x;

    int diffBit = xorAll & -xorAll;  // Rightmost set bit
    int a = 0, b = 0;
    for (int x : arr) {
        if (x & diffBit) a ^= x;
        else b ^= x;
    }
    return {a, b};
}

int main() {
    std::vector<int> arr1 = {4, 1, 2, 1, 2};
    std::cout << "Unique: " << findUnique(arr1) << "\n";  // 4

    std::vector<int> arr2 = {1, 2, 1, 3, 2, 5};
    auto [a, b] = findTwoUnique(arr2);
    std::cout << "Two unique: " << a << ", " << b << "\n";  // 3, 5
    return 0;
}
```

**Key points:** `x ^ x = 0` and `x ^ 0 = x`. For two unique elements, find a bit where they differ and partition.

---

## Solution 17.8

**Approach:** QuickSelect partitions like quicksort but only recurses into one side.

```cpp
#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>

int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low;
    for (int j = low; j < high; ++j)
        if (arr[j] <= pivot) std::swap(arr[i++], arr[j]);
    std::swap(arr[i], arr[high]);
    return i;
}

int quickSelect(std::vector<int>& arr, int low, int high, int k) {
    if (low == high) return arr[low];
    int p = partition(arr, low, high);
    if (k == p) return arr[k];
    if (k < p) return quickSelect(arr, low, p - 1, k);
    return quickSelect(arr, p + 1, high, k);
}

int findKthSmallest(std::vector<int> arr, int k) {
    return quickSelect(arr, 0, arr.size() - 1, k - 1);
}

int main() {
    std::vector<int> arr(1'000'000);
    std::mt19937 gen(42);
    std::uniform_int_distribution<> dist(1, 1'000'000);
    for (int& x : arr) x = dist(gen);

    auto start1 = std::chrono::high_resolution_clock::now();
    int kth = findKthSmallest(arr, 500'000);
    auto end1 = std::chrono::high_resolution_clock::now();

    auto start2 = std::chrono::high_resolution_clock::now();
    std::sort(arr.begin(), arr.end());
    int sortedKth = arr[499'999];
    auto end2 = std::chrono::high_resolution_clock::now();

    auto ms1 = std::chrono::duration_cast<std::chrono::milliseconds>(end1 - start1);
    auto ms2 = std::chrono::duration_cast<std::chrono::milliseconds>(end2 - start2);

    std::cout << "QuickSelect: " << ms1.count() << " ms, result=" << kth << "\n";
    std::cout << "Full sort: " << ms2.count() << " ms, result=" << sortedKth << "\n";
    return 0;
}
```

---

## Solution 18.7

**Approach:** Backtracking: place queens row by row, check column and diagonals.

```cpp
#include <iostream>
#include <vector>

bool isSafe(const std::vector<int>& queens, int row, int col) {
    for (int prevRow = 0; prevRow < row; ++prevRow) {
        int prevCol = queens[prevRow];
        if (prevCol == col) return false;
        if (std::abs(prevCol - col) == std::abs(prevRow - row)) return false;
    }
    return true;
}

void solveNQueens(int n, int row, std::vector<int>& queens, int& count) {
    if (row == n) {
        ++count;
        // Print solution
        for (int r = 0; r < n; ++r) {
            for (int c = 0; c < n; ++c)
                std::cout << (queens[r] == c ? "Q " : ". ");
            std::cout << "\n";
        }
        std::cout << "\n";
        return;
    }
    for (int col = 0; col < n; ++col) {
        if (isSafe(queens, row, col)) {
            queens[row] = col;
            solveNQueens(n, row + 1, queens, count);
        }
    }
}

int main() {
    int n = 8;
    std::vector<int> queens(n, -1);
    int count = 0;
    solveNQueens(n, 0, queens, count);
    std::cout << "Total solutions: " << count << "\n";  // 92
    return 0;
}
```

---

## Solution 22.6

**Approach:** Kruskal's algorithm with union-find.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

struct Edge {
    int u, v, weight;
    bool operator<(const Edge& other) const { return weight < other.weight; }
};

class UnionFind {
    std::vector<int> parent, rank;
public:
    UnionFind(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    bool unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        if (rank[px] < rank[py]) std::swap(px, py);
        parent[py] = px;
        if (rank[px] == rank[py]) ++rank[px];
        return true;
    }
};

int kruskal(int n, std::vector<Edge>& edges) {
    std::sort(edges.begin(), edges.end());
    UnionFind uf(n);
    int mstWeight = 0;
    int edgesUsed = 0;

    for (const auto& e : edges) {
        if (uf.unite(e.u, e.v)) {
            mstWeight += e.weight;
            std::cout << "Edge: " << e.u << "-" << e.v << " (" << e.weight << ")\n";
            if (++edgesUsed == n - 1) break;
        }
    }
    return mstWeight;
}

int main() {
    std::vector<Edge> edges = {
        {0, 1, 4}, {0, 2, 2}, {1, 2, 1},
        {1, 3, 5}, {2, 3, 8}, {2, 4, 3}, {3, 4, 2}
    };
    int total = kruskal(5, edges);
    std::cout << "MST weight: " << total << "\n";  // 8
    return 0;
}
```
