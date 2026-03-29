# Context Bridge — Snapshots Directory

> **Purpose**: Frozen point-in-time checkpoint states for use by the Rewind command
> **Written by**: Stage 3 of Checkpoint workflow (sub-step after bridge update)
> **Read by**: Rewind protocol ONLY — never loaded as session context
> **Rule**: Read-only after creation. Never modified or deleted.

---

## Why Snapshots Exist

The `master-cumulative.md` bridge is an **append-only, forward-only** document. It is never rolled back. This design prevents cross-lesson data loss during Rewind (e.g., rewinding lesson 2.1 checkpoint would otherwise destroy lesson 3.1 progress).

Instead, each checkpoint writes a frozen snapshot here. Rewind reads from snapshots to restore teaching context — the master bridge remains untouched.

## File Naming

```
lesson-{X.Y}-L{N}-{semantic-concept}-snapshot.md
```

**Examples**:
- `lesson-2.1-L1-structured-text-and-intent-layer-snapshot.md`
- `lesson-3.1-L2-hook-architecture-snapshot.md`
- `lesson-3.17-L3-orchestration-patterns-snapshot.md`

## Content Per Snapshot

Each snapshot contains verbatim copies of these bridge sections at the moment that checkpoint completed:

| Section | Purpose |
|---------|---------|
| Section 6 — Knowledge Graph | Concepts mastered up to this point |
| Section 7 — Vocabulary Bank | Terms known up to this point |
| Section 14 — Checkpoint History | Full history table at that moment |
| Section 15 — Current Checkpoint State | Active layer, last timestamp |

Plus a header identifying the snapshot:
```markdown
# Snapshot: Lesson {X.Y} Layer L{N}
> **Frozen at**: {ISO8601 timestamp}
> **Semantic concept**: {kebab-case-name}
> **Purpose**: Read-only. Used by Rewind. Do not modify.
> **Master bridge row**: L{N} | {timestamp} | ✓ Archived
```

## How Rewind Uses Snapshots

1. User types `Rewind`
2. Rewind protocol lists all snapshots for the current lesson
3. User selects a layer (e.g., L1)
4. Protocol reads `lesson-{X.Y}-L1-*-snapshot.md`
5. Context is restored from snapshot — knowledge graph, vocab, state all reflect that exact moment
6. **Master bridge is NOT modified** — teaching continues forward from restored state

## Legacy Checkpoints

Checkpoints created before this snapshot system was introduced will not have snapshot files. If Rewind selects a legacy checkpoint layer, the protocol falls back to metadata reconstruction and warns the user accordingly.

## Important Rules

- **Never edit** snapshot files after creation
- **Never delete** snapshot files (they are permanent historical records)
- **Never load** snapshots as session context (only `master-cumulative.md` is loaded at session start)
- Snapshots are **not** backups of the bridge — they are selective frozen state extracts
