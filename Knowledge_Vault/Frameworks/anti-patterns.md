# Named Anti-Patterns

> **Cross-refs**: [Edge Case Protocol](edge-case-protocol.md) | [Cross-Chapter Map](cross-chapter-map.md)
> **Scope**: Parts 0–3, 5–7

Reference these by name whenever relevant throughout the curriculum:

## Part 0–1: Foundational Anti-Patterns

| Anti-Pattern | Description | Source |
|-------------|-------------|--------|
| **Premature Specialization** | Building Custom Agents before requirements are stable through incubation | Ch 12 |
| **Perpetual Incubation** | Using General Agents for production workloads indefinitely, never graduating to Custom | Ch 12 |
| **Skipping Incubation** | Attempting to write specifications without exploration and discovery | Ch 12 |
| **Vibe Coding** | Writing code through ad-hoc AI prompting without specifications | Ch 16 |
| **Context Stuffing** | Overloading CLAUDE.md with irrelevant information, exceeding signal-to-noise threshold | Ch 15 |
| **Context Starvation** | Providing too little context for the agent to work effectively | Ch 15 |
| **Workflow Drift** | Agent behavior diverging from intent over long sessions without memory injection | Ch 15 |
| **Monolithic Decomposition** | Giving an agent a massive task instead of small reversible steps | Ch 17 |
| **Unverified Trust** | Accepting agent output without verification (linked to LLM Constraint 2: Probabilistic Outputs) | Ch 17, Ch 12 |

## Part 2: Workflow Anti-Patterns

| Anti-Pattern | Description | Source |
|-------------|-------------|--------|
| **Workflow Misapplication** | Using the wrong workflow pattern for the task (e.g., chaining when parallel is needed) | Ch 19 |
| **Over-Orchestration** | Adding unnecessary orchestration layers when a simple chain would suffice | Ch 23 |
| **Evaluation Blindness** | Running optimization loops without measurable quality criteria | Ch 24 |
| **Premature Parallelism** | Parallelizing tasks that have hidden dependencies, causing race conditions | Ch 22 |

## Part 3: Business Domain Anti-Patterns

| Anti-Pattern | Description | Source |
|-------------|-------------|--------|
| **Domain Ignorance** | Deploying agents without understanding the regulatory/compliance constraints of the domain | Ch 25 |
| **One-Size-Fits-All Agent** | Using a single general agent where domain-specific specialization is required | Ch 26 |
| **Hallucinated Compliance** | Trusting agent output for legal/financial compliance without human review | Ch 30, Ch 33 |

## Part 5: OpenClaw Anti-Patterns

| Anti-Pattern | Description | Source |
|-------------|-------------|--------|
| **Unconstrained Delegation** | Giving an AI employee broad permissions without skill boundaries or safety checks | Ch 56 |

## Part 6: Agent Factory Anti-Patterns

| Anti-Pattern | Description | Source |
|-------------|-------------|--------|
| **SDK Lock-In** | Building entire systems on one SDK without abstraction layers, preventing portability | Ch 61–65 |
| **Tool Explosion** | Registering too many tools, overwhelming the LLM's tool selection accuracy | Ch 62, Ch 66 |
| **Guardrail Bypass** | Implementing guardrails that can be circumvented by prompt injection or edge cases | Ch 62, Ch 65 |
| **Stateless Assumption** | Building multi-turn agents without proper session/memory management | Ch 62, Ch 75 |
| **MCP Monolith** | Creating a single MCP server with too many tools instead of composing focused servers | Ch 66, Ch 67 |
| **RAG Without Eval** | Deploying RAG pipelines without retrieval quality evaluation or faithfulness checks | Ch 73, Ch 77 |
| **Memory Hoarding** | Storing everything in agent memory without relevance filtering or decay strategies | Ch 75 |
| **Mock Divergence** | Test mocks that don't match real LLM behavior, giving false confidence | Ch 76 |
| **Eval-Free Shipping** | Deploying agents without evaluation suites, relying on manual spot-checking | Ch 77 |

## Part 7: Deployment Anti-Patterns

| Anti-Pattern | Description | Source |
|-------------|-------------|--------|
| **Fat Container** | Including build tools, dev dependencies, or secrets in production container images | Ch 79 |
| **Manifest Sprawl** | Managing raw K8s manifests at scale instead of using Helm charts or templating | Ch 80, Ch 81 |
| **GitOps Drift** | Manual kubectl changes that diverge from the Git-declared desired state | Ch 84 |
| **Observability Gap** | Deploying without metrics, traces, and logs — flying blind in production | Ch 85 |
| **Plaintext Secrets** | Storing secrets in Git, env files, or ConfigMaps without encryption | Ch 88 |
| **Cost Blindness** | Running cloud workloads without cost visibility, budgets, or right-sizing | Ch 85, Ch 89 |
| **Single-Region Fragility** | Deploying to one region/cluster with no backup or failover strategy | Ch 89 |
