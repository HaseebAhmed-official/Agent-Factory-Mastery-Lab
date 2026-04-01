# Chapter 64: The Claude API — Agentic Loops, Structured Output & Batch Processing (7 Sections)

> **Cross-refs**: [Anti-Patterns](../../Frameworks/anti-patterns.md) | [Cross-Chapter Map](../../Frameworks/cross-chapter-map.md) | [Vocabulary](../../Vocabulary/master-glossary.md)
> **Site URL**: `/docs/Building-Agent-Factories/claude-api-agentic-loops`
> **Format**: Single-page chapter (all content on one page)

| Section | Title | Core Concepts |
|---------|-------|---------------|
| 64.1 | The Messages API — Anatomy of a Request and Response | API structure, request/response format, message roles |
| 64.2 | Tool Definitions and Tool Use | Tool schema definition, tool_use blocks, tool_result |
| 64.3 | The Agentic Loop | Iterative tool-calling loop, stop conditions, convergence |
| 64.4 | tool_choice — Controlling Tool Selection | auto/any/tool modes, forced tool selection |
| 64.5 | Structured Output via tool_use with JSON Schemas | Schema-driven extraction, type-safe outputs |
| 64.6 | Validation-Retry Loops for Extraction Quality | Output validation, retry strategies, quality assurance |
| 64.7 | The Message Batches API | Batch processing, async batch jobs, cost optimization |
