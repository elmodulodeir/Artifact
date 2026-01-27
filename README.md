# Context Freezing Demo

### Reusable Decision Artifacts for LLM Systems

---

## Overview

This repository demonstrates a minimal but concrete pattern for reducing
repeated context cost in LLM-based systems.

Instead of resending the full reasoning context on every decision,
the system:

* Consolidates decisions once into a **frozen artifact**
* Reuses that artifact across many executions
* Processes only small, per-iteration delta inputs

The goal of this demo is **cost and structure**, not model quality.

---

## Problem

In many LLM systems:

* The same high-level decisions are recomputed
* Long context is resent on every iteration
* Cost scales linearly with usage, even when logic is unchanged

This is common in:

* Agent loops
* Real-time decision systems
* Market analysis
* Workflow orchestration
* Tool-using LLMs

---

## Core Idea

Convert repeated reasoning into a **reusable decision state**.

Pay the full context cost once:

* Freeze it as an artifact
* Reuse it deterministically
* Avoid recalculating or resending it

This shifts cost from:

> **Per-iteration context**
>
> to
>
> **One-time context + minimal delta input**

---

## What This Demo Shows

* A frozen decision artifact (~tens of tokens)
* A loop of 5,000 executions
* A comparison between:

  * **Baseline**: full context resent every iteration
  * **Artifact-based**: artifact loaded once + delta input only

The output shows:

* Total token usage
* Number of unique decision outcomes
* Estimated token savings

---

## How It Works

### 1. Artifact Initialization

* Encodes regimes and rules
* Loaded once (one-time token cost)

### 2. Execution Loop

Each iteration receives only:

* Volatility
* Volume

The decision is derived using the frozen rules.

### 3. Cost Accounting

* **Baseline**: artifact + delta counted every iteration
* **Optimized**: artifact counted once, delta counted per iteration

---

## Running the Demo

### Requirements

* Python 3.9+
* `tiktoken`

### Install Dependency

```bash
pip install tiktoken
```

### Run

```bash
python artifact_demo.py
```

A sample output is included in `results_example.txt`,
so the script does not need to be executed to evaluate the results.

---

## Interpretation

This demo does **not** claim:

* Reduced FLOPs inside the model
* Architectural changes to transformer internals

It demonstrates a **system-level optimization**:

* Less context
* Fewer repeated tokens
* Same decisions

This pattern is applicable to:

* LLM agents
* Real-time analysis
* Long-running loops
* Cost-sensitive deployments

---

## Why This Matters

At scale:

* Repeated context dominates cost
* Eliminating redundancy compounds over time

Freezing decision state turns:

> Repeated reasoning
>
> into
>
> Reusable infrastructure

---

## Scope

This is a minimal demonstration.

It intentionally avoids:

* Production infrastructure
* Model-specific optimizations
* Domain tuning

The goal is **clarity and verifiability**.