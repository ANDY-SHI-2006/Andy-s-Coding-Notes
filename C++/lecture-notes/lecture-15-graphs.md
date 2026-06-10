# Lecture 15: Graphs

> **Source**: Data Structure and Programming Methodology  
> **Instructor**: Dr. Peidong Liu, Faculty of Engineering, Westlake University  
> **Semester**: Spring 2026  
> **Corresponding Course Chapter**: [Ch 22 Graph Algorithms](../c++-english-version/phase2-data-structures-algorithms/22-graph-algorithms.md)

---

## Table of Contents

1. [Graph Fundamentals](#1-graph-fundamentals)
2. [Graph Applications](#2-graph-applications)
3. [Graph Representation](#3-graph-representation)
4. [Breadth-First Search (BFS)](#4-breadth-first-search-bfs)
5. [Depth-First Search (DFS)](#5-depth-first-search-dfs)
6. [Topological Sort](#6-topological-sort)
7. [Spanning Trees](#7-spanning-trees)
8. [Dijkstra's Algorithm](#8-dijkstras-algorithm)

---

## 1. Graph Fundamentals

A **graph** `G = (V, E, w)` consists of:
- `V`: a set of **vertices** (nodes)
- `E`: a set of **edges** connecting vertices
- `w`: a **weight function** assigning values to edges

### Types of Graphs

| Type | Description |
|------|-------------|
| **Directed graph** | Edges have direction `(u → v)` |
| **Undirected graph** | Edges have no direction `(u — v)` |
| **Weighted graph** | Edges have weights (costs, distances) |
| **Complete graph** | Every pair of vertices is connected; `|E| = n(n-1)/2` |

### Terminology

| Term | Definition |
|------|------------|
| **Path** | A sequence of edges from one vertex to another |
| **Simple path** | A path that never visits the same vertex twice |
| **Length of a path** | Number of edges in the path |
| **Cycle** | A path that begins and ends at the same vertex |
| **Simple cycle** | A simple path that is also a cycle |
| **Connected graph** | There is a path between every pair of vertices |
| **Connected component** | A maximal connected subgraph |

---

## 2. Graph Applications

Graphs model relationships and networks across many domains:

| Domain | Problem | Graph Concept |
|--------|---------|---------------|
| **Travel planning** | Shortest route between cities | Shortest path |
| **Logistics** | Visit all cities with minimum cost | Traveling Salesman Problem (TSP) |
| **Internet routing** | Best packet route from A to B | Shortest path |
| **Course planning** | Order subjects satisfying prerequisites | Topological sort |
| **Epidemic studies** | Track disease spread | Graph connectivity |
| **Biology** | Protein interaction networks | Graph clustering |
| **VLSI design** | Chip layout optimization | Graph partitioning |
| **Job scheduling** | Task ordering with dependencies | Topological sort |

---

## 3. Graph Representation

### Adjacency Matrix

A 2D array where `adj[i][j] = weight` if edge `(i, j)` exists, otherwise `0` or `∞`.

```cpp
// Fixed size
#define MAXV 100
int adj[MAXV][MAXV];

// Dynamic size
vector<vector<int>> adj;
```

**Space**: `O(V²)`  
**Best for**: Dense graphs

### Adjacency List

For each vertex, store a list of its neighbors.

```cpp
struct Edge {
    int to;     // destination vertex
    int weight; // edge weight
};

vector<list<Edge>> adj;
```

**Space**: `O(V + E)`  
**Best for**: Sparse graphs

---

## 4. Breadth-First Search (BFS)

BFS explores a graph level by level, starting from a source vertex. It uses a **queue** and is analogous to level-order tree traversal.

### Basic BFS

```
BFS(v):
    Q = new Queue
    Q.enqueue(v)
    mark v as visited
    while Q is not empty:
        curr = Q.dequeue()
        print curr
        for each w in adj(curr):
            if w is not visited:
                Q.enqueue(w)
                mark w as visited
```

**Time**: `O(V + E)` — each vertex is enqueued/dequeued once, each edge is examined once.

### Building the BFS Tree

Track the parent of each discovered vertex:

```
BFS(v):
    Q.enqueue(v)
    mark v as visited
    while Q is not empty:
        curr = Q.dequeue()
        for each w in adj(curr):
            if w is not visited:
                Q.enqueue(w)
                w.parent = curr      // BFS tree edge
                mark w as visited
```

### Calculating Levels

The level of a vertex is its distance (in edges) from the source:

```
BFS(v):
    Q.enqueue(v)
    mark v as visited
    v.level = 1
    while Q is not empty:
        curr = Q.dequeue()
        for each w in adj(curr):
            if w is not visited:
                Q.enqueue(w)
                w.level = curr.level + 1
                mark w as visited
```

BFS finds the **shortest path** (in terms of number of edges) from the source to every reachable vertex in an unweighted graph.

---

## 5. Depth-First Search (DFS)

DFS explores as deeply as possible before backtracking.

### Iterative DFS

```
DFS(v):
    S = new Stack
    S.push(v)
    print and mark v as visited
    while S is not empty:
        curr = S.top()
        if every vertex in adj(curr) is visited:
            S.pop()
        else:
            let w be an unvisited neighbor of curr
            S.push(w)
            print and mark w as visited
```

This version more closely simulates the recursion call stack: a vertex is only popped after all its descendants have been explored.

### Recursive DFS

```
DFS(v):
    print v
    mark v as visited
    for each w in adj(v):
        if w is not visited:
            DFS(w)
```

**Time**: `O(V + E)`

---

## 6. Topological Sort

A **topological sort** produces a linear ordering of vertices in a **Directed Acyclic Graph (DAG)** such that for every edge `(u → v)`, `u` appears before `v`.

### Algorithm (Kahn's Algorithm)

```
TopologicalSort(G):
    q = new Queue()
    for each vertex v in G:
        if v.inDegree == 0:
            q.enqueue(v)
    
    while q is not empty:
        v = q.dequeue()
        output v
        for each neighbor w of v:
            w.inDegree--
            if w.inDegree == 0:
                q.enqueue(w)
```

If the output contains fewer than `V` vertices, the graph has a cycle and topological sorting is impossible.

**Applications**: Course prerequisite planning, job scheduling, compilation order.

---

## 7. Spanning Trees

### Spanning Tree in an Unweighted Graph

A **spanning tree** of a connected, undirected graph is a subgraph that:
- Contains all vertices
- Is connected
- Has no cycles
- Has exactly `V - 1` edges

Any graph traversal (BFS or DFS) produces a spanning tree from the edges used to discover new vertices.

### Minimum Spanning Tree (MST)

In a **weighted** graph, an MST is a spanning tree with the **minimum total edge weight**.

#### Prim's Algorithm

Build the MST incrementally, one vertex at a time:

1. Start with any single vertex as the initial tree `T`.
2. Repeatedly add the cheapest edge that connects a vertex in `T` to a vertex outside `T`.
3. Continue until `T` contains all vertices.

**Time with min-heap**: `O(E log V)`

---

## 8. Dijkstra's Algorithm

Finds the shortest path from a source vertex to all other vertices in a weighted graph with **non-negative edge weights**.

### Idea

Maintain a table of the currently known shortest distance to each vertex. Repeatedly select the unvisited vertex with the smallest known distance and update its neighbors.

### Pseudocode

```
Dijkstra(G, source):
    for each vertex v:
        dist[v] = infinity
        visited[v] = false
    dist[source] = 0
    
    while there are unvisited vertices:
        u = unvisited vertex with minimum dist[u]
        visited[u] = true
        
        for each neighbor v of u:
            if not visited[v] and dist[u] + weight(u,v) < dist[v]:
                dist[v] = dist[u] + weight(u,v)
```

**Time with array**: `O(V²)`  
**Time with min-heap**: `O((V + E) log V)`

---

## Summary

| Algorithm | Purpose | Time |
|-----------|---------|------|
| BFS | Level-order traversal, shortest path in unweighted graphs | `O(V + E)` |
| DFS | Deep exploration, cycle detection, topological sort | `O(V + E)` |
| Topological Sort | Linear ordering of DAG vertices | `O(V + E)` |
| Prim's | Minimum spanning tree | `O(E log V)` with heap |
| Dijkstra's | Shortest path (non-negative weights) | `O((V+E) log V)` with heap |

---

## Further Reading

- **Course Chapter**: [Ch 22 Graph Algorithms](../c++-english-version/phase2-data-structures-algorithms/22-graph-algorithms.md) — C++ implementations of BFS/DFS, cycle detection, strongly connected components, and additional algorithms (Kruskal, Bellman-Ford, Floyd-Warshall).
