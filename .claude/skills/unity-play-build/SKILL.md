# Unity Play Build Skill

Transform Unity Android Studio exports into Google Play Store ready AAB builds through systematic analysis and iterative problem-solving.

## Trigger

**"new Play build at `<folder>`"** — where `<folder>` is the Unity export folder path (e.g., `Play/ss1.0.3/`)

**Paths:**
- `<project_root>` = Repository root (current working directory)
- `<folder>` = Unity export folder (e.g., `Play/ss1.0.3/`)

## Contents

| File | Purpose |
|------|---------|
| `references/export-knowledge.md` | **Single source of truth** — all fixes, error patterns, solutions |
| `references/edge-to-edge.md` | Android 15 edge-to-edge enforcement details |
| `references/16kb-research.md` | Google Play 16KB page size compliance research |
| `<project_root>/scripts/fix_elf_alignment.py` | Python script for ELF 16KB alignment |

---

## Workflow

### 1. Read Knowledge
Read `references/export-knowledge.md` thoroughly before making any changes. This document contains:
- All known fixes organized by category
- Error messages and their solutions
- Code snippets and configurations

### 2. Analyze
Examine the Unity export folder structure:
- Verify `launcher/`, `unityLibrary/` modules exist
- Check `build.gradle` files for current configuration
- Identify Unity version and SDK versions

### 3. Fix
Apply **ALL** fixes from `references/export-knowledge.md` systematically:
- Work through each section in order
- Apply every relevant fix to the project
- Copy 16KB script to Unity export folder:
  ```
  cp "<project_root>/scripts/fix_elf_alignment.py" "<folder>/"
  ```
- Add Gradle automation for 16KB compliance

### 4. Build
Build **AAB only** (do NOT build APK):

    ./gradlew clean
    ./gradlew bundleRelease

### 5. Iterate (Up to 4 Attempts)

For each build failure:
1. **Analyze** — Read full build error output
2. **Consult** — Search `references/export-knowledge.md` for matching error patterns
3. **Fix** — Apply the documented solution
4. **Rebuild** — Try again
5. **Track** — Log attempt and outcome

### 6. Verify
Confirm build success and Google Play readiness.

### 7. Notify
When build completes, play sound notification twice:

**Success** (AAB generated):

    afplay /System/Library/Sounds/Hero.aiff && afplay /System/Library/Sounds/Hero.aiff

**Failure** (after 4 attempts):

    afplay /System/Library/Sounds/Basso.aiff && afplay /System/Library/Sounds/Basso.aiff

---

## NEW ISSUE REPORTING Protocol

When encountering an issue NOT in the knowledge base:

### 1. Document
Add to `references/export-knowledge.md` following the existing format:

    ### [N.N] [Issue Name]
    **Problem**: [What happens]
    
    **Error Message**:
    [Exact error text]
    
    **File(s) Fixed**: [Which files need modification]
    
    **Solution**:
    [Code/configuration fix]
    
    **Why This Happens**: [Root cause explanation]

### 2. Categorize
Place in the appropriate section (see Table of Contents in knowledge file):
- Section 1: Project Setup & Requirements
- Section 2: Java & Build Configuration
- Section 3: Dependencies & Libraries
- Section 4: Android Manifest & Permissions
- Section 5: Build Optimization & Packaging
- Section 6: Google Play Compliance

### 3. Report
Inform user:

    📝 NEW ISSUE DOCUMENTED
    
    **Issue**: [Brief description]
    **Severity**: [Critical/High/Medium/Low]
    **Solution**: [Brief solution]
    **Added to**: references/export-knowledge.md Section [N]

---

## Success Criteria

    ✅ AAB generated (~111MB typical)
    ✅ API 35 compliant
    ✅ 16KB page size compliant
    ✅ All new issues documented in knowledge file

---

## Build Attempt Tracking

    Build Attempt 1: [Status] - [Error/Success] - [Fix Applied]
    Build Attempt 2: [Status] - [Error/Success] - [Fix Applied]
    Build Attempt 3: [Status] - [Error/Success] - [Fix Applied]
    Build Attempt 4: [Status] - [Error/Success] - [Fix Applied]

---

## Communication Style

- Be concise and action-oriented
- Report progress systematically
- Use checkmarks for completed fixes
- Provide final build summary with file sizes
- Don't ask permission for standard fixes
- Document any new issues to the knowledge file
