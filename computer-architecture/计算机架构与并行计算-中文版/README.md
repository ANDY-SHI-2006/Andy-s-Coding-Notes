# 计算机架构与并行计算 中文版

《Computer System Architecture and Parallel Computing》（西湖大学，Fall 2026）课程笔记。课程主线是**时间序**：从计算简史出发，沿存储层次 → 单核（ILP/DLP）→ 多核（TLP）→ 数据中心 → AI 时代 DSA 一路讲到当下。

## 目录

> 笔记随课程进度更新；尚无链接的条目为规划中章节。

### 第一部分：基础（Foundations，4 讲）
1. [课程介绍与计算简史](01-课程介绍与计算简史.md) — *课程定位、计算系统分层、硬件/语言/OS 简史、"体系结构"一词的由来、Dennard Scaling 与暗硅*
2. 计算机组成与编译基础 I — *计算与数值表示*
3. 计算机组成与编译基础 II — *编译器*
4. 计算机组成与编译基础 III — *（待补充）*

### 第二部分：核心（Core，9 讲）
5. 存储层次与 Cache — *性能瓶颈、失效率/多级/带宽动手分析（不含虚拟内存）*
6. CPU：指令级并行（ILP）I — *静态 + 动态*
7. CPU：指令级并行（ILP）II — *Tomasulo、ROB*
8. CPU：指令级并行（ILP）III — *分支预测*
9. CPU & GPU：数据级并行（DLP）I
10. CPU & GPU：数据级并行（DLP）II
11. CPU：多核与线程级并行（TLP）I
12. CPU：多核与线程级并行（TLP）II
13. CPU：多核与线程级并行（TLP）III

### 第三部分：拓展（Extensions，3 讲）
14. 云服务器与其他设备 — *互联网（分布式）、FPGA & EDA、DSP、MCU 与嵌入式*
15. AI/LLM 时代专题 I — *领域专用架构 DSA：Google TPU、华为 NPU、中科院 DianNao 系列*
16. AI/LLM 时代专题 II — *AI 编译器（TVM 等）*

---

## 导航

每一章的开头和结尾都设有导航链接，方便在各节之间浏览切换。

## 图片

`../image/` 为两个语言版本共享的图片目录，用 Obsidian wikilink 引用（如 `![[computing-system-layers.png]]`）。

## 课程结构

- **第 1–4 章**：基础（导论 + 计算机组成与编译基础）
- **第 5–13 章**：核心（存储层次、ILP、DLP、TLP）
- **第 14–16 章**：拓展（云与嵌入式设备、DSA、AI 编译器）
