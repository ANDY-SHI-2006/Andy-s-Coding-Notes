[← Previous: Number Theory Essentials](40-number-theory-essentials.md) | [Next: Shortest Paths & Topological Sort →](42-shortest-paths-topological-sort.md)

# 41 Union-Find & Minimum Spanning Tree
## Disjoint Sets, Kruskal & Prim

A graph connects vertices through edges. Two fundamental questions arise repeatedly:

1. **Connectivity**: Are two vertices in the same connected component?
2. **Minimum cost**: What is the cheapest set of edges that connects all vertices?

The **Union-Find** (Disjoint Set Union, DSU) data structure answers the first question in near-constant time. **Minimum Spanning Tree** (MST) algorithms answer the second.

---

## 41.1 Union-Find (Disjoint Set Union)

Union-Find maintains a collection of disjoint sets. It supports two operations:

- **Find(x)**: Determine which set `x` belongs to.
- **Union(x, y)**: Merge the sets containing `x` and `y`.

### Basic Implementation

Each set is represented as a tree, where `parent[x]` points to `x`'s parent. The root is its own parent.

```cpp
#include <vector>
using namespace std;

class UnionFind {
    vector<int> parent;
    vector<int> rank_; // Approximate tree height
    
public:
    UnionFind(int n) {
        parent.resize(n);
        rank_.resize(n, 0);
        for (int i = 0; i < n; ++i) parent[i] = i;
    }
    
    // Find with path compression
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Compress path
        }
        return parent[x];
    }
    
    // Union by rank
    void unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return;
        
        if (rank_[px] < rank_[py]) swap(px, py);
        parent[py] = px;
        if (rank_[px] == rank_[py]) rank_[px]++;
    }
    
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};
```

### Path Compression

During `find(x)`, every node on the path from `x` to the root is rewired to point directly to the root. This flattens the tree, making future queries `O(1)` amortized.

### Union by Rank / Size

Always attach the shorter tree under the taller tree. This guarantees tree height remains `O(log n)`. Combined with path compression, the amortized complexity per operation is `O(α(n))`—effectively constant, where `α` is the inverse Ackermann function.

| Operation | Amortized Time |
|-----------|---------------|
| Find | `O(α(n))` ≈ `O(1)` |
| Union | `O(α(n))` ≈ `O(1)` |

---

## 41.2 Extended Union-Find

### Weighted Union-Find

Track additional information per node, such as the distance to the parent or the relationship to the set representative.

**Example**: In the "food chain" problem, each node has a type (A, B, or C) relative to its parent. `find(x)` returns the root and updates the relative type using path compression.

```cpp
class WeightedUnionFind {
    vector<int> parent, weight;
    
public:
    WeightedUnionFind(int n) : parent(n), weight(n, 0) {
        iota(parent.begin(), parent.end(), 0);
    }
    
    // Returns root of x
    int find(int x) {
        if (parent[x] != x) {
            int root = find(parent[x]);
            weight[x] += weight[parent[x]]; // Accumulate weight
            parent[x] = root;
        }
        return parent[x];
    }
    
    // Set relation: weight[y] - weight[x] = w (in merged set)
    void unite(int x, int y, int w) {
        int px = find(x), py = find(y);
        if (px == py) return;
        parent[py] = px;
        weight[py] = weight[x] - weight[y] + w;
    }
};
```

---

## 41.3 Kruskal's Algorithm

**Problem**: Given a connected, undirected, weighted graph, find a subset of edges that connects all vertices with minimum total weight.

**Kruskal's Insight**: Process edges in ascending order of weight. Add an edge if it connects two previously disconnected components.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Edge {
    int u, v, w;
    bool operator<(const Edge& other) const {
        return w < other.w;
    }
};

class UnionFind {
    vector<int> parent, rank_;
public:
    UnionFind(int n) {
        parent.resize(n);
        rank_.resize(n, 0);
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }
    bool unite(int x, int y) {
        x = find(x); y = find(y);
        if (x == y) return false;
        if (rank_[x] < rank_[y]) swap(x, y);
        parent[y] = x;
        if (rank_[x] == rank_[y]) rank_[x]++;
        return true;
    }
};

int kruskal(int n, vector<Edge>& edges) {
    sort(edges.begin(), edges.end());
    UnionFind uf(n);
    int mstWeight = 0;
    int edgesUsed = 0;
    
    for (const auto& e : edges) {
        if (uf.unite(e.u, e.v)) {
            mstWeight += e.w;
            edgesUsed++;
            if (edgesUsed == n - 1) break; // MST complete
        }
    }
    
    return edgesUsed == n - 1 ? mstWeight : -1; // -1 if graph is disconnected
}

int main() {
    int n = 4;
    vector<Edge> edges = {
        {0, 1, 1},
        {1, 2, 2},
        {0, 2, 3},
        {2, 3, 4},
        {0, 3, 5}
    };
    cout << kruskal(n, edges) << endl; // Output: 7 (edges 0-1, 1-2, 2-3)
    return 0;
}
```

**Complexity**: `O(E log E)` for sorting + `O(E α(V))` for union-find ≈ `O(E log E)`.

---

## 41.4 Prim's Algorithm

Prim's algorithm grows the MST from a single starting vertex, always adding the cheapest edge that connects a vertex in the tree to a vertex outside.

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits>
using namespace std;

int prim(int n, const vector<vector<pair<int,int>>>& adj) {
    vector<bool> inMST(n, false);
    vector<int> minEdge(n, INT_MAX);
    minEdge[0] = 0;
    
    // (weight, vertex)
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, 0});
    
    int mstWeight = 0;
    int edgesUsed = 0;
    
    while (!pq.empty() && edgesUsed < n) {
        auto [w, u] = pq.top(); pq.pop();
        if (inMST[u]) continue;
        
        inMST[u] = true;
        mstWeight += w;
        edgesUsed++;
        
        for (auto [v, weight] : adj[u]) {
            if (!inMST[v] && weight < minEdge[v]) {
                minEdge[v] = weight;
                pq.push({weight, v});
            }
        }
    }
    
    return edgesUsed == n ? mstWeight : -1;
}
```

**Complexity**: `O(E log V)` with a binary heap.

### Kruskal vs. Prim

| Aspect | Kruskal | Prim |
|--------|---------|------|
| Data structure | Edge list + Union-Find | Adjacency list + Priority queue |
| Best for | Sparse graphs (`E ≈ V`) | Dense graphs (`E ≈ V²`) |
| Time | `O(E log E)` | `O(E log V)` |
| Space | `O(E)` | `O(V)` |

---

## 41.5 MST Properties and Variants

### Cut Property

For any cut of the graph (a partition of vertices into two sets), the minimum-weight edge crossing the cut belongs to some MST. Both Kruskal and Prim implicitly rely on this property.

### Second Best MST

Sometimes we need the MST with the smallest weight that is **strictly greater** than the optimal MST. One approach:
1. Compute the MST.
2. For each non-MST edge `(u, v, w)`, add it to the MST (creating a cycle) and remove the maximum-weight edge on the `u-v` path in the MST.
3. The minimum weight among all such alternatives is the second best MST.

This requires finding the maximum edge on a tree path—an application of LCA with binary lifting (beyond our scope but a natural extension).

---

## 41.6 Summary

### Key Takeaways

1. **Union-Find** with path compression and union by rank achieves amortized `O(α(n))` per operation—practically constant.
2. **Kruskal** sorts edges and greedily adds the cheapest edge that connects disjoint components. Ideal for sparse graphs.
3. **Prim** grows the tree from a starting node using a priority queue. Ideal for dense graphs.
4. **The cut property** guarantees the correctness of both algorithms: the cheapest crossing edge is always safe to include.
5. **Weighted Union-Find** extends the structure to track relative properties (distances, parity, types) within each set.

### Template Summary

```cpp
// Union-Find template
class UnionFind {
    vector<int> p, r;
public:
    UnionFind(int n) : p(n), r(n,0) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x]==x ? x : p[x]=find(p[x]); }
    bool unite(int a, int b) {
        a=find(a); b=find(b);
        if(a==b) return false;
        if(r[a]<r[b]) swap(a,b);
        p[b]=a; if(r[a]==r[b]) r[a]++;
        return true;
    }
};

// Kruskal template
int kruskal(int n, vector<Edge>& edges) {
    sort(edges.begin(), edges.end());
    UnionFind uf(n);
    int total = 0, used = 0;
    for(auto& e: edges) if(uf.unite(e.u, e.v)) {
        total += e.w;
        if(++used == n-1) break;
    }
    return used == n-1 ? total : -1;
}
```

### Further Reading

- **Chapter 42**: Shortest path algorithms (Dijkstra, Floyd-Warshall) extend the graph toolkit.
- **Chapter 19**: Tree traversals and representations are prerequisites for advanced MST variants.

[← Previous: Number Theory Essentials](40-number-theory-essentials.md) | [Next: Shortest Paths & Topological Sort →](42-shortest-paths-topological-sort.md)
