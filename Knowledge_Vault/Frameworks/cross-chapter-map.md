# Cross-Chapter Connection Map

> **Cross-refs**: [Anti-Patterns](anti-patterns.md) | [Curriculum chapters](../Curriculum/)
> **Scope**: Parts 0–3, 5–7 (Chapters 1–40, 56–57, 61–90)

Use these connections explicitly when teaching to build the student's integrated mental model.

## Part 1 Internal Connections (Ch 12–18)

```
CHAPTER 12 (Paradigm) ─────────────── CHAPTER 16 (SDD)
  "Agent Maturity Model"                "Specifications crystallize
   drives the decision of                incubation insights into
   WHEN to move from                     production-ready artifacts"
   exploration to specs

CHAPTER 12 (Paradigm) ─────────────── CHAPTER 17 (Seven Principles)
  "Orchestrator role"                   "Principles are HOW the
   defines WHAT you become;              orchestrator directs agents
                                         effectively"

CHAPTER 13 (Markdown) ─────────────── CHAPTER 15 (Context Engineering)
  "Markdown syntax"                     "CLAUDE.md is written IN
   is the tool;                          markdown using these skills"

CHAPTER 13 (Markdown) ─────────────── CHAPTER 16 (SDD)
  "Markdown mastery"                    "Specifications ARE
   enables writing...                    markdown documents"

CHAPTER 14 (Claude Code) ──────────── CHAPTER 15 (Context Engineering)
  "CLAUDE.md, Skills,                   "Context engineering is the
   Hooks, Subagents"                     quality control discipline
   are the mechanisms;                   for these mechanisms"

CHAPTER 14 (Claude Code) ──────────── CHAPTER 17 (Seven Principles)
  "Claude Code capabilities"            "Principles guide HOW to
   are the tools;                        use these tools effectively"

CHAPTER 14 (Claude Code) ──────────── CHAPTER 18 (Teams/CI/CD)
  "CLAUDE.md, Skills, Hooks"            "Chapter 18 scales these to
   are individual-level tools;           teams, pipelines, and
                                         shared engineering infrastructure"

CHAPTER 15 (Context Eng) ──────────── CHAPTER 16 (SDD)
  "Context quality"                     "Specifications ARE
   determines output;                    high-quality context"

CHAPTER 15 (Context Eng) ──────────── CHAPTER 18 (Teams/CI/CD)
  "Context architecture"                "Path-specific rules + config
   at individual level;                  hierarchy = team-scale
                                         context architecture"

CHAPTER 16 (SDD) ──────────────────── CHAPTER 18 (Teams/CI/CD)
  "Four-phase workflow"                 "CI/CD integration automates
   for solo development;                 the spec→verify loop at
                                         pipeline scale"

LLM CONSTRAINT RESPONSES:
  Ch.12 Constraint 1 (Statelessness) ── Ch.17 Principle 5 (Persisting State in Files)
  Ch.12 Constraint 2 (Probabilistic)  ── Ch.17 Principle 3 (Verification as Core Step)
  Ch.12 Constraint 3 (Context Window) ── Ch.15 (Context Engineering -- the entire chapter)
```

## Cross-Part Connections

```
PART 0 → PART 1
  Ch 3 (Systems Thinking) ─────────── Ch 12 (Paradigm)
    "Systems thinking is the            "The Agent Factory IS a system:
     prerequisite mental model"          inputs, feedback loops, emergence"

  Ch 6 (Working with AI) ─────────── Ch 14 (Claude Code)
    "General AI collaboration            "Claude Code is the practical
     principles from Part 0"             tool that embodies them"

PART 1 → PART 2
  Ch 12 (Paradigm) ───────────────── Ch 19–24 (Workflow Primitives)
    "Agent maturity model defines        "Workflow primitives are the
     the graduation path"                building blocks for custom agents"

  Ch 17 (Seven Principles) ──────── Ch 23 (Orchestrator-Workers)
    "Orchestrator role principles"       "Orchestrator-Worker pattern is
                                         the architectural realization"

PART 2 → PART 3
  Ch 19–24 (Workflow Primitives) ── Ch 25–40 (Business Domain)
    "Abstract workflow patterns"         "Domain-specific applications
                                         of those patterns"

  Ch 20 (Prompt Chaining) ────────── Ch 27 (Knowledge Extraction)
    "Chain pattern"                      "Applied to document processing
                                         and knowledge extraction"

  Ch 22 (Parallel Workflows) ────── Ch 34 (Sales/Marketing)
    "Parallel execution"                 "Multi-channel campaign
                                         orchestration"

PART 1 → PART 5
  Ch 14 (Claude Code) ────────────── Ch 56 (OpenClaw)
    "General agent usage"                "OpenClaw operationalizes
                                         the AI employee concept"

PART 1 → PART 6
  Ch 12 (Paradigm) ───────────────── Ch 61 (Intro to AI Agents)
    "Conceptual paradigm"                "Technical implementation of
                                         the agent concept"

  Ch 14 (Claude Code) ────────────── Ch 65 (Claude Agent SDK)
    "Claude Code as user tool"           "Claude Agent SDK for building
                                         programmatic agents"

  Ch 15 (Context Engineering) ────── Ch 66–67 (MCP)
    "Context quality principles"         "MCP is the protocol that
                                         enables structured context flow"

  Ch 17 (Seven Principles) ──────── Ch 69 (Multi-Agent Reliability)
    "Verification as core step"          "Systematic reliability for
                                         multi-agent systems"

PART 2 → PART 6
  Ch 23 (Orchestrator-Workers) ──── Ch 62, 63, 65 (Agent SDKs)
    "Orchestration patterns"             "SDK-level implementation of
                                         orchestration patterns"

  Ch 24 (Evaluator-Optimizer) ───── Ch 77 (Evals)
    "Evaluation loop concept"            "Production evaluation
                                         frameworks and tooling"

PART 5 → PART 6
  Ch 56 (OpenClaw) ───────────────── Ch 61 (Intro to AI Agents)
    "AI employee experience"             "Deep technical understanding
                                         of what powers the employee"

PART 6 INTERNAL CONNECTIONS
  Ch 61 (Intro) ──────────────────── Ch 62–65 (SDK chapters)
    "Agent concepts"                     "SDK-specific implementations"

  Ch 62 (OpenAI SDK) ─────────────── Ch 63 (Google ADK)
    "OpenAI approach"                    "Google approach — compare
                                         design philosophies"

  Ch 64 (Claude API) ─────────────── Ch 65 (Claude Agent SDK)
    "Low-level API"                      "High-level SDK built on
                                         the API"

  Ch 66 (MCP Fundamentals) ──────── Ch 67 (Advanced MCP)
    "Protocol basics"                    "Production server development"

  Ch 67 (Advanced MCP) ──────────── Ch 68 (Agent Skills + Code Exec)
    "MCP servers"                        "Skills that wrap MCP tools
                                         and execute code"

  Ch 70 (FastAPI) ────────────────── Ch 71 (ChatKit)
    "API framework"                      "Chat server built on
                                         FastAPI patterns"

  Ch 73 (Vector DB/RAG) ─────────── Ch 75 (Augmented Memory)
    "Retrieval-augmented generation"     "Memory systems that USE
                                         vector retrieval"

  Ch 74 (Relational DB) ─────────── Ch 70 (FastAPI)
    "Database layer"                     "API layer that exposes
                                         database operations"

  Ch 76 (TDD) ────────────────────── Ch 77 (Evals)
    "Testing methodology"                "Evaluation methodology —
                                         TDD for correctness, evals for quality"

PART 6 → PART 7
  Ch 70 (FastAPI) ────────────────── Ch 79 (Docker)
    "API application"                    "Containerizing the application"

  Ch 65 (Claude Agent SDK) ──────── Ch 80 (Kubernetes)
    "Agent application"                  "Deploying agents to K8s"

  Ch 76 (TDD) ────────────────────── Ch 84 (CI/CD)
    "Test suite"                         "Tests run in CI pipeline"

  Ch 77 (Evals) ──────────────────── Ch 85 (Observability)
    "Agent quality metrics"              "Production monitoring of
                                         agent performance"

PART 7 INTERNAL CONNECTIONS
  Ch 79 (Docker) ─────────────────── Ch 80 (Kubernetes)
    "Container images"                   "Orchestrating containers"

  Ch 80 (K8s) ────────────────────── Ch 81 (Helm)
    "K8s manifests"                      "Packaging manifests as charts"

  Ch 82 (Kafka) ──────────────────── Ch 83 (Dapr Core)
    "Event-driven messaging"             "Dapr pub/sub abstracts
                                         the Kafka details"

  Ch 83 (Dapr Core) ──────────────── Ch 87 (Dapr Actors/Workflows)
    "Dapr building blocks"               "Advanced Dapr: actors +
                                         workflow orchestration"

  Ch 84 (CI/CD) ──────────────────── Ch 90 (Real Cloud Deployment)
    "Pipeline automation"                "Deploying via GitOps to
                                         real cloud infrastructure"

  Ch 85 (Observability) ─────────── Ch 89 (Cost & DR)
    "Monitoring stack"                   "Cost visibility and
                                         disaster recovery planning"

  Ch 86 (Traffic Engineering) ───── Ch 88 (Production Security)
    "Traffic routing"                    "Security at the traffic layer"
```
