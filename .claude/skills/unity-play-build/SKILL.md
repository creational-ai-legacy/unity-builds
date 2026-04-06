# unity-play-build

Transform Unity Android Studio exports into Google Play Store ready AAB builds through systematic analysis and iterative problem-solving.

## Philosophy

Every Unity export is different. Unity's Android Resolver generates varying Gradle structures, dependency configurations, and manifest layouts across versions and project settings. Never assume a fixed structure — always **detect and adapt**. The knowledge base documents known variants (e.g., `allprojects` repos vs `dependencyResolutionManagement`, presence or absence of IL2CPP build tasks). When you encounter something new, diagnose it, fix it, and document it.

## Trigger

**"new Play build at `<folder>`"** — where `<folder>` is the Unity export folder path (e.g., `Play/ss1.0.3/`)

**Paths:**
- `<project_root>` = Repository root (current working directory)
- `<skill_dir>` = This skill's base directory (provided in the preamble when the skill loads)
- `<folder>` = Unity export folder (e.g., `Play/ss1.0.3/`)

## Contents

All `references/` paths are relative to `<skill_dir>`:

| File | Purpose |
|------|---------|
| `references/knowledge.md` | **Single source of truth** — all fixes, error patterns, solutions |
| `references/edge-to-edge.md` | Android 15 edge-to-edge enforcement details |
| `references/16kb-research.md` | Google Play 16KB page size compliance research |
| `references/mainagent-guide.md` | Sequential build approach (main agent does everything) |
| `references/subagent-guide.md` | Parallel build approach (5 subagents + orchestrator) |
| `<project_root>/scripts/fix_elf_alignment.py` | Python script for ELF 16KB alignment |

## Execution Modes

| Mode | Guide | Best For |
|------|-------|----------|
| **Sequential** | `references/mainagent-guide.md` | Single-agent, straightforward builds |
| **Parallel** | `references/subagent-guide.md` | Fast builds using 5 subagents + orchestrator |

When triggered directly ("new Play build at ..."), use the **parallel** mode by default. The user can also invoke a specific mode via commands:
- `/unity-play-build-solo <folder>` — sequential
- `/unity-play-build-parallel <folder>` — parallel

Follow the selected guide exactly. Both guides share the same logging, reporting, and notification formats defined below.

---

## Build Log Format

Logs are **one file per version**, append-only. Extract the version from `<folder>` (e.g., `hex2.0.0b128` → version `hex2.0.0`). Log file: `Play/logs/<version>.log`.

Each build appends a new entry separated by `===`. Never overwrite — just append.

```bash
# Start timer (append, don't overwrite)
mkdir -p Play/logs
echo "" >> Play/logs/<version>.log
echo "===" >> Play/logs/<version>.log
echo "Build: <build-name> | Folder: <folder>" >> Play/logs/<version>.log
echo "Started: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> Play/logs/<version>.log
```

```
===
Build: <build-name> | Folder: <folder>
Started: YYYY-MM-DD HH:MM:SS TZ
Configured: YYYY-MM-DD HH:MM:SS TZ
Build Attempt N: YYYY-MM-DD HH:MM:SS TZ — SUCCESS/FAILED (error summary)
Completed: YYYY-MM-DD HH:MM:SS TZ
Configure: Xm Xs | Build: Xm Xs | Total: Xm Xs | AAB: <size>MB
```

## Report to User

```
Build: <build-name>
AAB: <size>
Attempts: <N>/4

Success Criteria:
- AAB generated
- API 35 compliant
- 16KB page size compliant

Configure: Xm Xs
Build: Xm Xs
Total: Xm Xs
```

## Notify

When build completes, play sound notification then say "Build Complete":

**Success** (AAB generated):

    afplay /System/Library/Sounds/Hero.aiff && afplay /System/Library/Sounds/Hero.aiff && say "Build Complete"

**Failure** (after 4 attempts):

    afplay /System/Library/Sounds/Basso.aiff && afplay /System/Library/Sounds/Basso.aiff && say "Build Complete"

---

## NEW ISSUE REPORTING Protocol

When encountering an issue NOT in the knowledge base:

### 1. Document
Add to `references/knowledge.md` following the existing format:

    ### [N.N] [Issue Name]
    **Problem**: [What happens]
    
    **Error Message**:
    [Exact error text]
    
    **File(s) Fixed**: [Which files need modification]
    
    **Solution**:
    [Code/configuration fix]
    
    **Why This Happens**: [Root cause explanation]

### 2. Categorize
Place in the appropriate section:
- Section 1: Project Setup & Requirements
- Section 2: Java & Build Configuration
- Section 3: Dependencies & Libraries
- Section 4: Android Manifest & Permissions
- Section 5: Build Optimization & Packaging
- Section 6: Google Play Compliance

### 3. Report
Inform user of the new issue, severity, solution, and where it was added.

---

## Success Criteria

- AAB generated (~80-110MB typical)
- API 35 compliant
- 16KB page size compliant
- All new issues documented in knowledge file

---

## Communication Style

- Be concise and action-oriented
- Report progress systematically
- Use checkmarks for completed fixes
- Provide final build summary with file sizes
- Don't ask permission for standard fixes
- Document any new issues to the knowledge file
