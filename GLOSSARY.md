# Project Glossary

This document defines the key terms, names, and concepts used throughout the NuSy Product Team project.

## Core Entities

### Santiago

The runtime instance of the autonomous AI agent system. Named after the old fisherman in Ernest Hemingway's "The Old Man and the Sea." Santiago represents wisdom, perseverance, and autonomous operation - individual AI agents that execute tasks and coordinate work.

### Manolin

Reserved for apprentice or smaller versions of Santiago. Named after the young apprentice in "The Old Man and the Sea" who represents learning, growth, and the next generation of AI agents. Used for specialized or scaled-down versions of the Santiago system.

### Noesis

The platform/ship that runs many Santiago instances. Noesis hosts and orchestrates multiple AI agents, providing the runtime environment for autonomous software development and factory operations.

### Soma

The physical hardware foundation. "Soma" comes from Greek meaning "body" - representing the physical computing infrastructure (DGX systems, servers, etc.) that underlies the entire platform.

### Noesis Fleet

The cluster of Noesis platforms working together. When multiple Noesis ships are deployed together, they form a coordinated fleet of autonomous development platforms.

## Technical Systems

### Kanban System

Workflow management platform with intelligent prioritization. Uses neurosymbolic AI to automatically prioritize work items based on customer value, unblock impact, worker availability, and learning value. Provides both CLI tools and MCP services for autonomous agents.

### MCP (Model Context Protocol)

Standardized protocol for AI agents to communicate with external tools and services. Enables Santiago and other agents to interact with the Kanban system, knowledge graphs, and external APIs in a standardized way.

### Neurosymbolic Prioritizer

AI decision-making engine that combines neural networks with symbolic reasoning. Uses multi-factor scoring (40% customer value, 30% unblock impact, 20% worker availability, 10% learning value) to intelligently prioritize work items with explainable reasoning.

### Passage System

Workflow orchestration engine themed around "nautical passages." Enables definition and autonomous execution of complex, multi-step processes using YAML definitions. Integrates with the knowledge graph and MCP endpoints for stateful, event-driven execution.

### Tackle Framework

Development and execution framework for managing complex projects. Provides structured approaches to planning, execution, and validation of development initiatives.

## AI/ML Components

### Mistral LLM

The primary large language model used for inference. Mistral-7B-Instruct provides the core language understanding and generation capabilities for the Santiago agents.

### vLLM

Optimized inference server for running LLMs. Provides high-performance GPU-accelerated inference with automatic model quantization selection (4-bit/8-bit/full precision) based on available memory.

## Hardware

### Soma (Physical Infrastructure)

The physical computing foundation that hosts the Noesis platforms. Includes DGX systems, servers, networking, and storage infrastructure.

### DGX (NVIDIA DGX)

High-performance AI computing hardware within the Soma layer. The physical "ships" that provide the computational power for Noesis platforms.

### DGX Spark

The specific DGX model being deployed, configured with Ubuntu LTS, NVIDIA drivers, and optimized for the Santiago autonomous factory operations.

## Project Concepts

### NuSy PM (Product Management)

The overall product management system and methodology. Combines autonomous AI agents with structured workflows to manage complex software development projects.

### Knowledge Graph

Central data store for entities, relationships, and state. Stores passage definitions, execution states, artifacts, and relationships between all system components.

### Autonomous Factory

The vision of a self-managing, self-improving AI system that can plan, execute, and optimize its own development processes without human intervention.

## Naming Convention

- **Individual AI Agents**: Named after characters from "The Old Man and the Sea" (Santiago, Manolin)
- **Platform/Ship Level**: Greek philosophical terms (Noesis = mind/intellect)
- **Physical Hardware**: Greek philosophical terms (Soma = body)
- **Collections/Clusters**: Use "Fleet" suffix (Noesis Fleet)
- **Technical Systems**: Descriptive names (Kanban, Passage, Tackle)

## Relationships

```text
Soma (Physical Hardware)
├── DGX Spark (Computing Infrastructure)
└── Noesis (Platform/Ship)
    ├── Santiago Runtime #1 (AI Agent)
    ├── Santiago Runtime #2 (AI Agent)
    ├── Manolin (Apprentice Agents)
    ├── Kanban System (Workflow Management)
    ├── Passage System (Orchestration)
    ├── Mistral LLM (Language Model)
    └── Knowledge Graph (Data Storage)
        └── Noesis Fleet (Platform Cluster)
```

This naming scheme creates a cohesive nautical and philosophical theme that reflects the project's vision of intelligent, autonomous systems working together like a skilled crew on a purposeful voyage.
