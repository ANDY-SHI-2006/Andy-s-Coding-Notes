# 1 Introduction & A Brief History of Computing

> Course: Computer System Architecture and Parallel Computing (Westlake University, Fall 2026, Huan Wang)
> This lecture: course background and logistics, a history of computing (hardware & software), the origin of the term "computer architecture", and the content/scope of the course.

## 1.1 Where This Course Sits

In the curriculum, this course fits here:

1. Prerequisite: CS basics & programming (ICSP)
2. Then 4 core classes:
   - Logic/math: DS & Algorithms (C++)
   - **Hardware and H/S interface: Organization & Architecture (this course covers ~80% of it)**
   - Software: Operating Systems (~20% touched by this course)
   - Software: Networking
3. Future: AI computing

Course composition: **20% computer organization + 70% architecture & parallel computing + 10% compilers & OS**. Part of the content is grad-level.

Related classes and materials the course draws on:

- CMU CSAPP; *Computer Architecture: A Quantitative Approach* (CISC vs RISC)
- Stanford CS149 / CMU 15-418 (parallel computing); Stanford EE282
- Berkeley CS267 (HPC); CS152/CS252
- AI systems: MIT 6.5940 (Song Han), UW CSE 599W (Tianqi Chen), CMU 15-442/15-642, CMU 15-779 (FlashAttention, Triton, ZeRO/FSDP, PagedAttention, speculative decoding, MoE)
- More CS classes: [csdiy.wiki](https://csdiy.wiki/en)

## 1.2 Layers of a Computing System

![[computing-system-layers.png]]

Bottom-up: **Information → Digital Circuit (hardware) → Computer (hardware) → Operating System (software) → Network (H | S) → Applications (H | S)**. Programming connects Applications / Network / OS, and Algorithms support Programming.

An open question from the instructor: at which layer does AI (MLPs, CNNs, backpropagation) live?

> **Key takeaway:** Computers (software / compilers / AI...) were not this way from Day 1. History and context matter for understanding what is going on (know the past, so as to know the future).

## 1.3 A Brief History of Computing

### 1.3.1 The Magic 1940s

| Person | Contribution |
|--------|--------------|
| Alan Turing (1912–1954) | Computing & AI; the Turing test (originally the "imitation game"), 1949 |
| John von Neumann (1903–1957) | Digital computers; *First Draft of a Report on the EDVAC*, 1945 |
| Claude Shannon (1916–2001) | Information theory; *A Mathematical Theory of Communication*, 1948 |
| Norbert Wiener (1894–1964) | Cybernetics; *Cybernetics*, 1948 |

**The first AI was a piece of hardware**: in 1957, Frank Rosenblatt at Cornell Aeronautical Laboratory simulated the perceptron on an IBM 704, then built dedicated hardware — the Perceptron Mark I. Food for thought: why build hardware? Wasn't it easier to just write code like we do today? (Hint: compute and the software ecosystem were completely different back then.)

**ENIAC → EDVAC**:

- ENIAC (completed 1945, unveiled 1946-02-14) was the world's first programmable, electronic, general-purpose digital computer — but it was **programmed by rewiring**.
- In the summer of 1944, Goldstine had a chance encounter with John von Neumann on a railway platform in Aberdeen, Maryland, and described the UPenn project — leading to the 1945 EDVAC report (the stored-program idea).
- Note: von Neumann did **not** use the term "architecture".

### 1.3.2 Transistors (1948)

Bardeen, Shockley, and Brattain invented the transistor at Bell Labs in 1948; Shockley's July 1949 paper on p-n junctions laid the theoretical foundation for the bipolar junction transistor (BJT). The three shared the 1956 Nobel Prize in Physics. Computing moved from vacuum tubes to transistors.

### 1.3.3 Hardware Generations: Mainframe → Minicomputer → Microcomputer

| Generation | Examples | Era | Users | Notes |
|------------|----------|-----|-------|-------|
| Mainframe | IBM System/360 (1964) | 1950s–1960s | Big companies | The term came from the telephone switching industry (the main cabinet); back then it was simply "the computer" |
| Minicomputer | DEC PDP-8 (1965, ~$18,000) | from 1965 | Universities & labs | The "mini" label was likely inspired by the miniskirt and the Mini Cooper; **directly spawned Unix and the time-sharing culture** |
| Microcomputer / PC | Intel 4004 (1971, first microprocessor), Altair 8800 (1975), Apple II & Commodore PET (1977), IBM PC (1981) | mid-1970s–now | Families / individuals | The IBM PC cemented the term "PC" |

Later came laptops (personal, portable) and mobile phones (mobile personal devices). The trend: **computing keeps sinking down to smaller organizations and individuals**.

### 1.3.4 Programming Languages (skipped in class — self-study)

- **1950s**: FORTRAN (1957, IBM / John Backus) — the first language to prove compiler-generated code could approach handwritten assembly; LISP (1958, McCarthy) — symbolic computation and AI, pioneered recursion and garbage collection; COBOL (1959) — business data processing; ALGOL 60 — block structure and BNF, the syntactic ancestor of nearly all mainstream languages (McCarthy also co-designed ALGOL)
- **1960s–1970s, structured & systems programming**: BASIC (1964, teaching on time-sharing systems); Pascal (1970, Wirth); **C (1972, Ritchie) — created to rewrite Unix on the PDP-11; C and Unix mutually reinforced each other**, establishing the paradigm of building OSes in high-level languages
- **1980s, the rise of OOP**: Smalltalk (Xerox PARC) formalized OOP; C++ (1985, Stroustrup) brought OOP into the mainstream
- **1990s, the Internet, VMs & scripting**: Python (1991), Java (1995, the JVM's "write once, run anywhere"), JavaScript (1995), PHP, Ruby
- **Post-2000s, driven by multi-core & security**: C# (2000), Go (2009, purpose-built for multi-core servers), Rust (2010s, guaranteed memory safety), Swift (2014)

### 1.3.5 Operating Systems (self-study)

- **Early 1950s: no OS** — programmers had exclusive use of the whole machine via plugboards and paper tape; all job loading was manual
- **1956: the first recognized OS**, GM-NAA I/O (General Motors, for the IBM 704): essentially a batch-processing monitor that automatically loaded the next job to cut idle time on extremely costly hardware. **The true origin of operating systems: machines were prohibitively expensive, and human operation was the performance bottleneck**
- **1960s, foundational concepts**: IBM OS/360 (led by Fred Brooks — the project chronicled in *The Mythical Man-Month*) defined the standard form of commercial OSes; MIT's CTSS (1961) and Multics (1965) pioneered time-sharing, virtual memory, hierarchical file systems, and processes
- **1969: the birth of Unix** — after Bell Labs withdrew from Multics, Ken Thompson and Dennis Ritchie built Unix on a PDP-7 minicomputer (squarely a product of the minicomputer era)
- **1970s–1980s: temporary simplification in the microcomputer age** — CP/M (1974) and MS-DOS (1981) reverted to single-user, single-tasking; in the 1990s, as hardware improved, multitasking, virtual memory, and protected mode returned to microcomputers (Windows NT 1993, Linux 1991)

### 1.3.6 Important Timelines

1958 IC (TI) → 1968 Intel founded → **1971 first microprocessor (4004)** → 1972 C → 1975 Microsoft → 1976 Apple → 1978 Intel 8086 (x86) & ARM (Acorn) → 1983 GNU / free software → 1991 Python → 1993 WWW made public → 1994 Yahoo, Netscape → 1998 Google, Tencent → 1999 Alibaba → 2000 Baidu → 2007 iPhone → 2022 ChatGPT → … (homework: complete the list after class)

### 1.3.7 Lessons from History

- People's needs about information vary in **forms and scale** across different periods.
- Emerging demands drive the evolution of hardware and software — and hardware/software iterations, in turn, give rise to new forms of demand (the technology–human relationship is bidirectional).
- A winning solution is usually a good balance between **what we want (demand)** and **what we have (technology)**.

## 1.4 The Birth of "Computer Architecture": 1964, IBM System/360

In 1964, Amdahl, Blaauw, and Brooks published *Architecture of the IBM System/360* — the term "computer architecture" was coined (by project leader Fred Brooks).

- The System/360's chief architect, Gene Amdahl, also designed the IBM 704; the System/360 was a third-generation computer (homework: what were the 1st and 2nd generations?).
- It was a considerable risk for a company not known for gambles: the new line replaced all existing IBM products and cost USD 5 billion over four years.
- **The revolution: separating software from hardware.** Before it, buying a new computer meant scrapping all existing programs (there were no commercial software companies; software was custom-written for each machine). After it, software written for one machine ran on any other machine in the line — companies could start small and expand as needed.
- A side legacy: the System/360 pioneered the **8-bit byte** still in use today.

Summary:

- Before 1964: hardware was built with its ISA; different hardware meant different, incompatible ISAs; changing hardware meant rewriting software.
- After 1964: **the ISA was separated from the specific hardware implementation, as a standalone new layer**.
- **Computer architecture is essentially an abstraction model, a blueprint for how to build a computer — it is *not* hardware or software.**

## 1.5 What Computer Architecture Cares About Today

- Computer architecture is closely related to **parallel computing**.
- **Storage systems play a central role**: memory access is the key in modern architecture design, not compute.
- The theme of the whole area: **How can we get more computation?**
- Academic venues: CCF-recommended conferences (architecture / parallel & distributed computing / storage) — ISCA, MICRO, HPCA, ASPLOS, PPoPP, SC, FAST, DAC, EuroSys, ATC, HPDC, etc.

## 1.6 Textbooks and the Course's Main Thread

Recommended textbooks (P&H — John Hennessy and David Patterson, 2017 ACM A.M. Turing Award):

1. *Computer Organization and Design: The Hardware/Software Interface*
2. *Computer Architecture: A Quantitative Approach* (CA:AQA)

CA:AQA's chapter order is basically **time order** — which is also the main thread of this course:

- Chapter 2: memory hierarchy (why first? because it is the key)
- Chapters 3 & 4: single-core (ILP, DLP)
- Chapter 5: multi-core (TLP) — the PC era
- Chapter 6: cloud computing, clusters — the datacenter / Internet era
- Chapter 7: AI, domain-specific architectures (DSA) — the AI era

![[moores-law-trend.png]]

The evolution of computation: Scalar → Multi-issue/Superscalar → Vector → Parallel → GPUs. The key turning point:

- **Dennard Scaling** (Robert H. Dennard, 1974): as transistors get smaller, their power density remains constant — the physical basis of the "free lunch" of the Moore's-law era. Below 90nm/65nm, atoms became too few and the laws of quantum physics took over; Dennard Scaling failed.
- **2005: the multicore era — Dennard Scaling is dead.**
- **Dark Silicon**: a significant portion of the transistors on a modern chip must be left powered off ("dark") or severely underclocked ("dim") at any given moment, to prevent overheating.

Further readings:

- *The Free Lunch Is Over* (Dr. Dobb's Journal, March 2005)
- *Dark Silicon and the End of Multicore Scaling* (ISCA 2011)
- *A New Golden Age for Computer Architecture* (CACM 2019)

## 1.7 After-Class Tasks & Open Questions

- Self-study: the history of programming languages and operating systems (1.3.4 / 1.3.5)
- Complete the timeline in 1.3.6
- What were the first- and second-generation computers?
- Bonus topics (write a tech blog for bonus points):
  - Fortran is old — why hasn't it been replaced?
  - ALGOL is a family of **imperative** programming languages developed in 1958 — what is an imperative language?
  - In CA:AQA, why does data-level parallelism appear twice? Why do GPUs appear twice?
- Next lecture: recap — computing, numerical representation, compilers
