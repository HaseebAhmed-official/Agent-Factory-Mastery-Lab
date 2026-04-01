# Chapter 18: Claude Code for Teams, CI/CD & Advanced Configuration (10 Lessons + Quiz)

> **Cross-refs**: [Cross-Chapter Map](../../Frameworks/cross-chapter-map.md) | [Vocabulary](../../Vocabulary/master-glossary.md) | [Exercise Design](../../Pedagogy/exercise-design.md)
> **Site URL**: `/docs/General-Agents-Foundations/claude-code-teams-cicd`
>
> **Overview**: Transforms Claude Code from a solo developer tool into shared engineering infrastructure. Covers team configuration, pipeline automation, and advanced deployment patterns.
> **Certification alignment**: Claude Certified Architect: Foundations (Domains 3 & 4)

| Lesson | Title | Core Concepts | URL |
|--------|-------|---------------|-----|
| 18.1 | The CLAUDE.md Configuration Hierarchy | Three-level configuration (user/project/directory), @import syntax for modular rules, .claude/rules/ directory structure, /memory command for persistent context | `/claude-md-configuration-hierarchy` |
| 18.2 | Path-Specific Rules with Glob Patterns | YAML frontmatter scoping, glob syntax patterns (*.ts, src/**), token efficiency strategies, when path-aware rules beat global rules | `/path-specific-rules-with-glob-patterns` |
| 18.3 | Custom Skills with Frontmatter | `context: fork` attribute, `allowed-tools` restrictions, `argument-hint` attribute for discoverability; skill decision frameworks for team use | `/custom-skills-with-frontmatter` |
| 18.4 | Plan Mode vs Direct Execution | Mode selection criteria (exploratory vs deterministic tasks), Explore subagent integration, when plan mode prevents costly mistakes | `/plan-mode-vs-direct-execution` |
| 18.5 | Iterative Refinement Techniques | Concrete I/O examples in prompts, test-driven iteration loops, interview patterns for requirement extraction, feedback-driven prompt improvement | `/iterative-refinement-techniques` |
| 18.6 | Claude Code in CI/CD Pipelines | `-p` flag for non-interactive execution, `--output-format json` for structured output, `--json-schema` for validation, duplicate comment prevention, pipeline integration patterns | `/claude-code-in-cicd-pipelines` |
| 18.7 | Multi-Pass Review Architecture | Overcoming attention limitations through per-file passes, cross-file synthesis passes, staged review workflows for large codebases | `/multi-pass-review-architecture` |
| 18.8 | Session Management: Resume, Fork, and Recovery | Named sessions for continuity, `fork_session` for branching workflows, `/compact` command for context compression, change notification patterns | `/session-management-resume-fork-recovery` |
| 18.9 | Exercises | Hands-on practice: team CLAUDE.md hierarchy, pipeline integration, multi-pass review, session management | `/teams-cicd-exercises` |
| 18.10 | Chapter 18 Quiz | 50-question assessment covering all Chapter 18 concepts | `/chapter-quiz` |
