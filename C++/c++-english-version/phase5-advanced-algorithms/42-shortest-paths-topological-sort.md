[← Previous: Union-Find & MST](41-union-find-mst.md) | [Next: String Algorithms →](43-string-algorithms.md)

# 42 Shortest Paths & Topological Sort
## Dijkstra, Floyd-Warshall & Kahn's Algorithm

Graphs model relationships, but relationships are meaningless without measures of distance or precedence. This chapter completes the graph algorithm toolkit by exploring:

- **Shortest paths**: The minimum-cost route between vertices.
- **Topological order**: A valid sequence for tasks with dependencies.

These algorithms are staples of coding interviews, scheduling systems, network routing, and dependency management.

---

## 42.1 Dijkstra's Algorithm

**Problem**: Find the shortest path from a single source to all other vertices in a weighted graph with **non-negative edge weights**.

**Idea**: Maintain a set of visited vertices. Repeatedly select the unvisited vertex with the smallest known distance, mark it visited, and relax its outgoing edges.

### Priority Queue Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <climits>
using namespace std;

vector<int> dijkstra(int start, const vector<vector<pair<int,int>>>& adj) {
    int n = adj.size();
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    
    // (distance, vertex)
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, start});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue; // Stale entry
        
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}
```

**Complexity**: `O((V + E) log V)` with a binary heap.

**Why non-negative weights?** Dijkstra greedily commits to the shortest distance once a vertex is popped. Negative edges could invalidate this commitment later.

---

## 42.2 Bellman-Ford and SPFA

When edges can be negative (but no negative cycles reachable from the source), Dijkstra fails. Bellman-Ford handles this by relaxing all edges up to `V-1` times.

### Bellman-Ford

```cpp
vector<int> bellmanFord(int start, int n, const vector<tuple<int,int,int>>& edges) {
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    
    // Relax all edges (V-1) times
    for (int i = 0; i < n - 1; ++i) {
        for (auto [u, v, w] : edges) {
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    
    // Check for negative cycles
    for (auto [u, v, w] : edges) {
        if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
            // Negative cycle detected
            return {};
        }
    }
    
    return dist;
}
```

**Complexity**: `O(V · E)`.

### SPFA (Shortest Path Faster Algorithm)

SPFA is a queue-based optimization of Bellman-Ford. Only vertices whose distances changed are processed.

```cpp
vector<int> spfa(int start, const vector<vector<pair<int,int>>>& adj) {
    int n = adj.size();
    vector<int> dist(n, INT_MAX);
    vector<bool> inQueue(n, false);
    vector<int> count(n, 0); // Relaxation count for cycle detection
    
    queue<int> q;
    dist[start] = 0;
    q.push(start);
    inQueue[start] = true;
    
    while (!q.empty()) {
        int u = q.front(); q.pop();
        inQueue[u] = false;
        
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (!inQueue[v]) {
                    q.push(v);
                    inQueue[v] = true;
                    if (++count[v] > n) return {}; // Negative cycle
                }
            }
        }
    }
    
    return dist;
}
```

**Caveat**: SPFA has `O(V · E)` worst-case complexity. It is fast on random graphs but can be adversarially slow. For guaranteed performance with negative edges, use Bellman-Ford.

---

## 42.3 Floyd-Warshall

**Problem**: Find the shortest path between **all pairs** of vertices.

**Idea**: Dynamic programming. `dp[k][i][j]` = shortest path from `i` to `j` using only intermediate vertices from `{0, ..., k-1}`. This compresses to a 2D array updated in-place.

```cpp
#include <iostream>
#include <vector>
#include <climits>
using namespace std;

const int INF = 1e9;

void floydWarshall(vector<vector<int>>& dist) {
    int n = dist.size();
    
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
}

int main() {
    int n = 4;
    vector<vector<int>> dist(n, vector<int>(n, INF));
    for (int i = 0; i < n; ++i) dist[i][i] = 0;
    
    dist[0][1] = 5; dist[0][3] = 10;
    dist[1][2] = 3;
    dist[2][3] = 1;
    
    floydWarshall(dist);
    
    cout << "0 -> 3 shortest: " << dist[0][3] << endl; // Output: 9 (0-1-2-3)
    return 0;
}
```

**Complexity**: `O(V³)` time, `O(V²)` space.

**When to use**: Small dense graphs (`V <= 500`) or when all-pairs answers are needed upfront. Also used for **transitive closure** (reachability in unweighted graphs).

---

## 42.4 Topological Sort

A **topological ordering** of a Directed Acyclic Graph (DAG) is a linear ordering of vertices such that for every directed edge `(u, v)`, vertex `u` comes before `v`.

Topological sorts exist **if and only if** the graph has no directed cycles.

### Kahn's Algorithm (BFS)

Repeatedly remove vertices with no incoming edges.

```cpp
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

vector<int> topologicalSort(int n, const vector<vector<int>>& adj) {
    vector<int> inDegree(n, 0);
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) inDegree[v]++;
    }
    
    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) q.push(i);
    }
    
    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        
        for (int v : adj[u]) {
            if (--inDegree[v] == 0) q.push(v);
        }
    }
    
    // If order.size() < n, there is a cycle
    return order.size() == n ? order : vector<int>();
}
```

**Complexity**: `O(V + E)`.

### DFS-Based Topological Sort

Post-order traversal of a DFS naturally yields a reverse topological order.

```cpp
void dfsTopo(int u, const vector<vector<int>>& adj, vector<bool>& visited, vector<int>& order) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfsTopo(v, adj, visited, order);
    }
    order.push_back(u); // Post-order
}

vector<int> topologicalSortDFS(int n, const vector<vector<int>>& adj) {
    vector<bool> visited(n, false);
    vector<int> order;
    for (int i = 0; i < n; ++i) {
        if (!visited[i]) dfsTopo(i, adj, visited, order);
    }
    reverse(order.begin(), order.end());
    return order;
}
```

**Trade-off**: Kahn's algorithm detects cycles naturally (count processed vertices). DFS requires a separate cycle detection mechanism (e.g., three-color marking).

---

## 42.5 Applications of Topological Sort

### Longest Path in a DAG

In a DAG, the longest path can be found by processing vertices in topological order and relaxing edges:

```cpp
int longestPathDAG(int n, const vector<vector<pair<int,int>>>& adj) {
    // Build adjacency list of just edges (for in-degree)
    vector<vector<int>> simpleAdj(n);
    vector<int> inDegree(n, 0);
    for (int u = 0; u < n; ++u) {
        for (auto [v, w] : adj[u]) {
            simpleAdj[u].push_back(v);
            inDegree[v]++;
        }
    }
    
    queue<int> q;
    vector<int> dist(n, 0);
    for (int i = 0; i < n; ++i) if (inDegree[i] == 0) q.push(i);
    
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w > dist[v]) {
                dist[v] = dist[u] + w;
            }
            if (--inDegree[v] == 0) q.push(v);
        }
    }
    
    return *max_element(dist.begin(), dist.end());
}
```

### Course Scheduling

Given `n` courses and prerequisites `[a, b]` (meaning `b` must be taken before `a`), determine a valid schedule or detect impossible requirements (cycles).

This is exactly topological sort on the prerequisite graph.

---

## 42.6 Shortest Path Selection Guide

| Problem | Algorithm | Time | Handles Negatives |
|---------|-----------|------|-----------------|
| Single source, non-negative | Dijkstra (heap) | `O((V+E) log V)` | No |
| Single source, negatives | Bellman-Ford | `O(V·E)` | Yes (detects cycles) |
| Single source, negatives (average fast) | SPFA | `O(V·E)` worst | Yes (detects cycles) |
| All pairs | Floyd-Warshall | `O(V³)` | Yes (detects cycles) |
| Unweighted graph | BFS | `O(V+E)` | N/A |

---

## 42.7 Summary

### Key Takeaways

1. **Dijkstra** is the go-to algorithm for shortest paths with non-negative weights. Use a priority queue and skip stale entries.
2. **Bellman-Ford** handles negative edges and detects negative cycles. Its `O(V·E)` complexity is acceptable for small graphs.
3. **Floyd-Warshall** solves all-pairs shortest paths in `O(V³)`. It is also a simple way to compute transitive closure.
4. **Topological sort** exists only for DAGs. Kahn's algorithm (BFS) naturally detects cycles by counting processed vertices.
5. **DAG longest path** uses topological order followed by edge relaxation—an elegant DP on graphs.

### Template Summary

```cpp
// Dijkstra (priority queue)
vector<int> dijkstra(int s, const vector<vector<pair<int,int>>>& adj) {
    int n = adj.size();
    vector<int> dist(n, INT_MAX);
    dist[s] = 0;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d,u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v,w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

// Kahn's topological sort
vector<int> topoSort(int n, const vector<vector<int>>& adj) {
    vector<int> in(n), res;
    for (auto& list : adj) for (int v : list) in[v]++;
    queue<int> q;
    for (int i = 0; i < n; ++i) if (in[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        res.push_back(u);
        for (int v : adj[u]) if (--in[v] == 0) q.push(v);
    }
    return res.size() == n ? res : vector<int>();
}
```

### Further Reading

- **Chapter 22**: Review graph representations (adjacency list/matrix) which these algorithms build upon.
- **Chapter 38**: Tree DP and DAG longest path share the same topological-processing pattern.

[← Previous: Union-Find & MST](41-union-find-mst.md) | [Next: String Algorithms →](43-string-algorithms.md)
