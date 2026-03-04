# Sync Command Protocol

> **Purpose**: Auto-discover curriculum updates from official website, detect changes, intelligently merge
> **Version**: 1.0
> **Created**: 2026-03-03

---

## Command Trigger

**User types**: `Sync`

**Alternative forms**: `sync`, `Update`, `Refresh curriculum`

---

## Workflow

### STAGE 1: Pre-Flight Check

**Before fetching remote curriculum**:

1. **Check local state**:
   - Read `curriculum-manifest.json` (if exists)
   - Get list of local lessons in `Knowledge_Vault/Curriculum/`
   - Extract last sync timestamp
   - Build local lesson inventory:
     ```json
     {
       "3.1": {
         "title": "Origin Story",
         "path": "Knowledge_Vault/Curriculum/chapter-3-general-agents/3.1-origin-story.md",
         "last_modified": "2026-02-15T10:30:00Z",
         "hash": "abc123..."
       }
     }
     ```

2. **Check connectivity**:
   - Attempt to fetch `https://agentfactory.panaversity.org/docs/General-Agents-Foundations/`
   - If fails → Error: "Cannot connect to curriculum source. Check internet connection."
   - If succeeds → Continue

3. **User confirmation**:
   ```
   🔄 SYNC CURRICULUM

   Source: https://agentfactory.panaversity.org/docs/General-Agents-Foundations/
   Local lessons: {count}
   Last sync: {timestamp or "Never"}

   Proceed with discovery? (yes/no)
   ```

---

### STAGE 2: Discovery

**Execute curriculum crawl**:

1. **Run discovery script**:
   ```bash
   python scripts/sync-curriculum-discover.py
   ```

   **Script behavior**:
   - Crawl official website table of contents
   - Extract lesson list with:
     - Chapter number (1-6)
     - Lesson number (e.g., 3.1, 3.15, 3.17)
     - Lesson title
     - URL
     - Optional: Published date (if available in metadata)
   - Save to `curriculum-manifest.json` (remote snapshot)

2. **Load remote manifest**:
   - Read `curriculum-manifest.json`
   - Parse lesson inventory

---

### STAGE 3: Diff Detection

**Compare local vs remote**:

For each lesson in remote manifest:

1. **NEW**: Lesson exists in remote but NOT in local
   - Mark as `NEW`
   - Priority: High (user may want to study this)

2. **UPDATED**: Lesson exists in both, but content changed
   - **Detection method**:
     - Fetch remote content
     - Compute content hash (SHA-256)
     - Compare to local hash
     - If different → `UPDATED`
   - Priority: Medium (may want to review changes)

3. **UNCHANGED**: Lesson exists in both, content identical
   - Mark as `UNCHANGED`
   - Priority: Low (no action needed)

4. **DEPRECATED** (local only): Lesson exists locally but NOT in remote
   - Mark as `DEPRECATED`
   - Priority: Low (possibly removed from curriculum)
   - **Action**: Archive, don't delete

**Build diff report**:

```markdown
## Curriculum Sync Report
Generated: 2026-03-03 16:45

### Summary
- NEW lessons: 3
- UPDATED lessons: 2
- UNCHANGED lessons: 8
- DEPRECATED lessons: 1

### NEW Lessons
1. **3.25** - Advanced MCP Integration
   - URL: https://agentfactory.panaversity.org/.../advanced-mcp
   - Action: APPEND to Chapter 3

2. **4.8** - Custom Tool Development
   - URL: https://agentfactory.panaversity.org/.../custom-tools
   - Action: APPEND to Chapter 4

3. **5.12** - Multi-Agent Orchestration
   - URL: https://agentfactory.panaversity.org/.../multi-agent
   - Action: APPEND to Chapter 5

### UPDATED Lessons
1. **3.15** - Hooks and Extensibility
   - Local hash: abc123...
   - Remote hash: def456...
   - Changes detected: Content updated
   - Action: REPLACE local with remote

2. **3.22** - CoWork Terminal to Desktop
   - Local hash: ghi789...
   - Remote hash: jkl012...
   - Changes detected: Content updated
   - Action: REPLACE local with remote

### DEPRECATED Lessons
1. **3.5** - Legacy Integration Patterns
   - Status: Removed from official curriculum
   - Action: ARCHIVE to `.deprecated/`
```

---

### STAGE 4: User Review & Strategy Selection

**Present diff report to user**:

```
📊 SYNC REPORT

✨ NEW: 3 lessons
🔄 UPDATED: 2 lessons
✅ UNCHANGED: 8 lessons
⚠️ DEPRECATED: 1 lesson

[Full report shown above]

What would you like to do?

1️⃣ AUTO-SYNC ALL
   - Fetch all NEW lessons
   - Replace all UPDATED lessons
   - Archive all DEPRECATED lessons
   - Zero manual intervention

2️⃣ SELECTIVE SYNC
   - Choose which lessons to sync
   - Preview changes before applying
   - Skip unwanted updates

3️⃣ PREVIEW ONLY
   - Show what would change
   - Don't modify any files
   - Generate sync plan for later

4️⃣ CANCEL
   - Abort sync
   - No changes made

Your choice (1/2/3/4):
```

---

### STAGE 5: Execute Merge

**If user chooses AUTO-SYNC ALL or SELECTIVE SYNC**:

For each lesson to sync:

#### NEW Lessons → APPEND

1. **Fetch content**:
   - Use WebFetch to retrieve lesson from URL
   - Extract markdown content

2. **Save to local**:
   - Determine target path:
     ```
     Knowledge_Vault/Curriculum/chapter-{N}-{name}/{X.Y}-{lesson-slug}.md
     ```
   - Write content to file
   - Add YAML frontmatter:
     ```yaml
     ---
     lesson: "3.25"
     title: "Advanced MCP Integration"
     chapter: 3
     url: "https://agentfactory.panaversity.org/.../advanced-mcp"
     synced: "2026-03-03T16:45:00Z"
     hash: "xyz789..."
     status: "new"
     ---
     ```

3. **Update manifest**:
   - Add entry to `curriculum-manifest.json`
   - Update local inventory

#### UPDATED Lessons → REPLACE

1. **Backup old version**:
   - Copy existing file to `.archive/sync-backups/{lesson}-{timestamp}.md`
   - Preserve old content (recovery option)

2. **Fetch new content**:
   - Use WebFetch to retrieve updated lesson

3. **Replace local**:
   - Overwrite existing file with new content
   - Update YAML frontmatter:
     ```yaml
     synced: "2026-03-03T16:45:00Z"
     hash: "new-hash..."
     previous_hash: "old-hash..."
     status: "updated"
     ```

4. **Update manifest**:
   - Update hash in `curriculum-manifest.json`
   - Record sync timestamp

#### DEPRECATED Lessons → ARCHIVE

1. **Move to archive**:
   - Move file from `Knowledge_Vault/Curriculum/` to `.deprecated/{lesson}/`
   - Preserve content (not deleted)

2. **Update manifest**:
   - Mark as `deprecated` in `curriculum-manifest.json`
   - Keep record (don't remove entry)

---

### STAGE 6: Post-Sync Actions

**After all merge operations complete**:

1. **Update curriculum manifest**:
   - Write final `curriculum-manifest.json` with:
     - All lessons (local + remote)
     - Sync timestamp
     - Hash inventory
     - Deprecation markers

2. **Regenerate discovery systems**:
   - Run `python scripts/generate-index.py` to update `revision-notes/INDEX.md`
   - Run `python scripts/extract-tags.py` to update `search-index/tags-index.json`
   - Run `python scripts/build-search-index.py` to update `search-index/fulltext-index.json`

3. **Generate sync log**:
   - Write detailed log to `logs/sync-{timestamp}.log`:
     ```
     SYNC LOG: 2026-03-03 16:45

     NEW:
     - 3.25: Advanced MCP Integration (fetched, saved)
     - 4.8: Custom Tool Development (fetched, saved)
     - 5.12: Multi-Agent Orchestration (fetched, saved)

     UPDATED:
     - 3.15: Hooks and Extensibility (backed up, replaced)
     - 3.22: CoWork Terminal to Desktop (backed up, replaced)

     DEPRECATED:
     - 3.5: Legacy Integration Patterns (archived)

     Manifest updated: ✓
     Search indexes rebuilt: ✓
     Duration: 45 seconds
     ```

4. **Confirm to user**:
   ```
   ✅ SYNC COMPLETE

   ✨ 3 new lessons added
   🔄 2 lessons updated (backups in .archive/)
   ⚠️ 1 lesson archived (moved to .deprecated/)

   Curriculum manifest updated
   Search indexes rebuilt

   Sync log: logs/sync-2026-03-03-1645.log

   Next steps:
   - Review new lessons: 3.25, 4.8, 5.12
   - Check updated lessons: 3.15, 3.22
   - Study as usual

   Ready to continue?
   ```

---

## Edge Cases & Error Handling

### Case 1: Network Failure Mid-Sync

**Scenario**: Fetch fails after syncing 2/5 lessons

**Handling**:
1. Stop sync immediately
2. Rollback partial changes (delete newly added files)
3. Restore from backups (if any UPDATED lessons were replaced)
4. Report error:
   ```
   ❌ SYNC FAILED

   Network error after 2/5 lessons synced.
   All changes rolled back.

   Retry sync? (yes/no)
   ```

### Case 2: Curriculum Structure Changed

**Scenario**: Remote curriculum reorganized (e.g., Chapter 3 split into 3a and 3b)

**Handling**:
1. Detect structure mismatch
2. Warn user:
   ```
   ⚠️ CURRICULUM STRUCTURE CHANGED

   Remote curriculum has new organization:
   - Chapter 3 (old): General Agents
   - Chapter 3a (new): Claude Code Agents
   - Chapter 3b (new): Custom Agents

   Cannot auto-merge. Manual review required.

   Options:
   1. Preserve old structure (skip sync)
   2. Migrate to new structure (interactive)
   3. Export diff report for manual review
   ```

### Case 3: Hash Collision (Rare)

**Scenario**: Two different files produce same hash

**Handling**:
1. Detect collision (extremely unlikely with SHA-256)
2. Fall back to byte-by-byte comparison
3. If still identical → Mark as UNCHANGED
4. If different → Mark as UPDATED, log warning

### Case 4: Lesson Renumbered

**Scenario**: Lesson 3.15 becomes 3.16 in remote curriculum

**Handling**:
1. Detect title match but number mismatch
2. Prompt user:
   ```
   🔄 LESSON RENUMBERED DETECTED

   Local: 3.15 - Hooks and Extensibility
   Remote: 3.16 - Hooks and Extensibility (same title)

   Likely renumbered. What to do?

   1. Rename local (3.15 → 3.16)
   2. Keep both (treat as separate lessons)
   3. Skip this lesson
   ```

### Case 5: Curriculum URL Changed

**Scenario**: Website moved from `agentfactory.panaversity.org` to `panaversity.org/ai-agents`

**Handling**:
1. Detect 301/302 redirect
2. Update base URL in manifest
3. Retry fetch with new URL
4. Log URL change:
   ```
   🔗 URL CHANGED

   Old: https://agentfactory.panaversity.org/...
   New: https://panaversity.org/ai-agents/...

   Manifest updated with new base URL.
   ```

---

## Selective Sync Workflow

**If user chooses SELECTIVE SYNC**:

1. **Present lesson-by-lesson choices**:
   ```
   SELECT LESSONS TO SYNC

   ✨ NEW LESSONS (3):
   [ ] 3.25 - Advanced MCP Integration
   [ ] 4.8 - Custom Tool Development
   [ ] 5.12 - Multi-Agent Orchestration

   🔄 UPDATED LESSONS (2):
   [ ] 3.15 - Hooks and Extensibility
   [ ] 3.22 - CoWork Terminal to Desktop

   ⚠️ DEPRECATED LESSONS (1):
   [ ] 3.5 - Legacy Integration Patterns (archive?)

   Use AskUserQuestion tool with multiSelect: true
   ```

2. **User selects checkboxes**

3. **Execute only selected lessons**:
   - NEW: Fetch and save
   - UPDATED: Backup and replace
   - DEPRECATED: Archive

4. **Skip unselected lessons**:
   - Log as `skipped` in sync log
   - Don't modify files

---

## Preview-Only Mode

**If user chooses PREVIEW ONLY**:

1. **Generate sync plan**:
   - Create `sync-plan-{timestamp}.md` with:
     - Full diff report
     - Exact file paths that would change
     - Commands to execute manually
     - Estimated sync duration

2. **Save to `logs/`**:
   ```
   📄 Sync plan saved: logs/sync-plan-2026-03-03-1645.md

   Review the plan at your leisure.
   Run `Sync` again to execute.
   ```

3. **No changes made**:
   - Zero files modified
   - Manifest unchanged
   - Safe preview

---

## Curriculum Manifest Schema

**File**: `curriculum-manifest.json`

```json
{
  "version": "1.0",
  "last_sync": "2026-03-03T16:45:00Z",
  "source": {
    "base_url": "https://agentfactory.panaversity.org/docs/General-Agents-Foundations/",
    "toc_url": "https://agentfactory.panaversity.org/docs/General-Agents-Foundations/"
  },
  "lessons": {
    "3.1": {
      "chapter": 3,
      "title": "Origin Story",
      "url": "https://agentfactory.panaversity.org/.../origin-story",
      "local_path": "Knowledge_Vault/Curriculum/chapter-3-general-agents/3.1-origin-story.md",
      "hash": "abc123def456...",
      "synced_at": "2026-02-15T10:30:00Z",
      "status": "synced"
    },
    "3.15": {
      "chapter": 3,
      "title": "Hooks and Extensibility",
      "url": "https://agentfactory.panaversity.org/.../hooks-and-extensibility",
      "local_path": "Knowledge_Vault/Curriculum/chapter-3-general-agents/3.15-hooks-and-extensibility.md",
      "hash": "def456ghi789...",
      "previous_hash": "abc123old...",
      "synced_at": "2026-03-03T16:45:00Z",
      "status": "updated"
    },
    "3.5": {
      "chapter": 3,
      "title": "Legacy Integration Patterns",
      "url": null,
      "local_path": ".deprecated/3.5-legacy-integration-patterns.md",
      "hash": "old789xyz...",
      "deprecated_at": "2026-03-03T16:45:00Z",
      "status": "deprecated"
    }
  },
  "stats": {
    "total_lessons": 42,
    "synced": 40,
    "deprecated": 2,
    "chapters": {
      "1": 6,
      "2": 8,
      "3": 12,
      "4": 7,
      "5": 5,
      "6": 4
    }
  }
}
```

---

## Integration with CLAUDE.md

**Add to CLAUDE.md under "Commands" section**:

```markdown
### Sync Command

**Usage**: `Sync`

**Purpose**: Auto-discover curriculum updates from official website, intelligently merge changes

**Workflow**:
1. Fetch remote curriculum table of contents
2. Detect NEW, UPDATED, DEPRECATED lessons
3. Present diff report
4. User chooses: Auto-sync all / Selective sync / Preview only
5. Execute merge (append NEW, replace UPDATED, archive DEPRECATED)
6. Rebuild search indexes
7. Generate sync log

**Use cases**:
- Check for new lessons released
- Update local curriculum with latest content
- Archive lessons removed from official curriculum
```

---

## Quality Gates

Before finalizing sync:

1. **Completeness Check**:
   - All selected lessons processed?
   - No hanging partial states?

2. **Integrity Check**:
   - Hashes match downloaded content?
   - YAML frontmatter valid?
   - No corrupted files?

3. **Backup Verification**:
   - All UPDATED lessons backed up?
   - Backup files readable?

4. **Manifest Consistency**:
   - All lessons in manifest have corresponding files?
   - All files have manifest entries?

**If any gate fails**:
- Halt sync
- Report error
- Offer rollback

---

## Future Enhancements

**Phase 4+ (Not in current scope)**:

- **Auto-sync on startup**: Check for updates every session start
- **Notification system**: "3 new lessons available!"
- **Conflict resolution UI**: Interactive diff viewer for UPDATED lessons
- **Smart merge**: Preserve user annotations in local files when updating
- **Curriculum versioning**: Track curriculum version (v1.0, v1.1, etc.)
- **Offline mode**: Queue sync operations for later when offline

---

## Summary

**Sync command provides**:
- ✅ Auto-discovery of curriculum changes
- ✅ Intelligent diff detection (NEW/UPDATED/DEPRECATED)
- ✅ User-controlled merge strategies
- ✅ Safe backups before overwriting
- ✅ Archive instead of delete
- ✅ Detailed sync logs
- ✅ Rollback on error
- ✅ Selective sync (user chooses which lessons)

**User experience**:
1. Type `Sync`
2. Review diff report
3. Choose auto/selective/preview
4. Sync completes in ~30-60 seconds
5. Continue studying with latest curriculum

**Zero data loss. User always in control.**

---

**END OF PROTOCOL**
