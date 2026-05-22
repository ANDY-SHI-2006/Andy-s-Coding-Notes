[← Previous: Object-Oriented Programming Advanced Topics](30-oop-advanced.md) | [Next: Multi-Threading →](32-multi-threading.md)

# 31 Multi-File Programming

Modern C++ projects are rarely contained in a single file. This chapter explains how to split code across multiple translation units, manage dependencies, and understand the build process.

## 31.1 Compilation Model

### 31.1.1 Translation Units

### 31.1.2 The Build Pipeline: Preprocess → Compile → Link

### 31.1.3 Object Files and Symbols

## 31.2 Header and Source Files

### 31.2.1 Header Files (.h / .hpp)

### 31.2.2 Source Files (.cpp)

### 31.2.3 The One Definition Rule Across Files

## 31.3 Header Guards and Include Guards

### 31.3.1 #pragma once

### 31.3.2 Traditional Include Guards

### 31.3.3 Include What You Use (IWYU)

## 31.4 Linkage in Practice

### 31.4.1 External Linkage: Sharing Across Files

### 31.4.2 Internal Linkage: File-Private Variables

### 31.4.3 Inline Variables (C++17)

## 31.5 extern "C" and Interoperability

### 31.5.1 Calling C from C++

### 31.5.2 Creating C-Compatible Interfaces

## 31.6 Build Systems Basics

### 31.6.1 Makefiles

### 31.6.2 CMake Introduction

## 31.7 Summary

> **Key Concept:** Multi-file programming is about **separation of interface and implementation**. Headers declare *what* is available; source files define *how* it works; the linker resolves *where* everything lives.
