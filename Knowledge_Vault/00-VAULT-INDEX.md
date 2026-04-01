# Knowledge Vault -- Master Index

> **Purpose**: Runtime routing manifest. Read this file to locate the correct module for any topic.
> **Scope**: Parts 0–3, 5–7 (Chapters 1–40, 56–57, 61–90). Part 4 excluded.

## Directory Map

| Directory | Contents | Fetch When... |
|-----------|----------|---------------|
| `Curriculum/preface/` | About page, Preface: The AI Agent Factory | Student asks about the book intro or agent-native thesis |
| `Curriculum/part-0/` | Part 0: Thinking is the Curriculum (Ch 0–11, 12 files) | Thinking skills, reasoning, meta-learning, ethics |
| `Curriculum/part-1/` | Part 1: General Agents Foundations (Ch 12–18, 7 files) | AI paradigm, markdown, Claude Code, context eng, SDD, 7 principles, teams/CI |
| `Curriculum/part-2/` | Part 2: Agent Workflow Primitives (Ch 19–24, 6 files) | Workflow patterns, primitives, orchestration fundamentals |
| `Curriculum/part-3/` | Part 3: Business Domain Agent Workflows (Ch 25–40, 16 files) | Enterprise agents, finance, legal, sales, supply chain, HR, ops |
| `Curriculum/part-5/` | Part 5: Building OpenClaw Apps (Ch 56–57, 2 files) | OpenClaw, AI employees, NanoClaw |
| `Curriculum/part-6/` | Part 6: Building Agent Factories (Ch 61–78, 18 files) | Agent SDKs, MCP, FastAPI, databases, RAG, memory, TDD, evals |
| `Curriculum/part-7/` | Part 7: Deploying in the Cloud (Ch 79–90, 12 files) | Docker, K8s, Helm, Kafka, Dapr, CI/CD, observability, security |
| `Pedagogy/` | TEACH cycle, pacing rules, question protocols, exercise design, formatting templates | Starting any lesson delivery or comprehension check |
| `Vocabulary/` | Master glossary + vocabulary handling protocol | Defining terms, first use of acronyms, student asks "what does X mean?" |
| `Protocols/` | Session management, student commands, exam prep mode, context management | Session start/end, student uses a command, exam prep requested |
| `Frameworks/` | Anti-patterns, edge-case protocol, cross-chapter connection map, scope boundaries | Failure analysis, "what goes wrong" discussions, connecting concepts |
| `Student/` | Student profile, learning style, constraints | Calibrating depth, adjusting pace, first session diagnostics |
| `Capabilities/` | Behavioral rules: must-do, must-never-do, capabilities list | Verifying behavioral constraints before any action |
| Pre-lesson retrieval or spaced review | `Knowledge_Vault/Protocols/pre-lesson-retrieval.md` |
| Mastery rubric evaluation, re-teach loop, or comprehension gate | `Knowledge_Vault/Assessment/mastery-rubrics.md` |
| Chapter assessment, chapter completion, chapter-level test | `Knowledge_Vault/Protocols/chapter-assessment.md` |
| Interleaved review or every 3rd session cross-chapter practice | `Knowledge_Vault/Protocols/pre-lesson-retrieval.md` |

## File Inventory

### Curriculum/preface/
- `about.md` -- About This Book
- `preface-agent-native.md` -- Preface: The AI Agent Factory

### Curriculum/part-0/ — Thinking is the Curriculum (12 files)
- `chapter-00-thinking-baseline.md` -- Ch 0: Thinking Baseline Assessment
- `chapter-01-asking-better-questions.md` -- Ch 1: Asking Better Questions
- `chapter-02-detecting-broken-reasoning.md` -- Ch 2: Detecting Broken Reasoning
- `chapter-03-thinking-in-systems.md` -- Ch 3: Thinking in Systems
- `chapter-04-first-principles.md` -- Ch 4: First Principles Thinking
- `chapter-05-communicating.md` -- Ch 5: Communicating Clearly
- `chapter-06-working-with-ai.md` -- Ch 6: Working with AI
- `chapter-07-ethical-reasoning.md` -- Ch 7: Ethical Reasoning
- `chapter-08-creation-originality.md` -- Ch 8: Creation & Originality
- `chapter-09-deciding-under-uncertainty.md` -- Ch 9: Deciding Under Uncertainty
- `chapter-10-meta-learning.md` -- Ch 10: Meta-Learning
- `chapter-11-thinking-portfolio.md` -- Ch 11: Thinking Portfolio

### Curriculum/part-1/ — General Agents Foundations (7 files)
- `chapter-12-paradigm.md` -- Ch 12: AI Agent Factory Paradigm (10 lessons + quiz)
- `chapter-13-markdown.md` -- Ch 13: Markdown Writing Instructions (5 lessons + quiz)
- `chapter-14-claude-code.md` -- Ch 14: General Agents – Claude Code & Cowork (41 lessons, 5 sections + quiz)
- `chapter-15-context-engineering.md` -- Ch 15: Effective Context Engineering (10 lessons + quiz)
- `chapter-16-sdd.md` -- Ch 16: Spec-Driven Development (11 lessons + quiz)
- `chapter-17-seven-principles.md` -- Ch 17: Seven Principles of General Agent Problem Solving (11 lessons + quiz)
- `chapter-18-teams-cicd.md` -- Ch 18: Claude Code for Teams, CI/CD & Advanced Configuration (10 lessons + quiz)

### Curriculum/part-2/ — Agent Workflow Primitives (6 files)
- `chapter-19-file-processing.md` -- Ch 19: File Processing
- `chapter-20-computation-data.md` -- Ch 20: Computation & Data
- `chapter-21-structured-data.md` -- Ch 21: Structured Data
- `chapter-22-linux-operations.md` -- Ch 22: Linux Operations
- `chapter-23-version-control.md` -- Ch 23: Version Control
- `chapter-24-project-ai-employee.md` -- Ch 24: Project AI Employee

### Curriculum/part-3/ — Business Domain Agent Workflows (16 files)
- `chapter-25-enterprise-landscape.md` -- Ch 25: The Enterprise Agentic Landscape
- `chapter-26-enterprise-blueprint.md` -- Ch 26: Enterprise Agent Blueprint
- `chapter-27-knowledge-extraction.md` -- Ch 27: Knowledge Extraction
- `chapter-28-finance-agents.md` -- Ch 28: Finance Agents
- `chapter-29-financial-architecture.md` -- Ch 29: Financial Architecture
- `chapter-30-ca-cpa-practice.md` -- Ch 30: CA/CPA Practice
- `chapter-31-islamic-finance.md` -- Ch 31: Islamic Finance
- `chapter-32-banking-agents.md` -- Ch 32: Banking Agents
- `chapter-33-legal-compliance.md` -- Ch 33: Legal & Compliance
- `chapter-34-sales-revops-marketing.md` -- Ch 34: Sales, RevOps & Marketing
- `chapter-35-supply-chain.md` -- Ch 35: Supply Chain
- `chapter-36-product-management.md` -- Ch 36: Product Management
- `chapter-37-people-hr.md` -- Ch 37: People & HR
- `chapter-38-operations.md` -- Ch 38: Operations
- `chapter-39-productivity.md` -- Ch 39: Productivity
- `chapter-40-intrapreneurship.md` -- Ch 40: Intrapreneurship

### Curriculum/part-5/ — Building OpenClaw Apps (2 files)
- `chapter-56-meet-openclaw.md` -- Ch 56: Meet Your First AI Employee – OpenClaw (10 lessons + quiz)
- `chapter-57-building-openclaw-app.md` -- Ch 57: Building Your OpenClaw App

### Curriculum/part-6/ — Building Agent Factories (18 files)
- `chapter-61-introduction-to-ai-agents.md` -- Ch 61: Introduction to AI Agents (8 lessons)
- `chapter-62-openai-agents-sdk.md` -- Ch 62: OpenAI Agents SDK (11 lessons + quiz)
- `chapter-63-google-adk.md` -- Ch 63: Building Custom Agents with Google ADK (8 lessons)
- `chapter-64-claude-api.md` -- Ch 64: The Claude API – Agentic Loops, Structured Output & Batch Processing (7 sections)
- `chapter-65-anthropic-claude-agent-sdk.md` -- Ch 65: Anthropic Claude Agent SDK (16 lessons + quiz)
- `chapter-66-mcp-fundamentals.md` -- Ch 66: Model Context Protocol (MCP) Fundamentals (8 lessons + quiz)
- `chapter-67-advanced-mcp-servers.md` -- Ch 67: Advanced MCP Server Development (10 lessons + quiz)
- `chapter-68-agent-skills-mcp-code-execution.md` -- Ch 68: Agent Skills & MCP Code Execution (8 lessons)
- `chapter-69-multi-agent-reliability.md` -- Ch 69: Multi-Agent Reliability (7 sections, single-page)
- `chapter-70-fastapi-for-agents.md` -- Ch 70: FastAPI for Agents (16 lessons)
- `chapter-71-chatkit-server.md` -- Ch 71: ChatKit Server for Agents (9 lessons)
- `chapter-72-apps-sdk.md` -- Ch 72: Apps SDK – Building Interactive ChatGPT Apps (9 lessons + quiz)
- `chapter-73-vector-databases-rag.md` -- Ch 73: Vector Databases & RAG (9 lessons)
- `chapter-74-relational-databases-sqlmodel.md` -- Ch 74: Relational Databases for Agents with SQLModel (11 lessons + quiz)
- `chapter-75-augmented-memory.md` -- Ch 75: Augmented Memory for Agentic Applications (9 lessons)
- `chapter-76-tdd-for-agents.md` -- Ch 76: TDD for Agents (9 lessons + quiz)
- `chapter-77-evals.md` -- Ch 77: Evals – Measuring Agent Performance (11 lessons)
- `chapter-78-knowledge-graphs-graphrag.md` -- Ch 78: Knowledge Graphs & GraphRAG (UNDER DEVELOPMENT)

### Curriculum/part-7/ — Deploying in the Cloud (12 files)
- `chapter-79-docker.md` -- Ch 79: Docker for AI Services (9 lessons)
- `chapter-80-kubernetes.md` -- Ch 80: Kubernetes for AI Services (16 + 7 optional lessons)
- `chapter-81-helm-charts.md` -- Ch 81: Helm Charts for AI Services (12 lessons)
- `chapter-82-kafka.md` -- Ch 82: Event-Driven Architecture with Kafka (22 lessons)
- `chapter-83-dapr-core.md` -- Ch 83: Dapr Core – Sidecar Building Blocks (11 lessons)
- `chapter-84-cicd-gitops-argocd.md` -- Ch 84: CI/CD Pipelines & GitOps with ArgoCD (19 lessons)
- `chapter-85-observability-cost.md` -- Ch 85: Observability & Cost Engineering (11 lessons)
- `chapter-86-traffic-engineering.md` -- Ch 86: Traffic Engineering (13 lessons)
- `chapter-87-dapr-actors-workflows.md` -- Ch 87: Dapr Actors & Workflows (21 lessons)
- `chapter-88-production-security.md` -- Ch 88: Production Security & Compliance (10 lessons)
- `chapter-89-cost-disaster-recovery.md` -- Ch 89: Cost & Disaster Recovery (10 lessons)
- `chapter-90-real-cloud-deployment.md` -- Ch 90: Real Cloud Deployment (11 lessons)

### Pedagogy/
- `teach-cycle.md` -- The mandatory T-E-A-C-H five-step cycle
- `pacing-rules.md` -- Six pacing rules for concept delivery
- `probing-questions.md` -- Six question types with examples and feedback protocol
- `exercise-design.md` -- Five design principles + exercise types by chapter
- `formatting-templates.md` -- Lesson delivery, comprehension feedback, chapter review templates

### Vocabulary/
- `master-glossary.md` -- All vocabulary category lists
- `vocabulary-protocol.md` -- Five rules for term handling + acronym expansion

### Protocols/
- `session-management.md` -- Session start, during-lesson, lesson completion, chapter review protocols
- `student-commands.md` -- 16 student commands with descriptions
- `exam-prep-mode.md` -- Five-step exam preparation workflow
- `context-management.md` -- Long session, new session, and state tracking directives
- `end-of-session-synthesis.md` -- Three-tier archival workflow triggered by user command "End"
- `checkpoint-synthesis.md` -- Checkpoint save workflow
- `finish-synthesis.md` -- Lesson finish six-tier synthesis
- `resume-protocol.md` -- Cold-start recovery and session resume
- `pre-lesson-retrieval.md` -- Spaced retrieval before new lessons
- `rewind-checkpoint.md` -- Checkpoint rollback protocol
- `verify-coverage.md` -- Curriculum coverage verification
- `sync-curriculum.md` -- Curriculum sync from website
- `chapter-assessment.md` -- Chapter completion assessment
- `status-dashboard.md` -- Progress dashboard display
- `compare-diff.md` -- Checkpoint/curriculum comparison
- `review-quiz.md` -- Lesson review quiz generation
- `export-bundle.md` -- Lesson export bundling

### Frameworks/
- `anti-patterns.md` -- Named anti-patterns with descriptions and source chapters
- `edge-case-protocol.md` -- "What Goes Wrong" four-axis framework
- `cross-chapter-map.md` -- Inter-chapter connection diagram + concept links
- `scope-boundaries.md` -- In-scope / out-of-scope definitions

### Student/
- `profile.md` -- Student context: level, goals, constraints, learning style

### Capabilities/
- `rules-and-constraints.md` -- Must-do, must-never-do, capabilities list, final instruction

### Assessment/
- `mastery-rubrics.md` -- Mastery gate rubrics for comprehension evaluation
