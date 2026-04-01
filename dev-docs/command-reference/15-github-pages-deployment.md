# 15 — GitHub Pages Deployment

Auto-publish visual presentations, notes, and cheatsheets to a live website via GitHub Actions.

**When it triggers**: Every time you run `Finish` in chat (which creates a git tag `lesson-{X.Y}`), the GitHub Actions workflow automatically deploys the new content to your GitHub Pages site.

---

## Quick Start (3 steps)

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**, select: **GitHub Actions** (NOT "Deploy from a branch")
4. Click **Save**

### Step 2: Push your code

```bash
git add .
git commit -m "Add checkpoint system with GitHub Pages deployment"
git push origin main
```

### Step 3: Wait for deployment

1. Go to **Actions** tab in your repository
2. Watch the "Publish to GitHub Pages" workflow run
3. When complete, your site is live at:
   ```
   https://<username>.github.io/<repository-name>/
   ```

---

## What Gets Published

| Content | Source in repo | Destination on site |
|---------|---------------|---------------------|
| Visual presentations | `visual-presentations/*.html` | `/presentations/` |
| Concept map | `visual-presentations/concept-map.html` | `/concept-map.html` |
| Checkpoint notes | `revision-notes/**/*.md` | `/notes/**/*.html` (auto-converted) |
| Quick reference | `quick-reference/*.md` | `/quick-ref/*.html` (auto-converted) |
| Landing page | Auto-generated | `/index.html` |

---

## Site Structure

```
https://username.github.io/agent-factory-part-1/
├── index.html                    # Landing page
├── concept-map.html              # Interactive knowledge graph
├── presentations/
│   ├── index.html               # Presentations directory
│   ├── session-01-lesson-3.1-origin-story.html
│   └── session-01-lesson-3.1-L1-presentation.html
├── notes/
│   └── ch3-general-agents/
│       └── 3.1-origin-story/
│           ├── 3.1-L1-hook-architecture.html
│           └── 3.1-L2-custom-hooks.html
└── quick-ref/
    └── lesson-3.1-cheatsheet.html
```

---

## How It Connects to the Finish Workflow

```
You type "Finish" in chat
    │
    ▼
Finish protocol generates all 6 tiers
(HTML, flashcards, cheatsheet, etc.)
    │
    ▼
git-auto-push.py runs automatically (Stage 9)
    │
    ├─ Commits all lesson artifacts
    └─ Creates tag: lesson-{X.Y}
    │
    ▼
GitHub Actions workflow triggers on tag push
    │
    ▼
Workflow:
  1. Checkout code
  2. Install Node.js + Pandoc
  3. Copy presentations as-is
  4. Convert .md notes → HTML with Pandoc
  5. Generate index pages
  6. Upload as GitHub Pages artifact
  7. Deploy to live site
    │
    ▼
Site live at: https://username.github.io/repo-name/
```

---

## Workflow Trigger Conditions

The workflow (`publish-pages.yml`) runs automatically when:

1. **Push to main branch** with changes in:
   - `visual-presentations/`
   - `revision-notes/`
   - `quick-reference/`
   - `context-bridge/`
   - The workflow file itself

2. **Push a tag** matching `lesson-*` or `chapter-*-complete`

3. **Manual trigger**: Actions tab → "Publish to GitHub Pages" → "Run workflow"

---

## Customization

### Change the deployment branch

Edit `.github/workflows/publish-pages.yml`:

```yaml
on:
  push:
    branches:
      - main  # Change to your branch
```

### Add a custom domain

1. Settings → Pages → Custom domain → Enter your domain
2. Add DNS CNAME record pointing to `<username>.github.io`
3. Wait up to 24 hours for DNS propagation
4. Enable "Enforce HTTPS"

### Force re-deploy manually

```bash
git commit --allow-empty -m "Trigger deployment"
git push
```

---

## Required Permissions

The workflow automatically has these permissions:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

---

## Pre-Deployment Checklist

- [ ] Repository is public (or GitHub Pro for private Pages)
- [ ] Workflow file exists: `.github/workflows/publish-pages.yml`
- [ ] GitHub Pages enabled: Settings → Pages → Source: **GitHub Actions**
- [ ] At least one `Finish` has been run (creates HTML + flashcards)
- [ ] Pushed to main branch
- [ ] Workflow completed successfully in Actions tab
- [ ] Site accessible at `https://<username>.github.io/<repo>/`

---

## Monitoring Deployment

1. **Actions Tab**: All workflow runs with status
2. **Environments**: Settings → Environments → github-pages (deployment history)
3. **GitHub Traffic**: Insights → Traffic (14-day visitor history)

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Workflow fails | Missing Pandoc / malformed markdown | Check Actions tab logs; test locally: `pandoc file.md --to html5 -o test.html` |
| 404 page not found | Pages source not set to GitHub Actions | Settings → Pages → Source → GitHub Actions |
| Styles missing | Self-contained HTML generation | Already handled by `--self-contained` flag in workflow |
| Large repository warning | >1GB soft limit | Add to `.gitignore`: `*.mp4`, `*.zip`, `exports/` |
| Site not updating | Deployment didn't trigger | Manual trigger: Actions → Run workflow |

---

## Integration with Git Tagging

The deployment is tied to the `Finish` command's auto-tagging:

- `Finish` → `git-auto-push.py` → creates tag `lesson-3.1`
- Tag push → GitHub Actions detects `lesson-*` tag → deploys

To manually trigger deployment for an existing tag:

```bash
git tag -d lesson-3.1                      # Delete locally
git push origin :refs/tags/lesson-3.1     # Delete remotely
git tag lesson-3.1                         # Re-create
git push origin lesson-3.1               # Push tag → triggers deploy
```

---

## Next Steps After Deployment

1. **Share the link** with your study group or mentors
2. **Add a badge** to your README:
   ```markdown
   [![Deploy](https://github.com/<user>/<repo>/actions/workflows/publish-pages.yml/badge.svg)](https://github.com/<user>/<repo>/actions/workflows/publish-pages.yml)
   ```
3. **Enable discussions**: Settings → General → Features → Discussions
4. **Track visitors**: Insights → Traffic

---

## Related

- `11-git-integration-commands.md` — full git auto-push and tagging reference
- `03-finish-end-command.md` — the Finish command that triggers deployment
