# 🚀 LangGraph Learning Journey | Agentic AI & RAG Bootcamp

> A hands-on learning repository where I explore **LangGraph**, **Agentic AI**, **RAG**, **Multi-Agent Systems**, and **LLM Application Development** by implementing concepts learned from **Krish Naik's Ultimate RAG Bootcamp** and the **CampusX LangGraph Playlist**.

---

## 📚 Learning Sources

This repository contains my implementation, experiments, and notes from:

* 🎓 Krish Naik Academy — Ultimate RAG Bootcamp
* 🎓 CampusX — LangGraph Playlist
* 📖 LangGraph Official Documentation
* 📖 LangSmith Documentation

The purpose of this repository is **learning**, **experimentation**, and **building intuition** around production-ready AI Agents.

---

# 🎯 Objectives

This repository focuses on understanding and implementing:

* LangGraph Fundamentals
* Stateful AI Agents
* Multi-step Agentic Workflows
* Tool Calling
* Conditional Routing
* Human-in-the-loop Concepts
* Memory Management
* Retrieval Augmented Generation (RAG)
* Multi-Agent Systems
* Agent Debugging
* Agent Monitoring
* Observability using LangSmith

---

# 🏗️ Overall Architecture

```text
                     +----------------------+
                     |      User Query      |
                     +----------+-----------+
                                |
                                v
                  +----------------------------+
                  |      LangGraph Graph       |
                  |  (State + Workflow Engine) |
                  +-------------+--------------+
                                |
         ---------------------------------------------------
         |                |                |               |
         v                v                v               v
     Planner         Tool Node       Retriever       Memory Node
         |                |                |               |
         -----------------+----------------+---------------
                                |
                                v
                        LLM (Groq API)
                                |
                                v
                       Final AI Response
                                |
                                v
                        LangSmith Tracing
                                |
                                v
                  Monitoring • Debugging • Metrics
```

---

# 🔄 Agent Execution Flow

```text
User Input
     │
     ▼
Receive State
     │
     ▼
Planner Node
     │
     ▼
Need Tool?
 ┌───────────────┐
 │ Yes           │ No
 ▼               ▼
Tool Call      Direct LLM
 │               │
 └──────┬────────┘
        ▼
Update State
        ▼
Generate Response
        ▼
Return Output
        ▼
Log Everything to LangSmith
```

---

# 🧠 LangGraph Workflow

```text
START

   │

   ▼

Read User Input

   │

   ▼

Maintain Graph State

   │

   ▼

Route to Appropriate Node

   │

   ▼

Execute Tool / LLM

   │

   ▼

Update State

   │

   ▼

Conditional Edge

   │

   ▼

END
```

---

# ⚡ Why Groq API?

This repository uses the **Groq API** as the LLM provider during development.

### Why Groq?

✅ Generous Free Tier

Perfect for learning Agentic AI without spending money.

---

✅ Extremely Low Latency

Groq is among the fastest inference providers, making experimentation much smoother.

---

✅ Supports Multiple Open-Source Models

Examples include:

* Llama 3.x
* Gemma
* Qwen
* DeepSeek
* Mixtral

This makes it easy to experiment with different models without changing the application architecture.

---

✅ Easy LangChain Integration

Groq integrates seamlessly with:

* LangChain
* LangGraph
* LCEL
* Tool Calling
* Structured Outputs

---

✅ Cost Efficient

Instead of consuming paid OpenAI credits while learning, Groq's free tier enables rapid experimentation with minimal cost.

---

# 🔍 Why LangSmith?

Building AI Agents is very different from building traditional software.

Unlike normal applications, an AI Agent:

* reasons
* calls tools
* changes state
* makes decisions
* routes between nodes

Understanding **why** an agent produced a particular response is critical.

LangSmith provides exactly that observability layer.

---

# 🔬 LangSmith Workflow

```text
User Request

      │

      ▼

LangGraph Execution

      │

      ▼

Every Node Execution

      │

      ▼

Prompt Logging

      │

      ▼

LLM Response

      │

      ▼

Tool Calls

      │

      ▼

State Updates

      │

      ▼

Token Usage

      │

      ▼

Latency

      │

      ▼

Complete Trace Stored
```

---

# 📊 What LangSmith Helps Me Monitor

### 🔹 Prompt Inspection

View every prompt sent to the LLM.

---

### 🔹 Model Responses

Inspect raw responses before parsing.

---

### 🔹 Agent Decision Flow

Visualize:

* which node executed
* why routing happened
* execution path
* graph traversal

---

### 🔹 Tool Calls

Observe:

* tool selected
* tool inputs
* tool outputs
* execution time

---

### 🔹 Token Usage

Track:

* Prompt Tokens
* Completion Tokens
* Total Tokens

Useful for understanding cost and optimization opportunities.

---

### 🔹 Latency Analysis

Measure execution time for:

* LLM
* Tool Calls
* Entire Workflow

---

### 🔹 Error Debugging

Debug:

* Invalid tool outputs
* State issues
* Prompt failures
* Parsing errors

---

### 🔹 Explainability

One of the biggest advantages of LangSmith is transparency.

Instead of treating an LLM as a black box, LangSmith allows us to understand:

* why a node executed
* which path the agent selected
* how the state evolved
* where failures occurred

This greatly simplifies debugging complex Agentic workflows.

---

# 📂 Repository Structure

```text
.
├── Basics/
├── StateGraph/
├── Nodes/
├── Edges/
├── Conditional_Routing/
├── Tools/
├── Memory/
├── RAG/
├── Multi_Agent/
├── Projects/
├── Experiments/
├── utils/
├── notebooks/
└── README.md
```

---

# 🛠️ Tech Stack

* Python
* LangGraph
* LangChain
* LangSmith
* Groq API
* Open Source LLMs
* Pydantic
* dotenv
* Jupyter Notebook
* VS Code

---

# 🎯 Learning Philosophy

This repository is **not just about copying code**.

For every concept, I try to:

* Understand the theory
* Implement from scratch
* Experiment with variations
* Debug failures
* Observe execution using LangSmith
* Improve the implementation iteratively

The goal is to develop a strong intuition for building reliable, production-ready Agentic AI applications.

---

# 🚀 Future Topics

* Long-Term Memory
* Reflection Agents
* Planning Agents
* ReAct Agents
* Supervisor Architecture
* Multi-Agent Collaboration
* Human-in-the-Loop
* MCP Integration
* Advanced RAG
* Hybrid Search
* Agent Evaluation
* Production Deployment
* FastAPI Integration
* Docker
* Azure Deployment

---

## ⭐ Acknowledgements

A special thanks to **Krish Naik** and **CampusX** for creating high-quality educational content that made learning LangGraph and Agentic AI practical and approachable.

---

> **"Learning by Building."** Every notebook, workflow, and experiment in this repository is part of my journey toward mastering Agentic AI and production-ready LLM applications.
