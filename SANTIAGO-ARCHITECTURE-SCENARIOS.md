# 🏗️ Santiago Architecture Scenarios

**Understanding How Santiago Agents Work Across Different Contexts**

*Generated: November 18, 2025*

---

## 🎯 **Scenario 1: Normal Operation - Working on Kanban Features**

*Agents working on regular development tasks from the kanban board*

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  TRADITIONAL GIT REPOSITORIES (Persistent Storage)                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  nusy-product-team/                                                           │
│  ├── santiago_core/          # Santiago framework code                        │
│  ├── santiago-pm/            # Kanban system & PM tools                       │
│  ├── features/               # Feature definitions                            │
│  ├── expeditions/            # Research expeditions                           │
│  └── requirements.txt        # Dependencies                                   │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │  (Platform deployment)
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│  NÓESIS FACTORY RUNTIME (In-Memory Workspace)                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  SHARED IN-MEMORY GIT WORKSPACE                                        │   │
│  │  Repository: memory://santiago-workspace                               │   │
│  │  Branches: main, feature-*, expedition-*                               │   │
│  │  Files: Generated code, docs, research outputs                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                           │
│  │ Santiago-PM │  │ Santiago-   │  │ Santiago-   │                           │
│  │ Agent       │  │ Architect   │  │ Developer  │                           │
│  │             │  │ Agent       │  │ Agent      │                           │
│  │ Knowledge:  │  │             │  │            │                           │
│  │ • PM Graph  │  │ Knowledge:  │  │ Knowledge: │                           │
│  │ • Kanban    │  │ • Arch Graph│  │ • Dev Graph│                           │
│  │ • Strategy  │  │ • Design    │  │ • Code     │                           │
│  └─────────────┘  └─────────────┘  └─────────────┘                           │
│         │                │                │                                   │
│         └────────────────┼────────────────┘                                   │
│                          │                                                    │
│                 ┌────────▼────────┐                                           │
│                 │ MESSAGE BUS     │                                           │
│                 │ (Redis pub/sub) │                                           │
│                 └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**WORKFLOW:**
1. Kanban board shows: "Implement User Authentication" (feature)
2. Santiago-PM assigns task to Santiago-Developer
3. Santiago-Developer works in shared in-memory Git workspace
4. Code generated and committed to memory://santiago-workspace
5. Results can be exported to nusy-product-team/ if needed

---

## 🔄 **Scenario 2: Self-Improvement - Working on Santiago Framework**

*Agents improving their own capabilities and the Nóesis platform*

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  TRADITIONAL GIT REPOSITORIES (Persistent Storage)                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  nusy-product-team/                                                           │
│  ├── santiago_core/          # ⭐ TARGET: Improving this code                 │
│  │   ├── core/               # Agent framework                                │
│  │   ├── agents/             # Agent implementations                          │
│  │   ├── services/           # Knowledge graph, Git service                  │
│  │   └── run_team.py         # ⭐ TARGET: Improving deployment                │
│  ├── santiago-pm/            # Kanban system                                  │
│  └── features/               # New capabilities to implement                  │
│                                                                             │
│  santiago-dev/                # Development workspace                         │
│  ├── workspace/               # Temporary development files                   │
│  └── experiments/             # Research outputs                             │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │  (Self-improvement cycle)
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│  NÓESIS FACTORY RUNTIME (Self-Improvement Mode)                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  SHARED IN-MEMORY GIT WORKSPACE                                        │   │
│  │  Repository: memory://santiago-self-improvement                        │   │
│  │  Branches: improve-agents, enhance-framework, optimize-performance     │   │
│  │  Files: Modified santiago_core/, new agent capabilities                 │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                           │
│  │ Santiago-PM │  │ Santiago-   │  │ Santiago-   │                           │
│  │ Agent       │  │ Architect   │  │ Developer  │                           │
│  │ (Meta-PM)   │  │ (Meta-Arch) │  │ (Meta-Dev) │                           │
│  │             │  │             │  │            │                           │
│  │ Knowledge:  │  │ Knowledge:  │  │ Knowledge: │                           │
│  │ • Framework │  │ • System    │  │ • Code     │                           │
│  │ • Strategy  │  │ • Design    │  │ • Impl     │                           │
│  └─────────────┘  └─────────────┘  └─────────────┘                           │
│         │                │                │                                   │
│         └────────────────┼────────────────┘                                   │
│                          │                                                    │
│                 ┌────────▼────────┐                                           │
│                 │ MESSAGE BUS     │                                           │
│                 │ (Redis pub/sub) │                                           │
│                 └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**WORKFLOW:**
1. Kanban shows: "Enhance Santiago Agent Reasoning" (self-improvement task)
2. Santiago-PM analyzes current framework weaknesses
3. Santiago-Architect designs improvements to santiago_core/
4. Santiago-Developer implements changes in memory://santiago-self-improvement
5. Changes tested and validated
6. Successful improvements merged back to nusy-product-team/santiago_core/
7. Framework restarted with enhanced capabilities

---

## 🌍 **Scenario 3: New Domain - External Project Development**

*Agents working on projects outside the Nóesis ecosystem*

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  TRADITIONAL GIT REPOSITORIES (Persistent Storage)                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  nusy-product-team/                                                           │
│  ├── santiago_core/          # Agent framework (unchanged)                    │
│  └── santiago-pm/            # Kanban system                                  │
│                                                                             │
│  external-project/           # ⭐ NEW: Target project repository              │
│  ├── src/                    # Existing codebase                              │
│  ├── tests/                  # Test suite                                     │
│  ├── docs/                   # Documentation                                 │
│  └── README.md               # Project info                                  │
│                                                                             │
│  santiago-client-repos/      # Client project repositories                   │
│  ├── client-a/               # Client A's project                            │
│  ├── client-b/               # Client B's project                            │
│  └── client-c/               # Client C's project                            │
└─────────────────────┬───────────────────────────────────────────────────────────┘
                      │  (Domain adaptation)
                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│  NÓESIS FACTORY RUNTIME (Domain Adaptation Mode)                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  SHARED IN-MEMORY GIT WORKSPACE                                        │   │
│  │  Repository: memory://external-project-workspace                       │   │
│  │  Branches: feature-*, bugfix-*, refactor-*                             │   │
│  │  Files: Adapted code for new domain, new features                      │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Santiago-PM │  │ Santiago-   │  │ Santiago-   │  │ Domain      │           │
│  │ Agent       │  │ Architect   │  │ Developer  │  │ Expert      │           │
│  │ (Project    │  │ (System     │  │ (Code      │  │ Agent       │           │
│  │ Manager)    │  │ Architect)  │  │ (Code      │  │ (Specialized)│           │
│  │             │  │             │  │ Developer) │  │             │           │
│  │ Knowledge:  │  │ Knowledge:  │  │ Knowledge: │  │ Knowledge:  │           │
│  │ • PM Graph  │  │ • Arch Graph│  │ • Dev Graph│  │ • Domain    │           │
│  │ • Strategy  │  │ • Design    │  │ • Code     │  │ • Expertise │           │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘           │
│         │                │                │                │                   │
│         └────────────────┼────────────────┼────────────────┘                   │
│                          │                                                    │
│                 ┌────────▼────────┐                                           │
│                 │ MESSAGE BUS     │                                           │
│                 │ (Redis pub/sub) │                                           │
│                 └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**WORKFLOW:**
1. External request: "Build E-commerce Platform for Client A"
2. Santiago-PM analyzes requirements and domain
3. Domain Expert Agent loaded with e-commerce knowledge
4. Santiago-Architect designs system for new domain
5. Santiago-Developer implements in memory://external-project-workspace
6. Work exported to external-project/ repository
7. Client receives completed project

---

## 🎭 **Additional Scenarios**

### **Scenario 4: Multi-Project Parallel Processing**

```
REPOSITORIES: nusy-product-team/, project-a/, project-b/, project-c/
IN-MEMORY: memory://multi-project-workspace (with sub-workspaces)
AGENTS: 7 Santiago instances across 3 projects simultaneously
FEATURE: Parallel autonomous development on multiple domains
```

### **Scenario 5: Research & Experimentation Mode**

```
REPOSITORIES: nusy-product-team/, research-logs/
IN-MEMORY: memory://research-workspace (experimental branches)
AGENTS: Santiago instances with research-focused knowledge graphs
FEATURE: Autonomous hypothesis testing and experimental development
```

### **Scenario 6: Nóesis Fleet Coordination**

```
REPOSITORIES: nusy-product-team/, fleet-config/
IN-MEMORY: memory://fleet-coordination (inter-factory communication)
AGENTS: Santiago instances coordinating across multiple Nóesis factories
FEATURE: Distributed autonomous development across hardware clusters
```

---

## 🔑 **Key Similarities & Differences**

**Similar Across All Scenarios:**
- `nusy-product-team/` - Always contains the core Santiago framework
- In-memory Git workspace - Always the active development environment
- Agent knowledge graphs - Each agent maintains domain-specific learning
- Message bus - Inter-agent communication mechanism

**Differences by Scenario:**

| Scenario | Primary Target Repo | In-Memory Repo Purpose | Agent Focus |
|----------|-------------------|----------------------|-------------|
| Normal | `nusy-product-team/features/` | Feature implementation | Task execution |
| Self-Improvement | `nusy-product-team/santiago_core/` | Framework enhancement | Meta-development |
| New Domain | `external-project/` | Domain adaptation | Client deliverables |
| Multi-Project | Multiple external repos | Parallel workspaces | Resource allocation |
| Research | `research-logs/` | Hypothesis testing | Innovation |
| Fleet | `fleet-config/` | Inter-factory coordination | Distributed orchestration |

---

## 🧠 **Core Architecture Principles**

### **Dual Git Worlds**
- **Traditional Git**: `nusy-product-team/` - Platform persistence and human collaboration
- **In-Memory Git**: `memory://*` - High-performance autonomous development workspace

### **Agent Model**
- **Shared Framework**: All Santiagos are instances of the same core framework
- **Specialized Knowledge**: Each agent has domain-specific knowledge graphs
- **Collaborative Workspace**: All agents work in the same in-memory Git environment
- **Inter-Agent Communication**: Redis pub/sub message bus for coordination

### **Self-Improvement Cycle**
1. Agents identify framework weaknesses through experience
2. Self-improvement tasks added to kanban board
3. Agents work on enhancements in isolated in-memory workspace
4. Successful changes merged back to traditional Git
5. Framework restarted with improved capabilities

---

## 📚 **Repository Structure Reference**

```
nusy-product-team/           # Core platform repository
├── santiago_core/          # Agent framework and runtime
├── santiago-pm/            # Product management tools
├── features/               # Feature definitions
├── expeditions/            # Research expeditions
├── tests/                  # Test suites
└── requirements.txt        # Dependencies

santiago-dev/               # Development workspace
├── workspace/              # Temporary files
└── experiments/            # Research outputs

external-project/           # Client project repositories
├── src/                    # Source code
├── tests/                  # Tests
└── docs/                   # Documentation
```

---

*This document explains how Santiago agents flexibly adapt their architecture across different development contexts while maintaining the core in-memory Git collaboration model.*