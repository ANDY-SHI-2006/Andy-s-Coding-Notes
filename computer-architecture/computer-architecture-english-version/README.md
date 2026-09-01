# Computer Architecture & Parallel Computing — English Version

Notes for *Computer System Architecture and Parallel Computing* (Westlake University, Fall 2026). The course's main thread is **time order**: starting from computing history, then memory hierarchy → single-core (ILP/DLP) → multi-core (TLP) → datacenters → domain-specific architectures in the AI era.

## Table of Contents

> Notes are updated as the course progresses; entries without links are planned chapters.

### Part 1: Foundations (4 lectures)
1. [Introduction & A Brief History of Computing](01-introduction-and-computing-history.md) — *Course positioning, layers of a computing system, history of hardware/languages/OSes, the origin of "architecture", Dennard Scaling & dark silicon*
2. Computer Organization & Compiler Basics I — *Computing and numerical representation*
3. Computer Organization & Compiler Basics II — *Compilers*
4. Computer Organization & Compiler Basics III — *(TBD)*

### Part 2: Core (9 lectures)
5. Memory Hierarchy & Cache — *The performance bottleneck; hands-on analysis (miss rate, multi-level, bandwidth); virtual memory excluded*
6. CPU: Instruction-Level Parallelism (ILP) I — *Static + dynamic*
7. CPU: Instruction-Level Parallelism (ILP) II — *Tomasulo, ROB*
8. CPU: Instruction-Level Parallelism (ILP) III — *Branch prediction*
9. CPU & GPU: Data-Level Parallelism (DLP) I
10. CPU & GPU: Data-Level Parallelism (DLP) II
11. CPU: Multicore & Thread-Level Parallelism (TLP) I
12. CPU: Multicore & Thread-Level Parallelism (TLP) II
13. CPU: Multicore & Thread-Level Parallelism (TLP) III

### Part 3: Extensions (3 lectures)
14. Cloud Servers & Other Devices — *Internet (distributed), FPGA & EDA, DSP, MCU & embedded*
15. Topics in the AI/LLM Era I — *Domain-Specific Architectures: Google TPU, Huawei NPU, CAS DianNao series*
16. Topics in the AI/LLM Era II — *AI compilers (TVM, etc.)*

---

## Navigation

Each chapter contains navigation links at the top and bottom for easy browsing between sections.

## Images

`../image/` is a shared image directory for both language versions, referenced with Obsidian wikilinks (e.g. `![[computing-system-layers.png]]`).

## Course Structure

- **Chapters 1-4**: Foundations (intro + computer organization & compiler basics)
- **Chapters 5-13**: Core (memory hierarchy, ILP, DLP, TLP)
- **Chapters 14-16**: Extensions (cloud & embedded devices, DSA, AI compilers)
