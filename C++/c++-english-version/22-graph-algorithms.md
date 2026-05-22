[← Previous: Hash Tables](21-hash-tables.md) | [Next: Modern C++ Variable Features →](23-modern-cpp-variables.md)

# 22 Graph Algorithms

Graphs are versatile data structures that model relationships between objects. They are essential for solving problems in networking, mapping, scheduling, and many other domains.

## 22.1 Graph Fundamentals

### Graph Definition

A graph G = (V, E) consists of:
- **V**: Set of vertices (nodes)
- **E**: Set of edges (connections between vertices)

### Types of Graphs

| Type | Properties |
|------|-----------|
| **Undirected** | Edges have no direction |
| **Directed** | Edges have direction (arcs) |
| **Weighted** | Edges have associated weights |
| **Unweighted** | All edges equal weight |
| **Cyclic** | Contains cycles |
| **Acyclic** | No cycles (DAG, Tree) |
| **Connected** | Path exists between any two vertices |
| **Complete** | Every vertex connected to every other |
| **Bipartite** | Vertices can be divided into two sets |

### Graph Representations

#### Adjacency Matrix

```cpp
// Space: O(V²)
// Time to check edge: O(1)
class GraphMatrix {
    vector<vector<int>> adj;
    int n;
    
public:
    GraphMatrix(int vertices) : n(vertices) {
        adj.resize(n, vector<int>(n, 0));
    }
    
    void addEdge(int u, int v, int weight = 1) {
        adj[u][v] = weight;
        // For undirected: adj[v][u] = weight;
    }
    
    bool hasEdge(int u, int v) const {
        return adj[u][v] != 0;
    }
};
```

#### Adjacency List

```cpp
// Space: O(V + E)
// Time to check edge: O(degree)
class GraphList {
    vector<vector<pair<int,int>>> adj;  // (neighbor, weight)
    int n;
    
public:
    GraphList(int vertices) : n(vertices) {
        adj.resize(n);
    }
    
    void addEdge(int u, int v, int weight = 1) {
        adj[u].push_back({v, weight});
        // For undirected: adj[v].push_back({u, weight});
    }
    
    const vector<pair<int,int>>& getNeighbors(int u) const {
        return adj[u];
    }
};
```

## 22.2 Graph Traversals

### Depth-First Search (DFS)

```cpp
// Recursive DFS
void dfsRecursive(const vector<vector<int>>& adj, 
                  int start, vector<bool>& visited) {
    visited[start] = true;
    cout << start << " ";
    
    for (int neighbor : adj[start]) {
        if (!visited[neighbor]) {
            dfsRecursive(adj, neighbor, visited);
        }
    }
}

// Iterative DFS
void dfsIterative(const vector<vector<int>>& adj, int start) {
    int n = adj.size();
    vector<bool> visited(n, false);
    stack<int> st;
    
    st.push(start);
    
    while (!st.empty()) {
        int curr = st.top(); st.pop();
        
        if (visited[curr]) continue;
        visited[curr] = true;
        cout << curr << " ";
        
        for (int neighbor : adj[curr]) {
            if (!visited[neighbor]) {
                st.push(neighbor);
            }
        }
    }
}
```

**Applications:**
- Cycle detection
- Topological sort
- Connected components
- Path finding
- Maze solving

### Breadth-First Search (BFS)

```cpp
void bfs(const vector<vector<int>>& adj, int start) {
    int n = adj.size();
    vector<bool> visited(n, false);
    queue<int> q;
    
    visited[start] = true;
    q.push(start);
    
    while (!q.empty()) {
        int curr = q.front(); q.pop();
        cout << curr << " ";
        
        for (int neighbor : adj[curr]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
}
```

**Applications:**
- Shortest path in unweighted graphs
- Level-order traversal
- Minimum spanning tree (unweighted)
- Web crawling
- Social network analysis

## 22.3 Shortest Path Algorithms

### Dijkstra's Algorithm

Finds shortest path from source to all vertices in weighted graphs (no negative weights).

```cpp
vector<int> dijkstra(const vector<vector<pair<int,int>>>& graph, int src) {
    int n = graph.size();
    vector<int> dist(n, INT_MAX);
    dist[src] = 0;
    
    // (distance, vertex)
    priority_queue<pair<int,int>, vector<pair<int,int>>, 
                   greater<pair<int,int>>> pq;
    pq.push({0, src});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        
        if (d > dist[u]) continue;  // Skip outdated entry
        
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
// Time: O((V + E) log V), Space: O(V)
```

### Bellman-Ford Algorithm

Handles negative weights, detects negative cycles.

```cpp
vector<int> bellmanFord(const vector<vector<pair<int,int>>>& graph, int src) {
    int n = graph.size();
    vector<int> dist(n, INT_MAX);
    dist[src] = 0;
    
    // Relax edges V-1 times
    for (int i = 0; i < n - 1; i++) {
        for (int u = 0; u < n; u++) {
            for (auto [v, w] : graph[u]) {
                if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }
    }
    
    // Check for negative cycles
    for (int u = 0; u < n; u++) {
        for (auto [v, w] : graph[u]) {
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                throw runtime_error("Negative cycle detected");
            }
        }
    }
    
    return dist;
}
// Time: O(V × E), Space: O(V)
```

### Floyd-Warshall Algorithm

All-pairs shortest paths.

```cpp
vector<vector<int>> floydWarshall(vector<vector<int>>& dist) {
    int n = dist.size();
    
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX) {
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }
    return dist;
}
// Time: O(V³), Space: O(V²)
```

### Comparison

| Algorithm | Use Case | Time | Handles Negatives |
|-----------|----------|------|-------------------|
| BFS | Unweighted graphs | O(V + E) | N/A |
| Dijkstra | Weighted, single source | O((V+E) log V) | No |
| Bellman-Ford | Weighted, negative edges | O(V × E) | Yes |
| Floyd-Warshall | All-pairs shortest path | O(V³) | Yes |

## 22.4 Minimum Spanning Tree

### Kruskal's Algorithm

```cpp
struct Edge {
    int u, v, weight;
    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

class UnionFind {
    vector<int> parent, rank;
public:
    UnionFind(int n) {
        parent.resize(n);
        rank.resize(n);
        iota(parent.begin(), parent.end(), 0);
    }
    
    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]);
        return parent[x];
    }
    
    bool unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        
        if (rank[px] < rank[py]) swap(px, py);
        parent[py] = px;
        if (rank[px] == rank[py]) rank[px]++;
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
            mstWeight += e.weight;
            edgesUsed++;
            if (edgesUsed == n - 1) break;
        }
    }
    
    return mstWeight;
}
// Time: O(E log E), Space: O(V)
```

### Prim's Algorithm

```cpp
int prim(const vector<vector<pair<int,int>>>& graph) {
    int n = graph.size();
    vector<bool> inMST(n, false);
    vector<int> minEdge(n, INT_MAX);
    minEdge[0] = 0;
    
    priority_queue<pair<int,int>, vector<pair<int,int>>, 
                   greater<pair<int,int>>> pq;
    pq.push({0, 0});
    
    int mstWeight = 0;
    
    while (!pq.empty()) {
        auto [w, u] = pq.top(); pq.pop();
        
        if (inMST[u]) continue;
        inMST[u] = true;
        mstWeight += w;
        
        for (auto [v, weight] : graph[u]) {
            if (!inMST[v] && weight < minEdge[v]) {
                minEdge[v] = weight;
                pq.push({weight, v});
            }
        }
    }
    
    return mstWeight;
}
// Time: O((V + E) log V), Space: O(V)
```

## 22.5 Topological Sort

Ordering of vertices in a DAG such that for every edge (u, v), u comes before v.

```cpp
// Kahn's Algorithm (BFS-based)
vector<int> topologicalSortKahn(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> inDegree(n, 0);
    
    for (int u = 0; u < n; u++) {
        for (int v : adj[u]) {
            inDegree[v]++;
        }
    }
    
    queue<int> q;
    for (int i = 0; i < n; i++) {
        if (inDegree[i] == 0) q.push(i);
    }
    
    vector<int> result;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        result.push_back(u);
        
        for (int v : adj[u]) {
            if (--inDegree[v] == 0) {
                q.push(v);
            }
        }
    }
    
    if (result.size() != n) {
        throw runtime_error("Graph has cycle");
    }
    return result;
}

// DFS-based
void dfsTopo(const vector<vector<int>>& adj, int u, 
             vector<bool>& visited, vector<int>& result) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfsTopo(adj, v, visited, result);
        }
    }
    result.push_back(u);  // Add after visiting all neighbors
}

vector<int> topologicalSortDFS(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<bool> visited(n, false);
    vector<int> result;
    
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            dfsTopo(adj, i, visited, result);
        }
    }
    
    reverse(result.begin(), result.end());
    return result;
}
```

## 22.6 Cycle Detection

### Undirected Graph

```cpp
bool hasCycleUndirected(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<bool> visited(n, false);
    
    function<bool(int, int)> dfs = [&](int u, int parent) {
        visited[u] = true;
        
        for (int v : adj[u]) {
            if (!visited[v]) {
                if (dfs(v, u)) return true;
            } else if (v != parent) {
                return true;  // Found back edge
            }
        }
        return false;
    };
    
    for (int i = 0; i < n; i++) {
        if (!visited[i] && dfs(i, -1)) {
            return true;
        }
    }
    return false;
}
```

### Directed Graph

```cpp
bool hasCycleDirected(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> state(n, 0);  // 0=unvisited, 1=visiting, 2=visited
    
    function<bool(int)> dfs = [&](int u) {
        state[u] = 1;  // Mark as visiting
        
        for (int v : adj[u]) {
            if (state[v] == 1) return true;  // Back edge
            if (state[v] == 0 && dfs(v)) return true;
        }
        
        state[u] = 2;  // Mark as visited
        return false;
    };
    
    for (int i = 0; i < n; i++) {
        if (state[i] == 0 && dfs(i)) {
            return true;
        }
    }
    return false;
}
```

## 22.7 Strongly Connected Components

Tarjan's Algorithm for finding SCCs in directed graphs.

```cpp
vector<vector<int>> findSCC(const vector<vector<int>>& adj) {
    int n = adj.size();
    vector<int> disc(n, -1), low(n, -1);
    vector<bool> inStack(n, false);
    stack<int> st;
    vector<vector<int>> sccs;
    int time = 0;
    
    function<void(int)> dfs = [&](int u) {
        disc[u] = low[u] = ++time;
        st.push(u);
        inStack[u] = true;
        
        for (int v : adj[u]) {
            if (disc[v] == -1) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (inStack[v]) {
                low[u] = min(low[u], disc[v]);
            }
        }
        
        if (low[u] == disc[u]) {
            vector<int> scc;
            while (true) {
                int v = st.top(); st.pop();
                inStack[v] = false;
                scc.push_back(v);
                if (v == u) break;
            }
            sccs.push_back(scc);
        }
    };
    
    for (int i = 0; i < n; i++) {
        if (disc[i] == -1) dfs(i);
    }
    
    return sccs;
}
```

## 22.8 Common Graph Problems

### Number of Islands

```cpp
int numIslands(vector<vector<char>>& grid) {
    if (grid.empty()) return 0;
    
    int m = grid.size(), n = grid[0].size();
    int count = 0;
    
    function<void(int,int)> dfs = [&](int i, int j) {
        if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] != '1')
            return;
        
        grid[i][j] = '0';  // Mark as visited
        dfs(i+1, j); dfs(i-1, j);
        dfs(i, j+1); dfs(i, j-1);
    };
    
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == '1') {
                count++;
                dfs(i, j);
            }
        }
    }
    return count;
}
```

### Course Schedule (Cycle Detection)

```cpp
bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
    vector<vector<int>> adj(numCourses);
    vector<int> inDegree(numCourses, 0);
    
    for (auto& p : prerequisites) {
        adj[p[1]].push_back(p[0]);
        inDegree[p[0]]++;
    }
    
    queue<int> q;
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) q.push(i);
    }
    
    int visited = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        visited++;
        
        for (int v : adj[u]) {
            if (--inDegree[v] == 0) q.push(v);
        }
    }
    
    return visited == numCourses;
}
```

## 22.9 Summary

### Algorithm Selection Guide

| Problem | Algorithm |
|---------|-----------|
| Shortest path (unweighted) | BFS |
| Shortest path (positive weights) | Dijkstra |
| Shortest path (negative weights) | Bellman-Ford |
| All-pairs shortest path | Floyd-Warshall |
| Minimum spanning tree | Kruskal / Prim |
| Topological sort | Kahn / DFS |
| Cycle detection | DFS with state |
| Connected components | DFS / BFS / Union-Find |
| Strongly connected components | Tarjan's / Kosaraju |

### Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| DFS | O(V + E) | O(V) |
| BFS | O(V + E) | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |
| Bellman-Ford | O(V × E) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Kruskal | O(E log E) | O(V) |
| Prim | O((V+E) log V) | O(V) |

### Key Takeaways

1. **Choose representation** based on graph density (adjacency list for sparse)
2. **DFS** for exploring paths, topological sort, cycle detection
3. **BFS** for shortest path in unweighted graphs
4. **Dijkstra** for shortest path with positive weights
5. **Union-Find** for connectivity and MST problems
6. **Topological sort** for dependency resolution

[�?Previous: Hash Tables](25-hash-tables.md) | [Return to Index](README.md)
