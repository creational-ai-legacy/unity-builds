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
| `references/knowledge.md` | **Single source of truth** — all fixes, error patterns, solutions |
| `references/edge-to-edge.md` | Android 15 edge-to-edge enforcement details |
| `references/16kb-research.md` | Google Play 16KB page size compliance research |
| `<project_root>/scripts/fix_elf_alignment.py` | Python script for ELF 16KB alignment |

---

## Workflow

### 1. Read Knowledge & Start Timer
Read `references/knowledge.md` thoroughly before making any changes. This document contains:
- All known fixes organized by category
- Error messages and their solutions
- Code snippets and configurations

**Timestamp "Started"** — write the log file immediately:
```bash
mkdir -p Play/logs
echo "Build: <build-name>" > Play/logs/<build-name>.log
echo "Started: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> Play/logs/<build-name>.log
```

### 2. Fix Phase (Parallel)
In a **single message**, launch subagents first (they're the slow part), then create new files:

**Launch 6 background subagents** (`run_in_background: true`). Each subagent **owns its file(s) end-to-end** — it reads, assesses, AND applies all fixes. No file is touched by more than one subagent.

| Subagent | File(s) to Fix | Knowledge Sections |
|----------|---------------|-------------------|
| A | `gradle.properties`, `local.properties` | 1.2 NDK, 2.1 Java |
| B | `settings.gradle` | 4.7 flatDir (dependencyResolutionManagement) |
| C | `unityLibrary/build.gradle` | 1.1-1.3, 2.1-2.2, 3.1-3.5, 5.1 |
| D | `launcher/build.gradle` | 2.1-2.2, 4.7, 5.1-5.2, 6.1-6.2 |
| E | `unityLibrary/src/main/AndroidManifest.xml` | 4.1, 4.3-4.5 |
| F | `launcher/src/main/AndroidManifest.xml` | 4.2, 4.6 |

**Each subagent prompt must include:**
1. The full file path(s) to fix
2. The relevant sections from `references/knowledge.md` (paste the actual content)
3. Instructions: "Read the file. Compare against the knowledge sections. Apply all needed fixes using the Edit tool. Report what you changed."

**Subagent guardrails:**
- Use **Edit tool only** for existing files — never rewrite a file from scratch
- **NEVER** drop Unity-generated code (`BuildIl2Cpp`, `getSdkDir`, `BuildIl2CppTask`, etc.)
- If code is already correct, leave it alone
- Report a summary of changes made when done

**Orchestrator creates new files** (in the same message, no assessment needed):
- **Copy** `fix_elf_alignment.py` from `<project_root>/scripts/` to `<folder>/`
- **Create** `<folder>/fix_16kb_alignment.gradle` — 16KB alignment Gradle task (see knowledge 6.1)
- **Create** `<folder>/unityLibrary/src/main/res/xml/provider_paths.xml` (see knowledge 4.5)
- **Create** `<folder>/unityLibrary/src/main/res/values-v35/styles.xml` — edge-to-edge opt-out

### 3. Verify Subagent Work
As each subagent completes, **spot-check its work** — read key lines to confirm critical changes landed. Don't re-assess the whole file; just verify the most important items:

| Subagent | What to Spot-Check |
|----------|--------------------|
| A | `org.gradle.java.home` present, `ndk.dir` present |
| B | `dependencyResolutionManagement` removed |
| C | `VERSION_17`, `installreferrer:2.2`, `BuildIl2CppTask` exists, `buildConfig = false` |
| D | `apply from: '../fix_16kb_alignment.gradle'`, `VERSION_17`, `multiDexEnabled true` |
| E | `androidx.multidex.MultiDexApplication`, `removeAll` no xmlns |
| F | Activity declaration present, `tools:replace="android:hardwareAccelerated"` |

If a subagent missed something, fix it immediately. Don't wait for all subagents to verify — verify as they arrive.

### 4. Build (After All Verified)
**Timestamp "Configured"** — append to log immediately:
```bash
echo "Configured: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> Play/logs/<build-name>.log
```

Once all 6 subagents have completed and been verified, build **AAB only** (do NOT build APK):

    ./gradlew clean
    ./gradlew bundleRelease

### 5. Iterate (Up to 4 Attempts)

For each build failure:
1. **Analyze** — Read full build error output
2. **Consult** — Search `references/knowledge.md` for matching error patterns
3. **Fix** — Apply the documented solution
4. **Rebuild** — Try again
5. **Track** — Log attempt and outcome

### 6. Log & Report
**Append completion to log** — build result and durations are calculated from timestamps already in the file:
```bash
echo "Build Attempt N: $(date '+%Y-%m-%d %H:%M:%S %Z') — SUCCESS/FAILED" >> Play/logs/<build-name>.log
echo "Completed: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> Play/logs/<build-name>.log
```

Then read the log file, calculate durations from the timestamps, and append the summary:
```
Configure: Xm Xs
Build: Xm Xs
Total: Xm Xs
AAB: 79MB
```

For failed attempts, append each attempt with its error summary before the successful one.

**Report to user** — full build summary using the durations from the log:

    Build: <build-name>
    AAB: <size>
    Attempts: <N>/4
    
    ✅ AAB generated
    ✅ API 35 compliant
    ✅ 16KB page size compliant
    
    Configure: Xm Xs
    Build: Xm Xs
    Total: Xm Xs

### 7. Notify
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
    **Added to**: references/knowledge.md Section [N]

---

## Success Criteria

    ✅ AAB generated (~80-110MB typical)
    ✅ API 35 compliant
    ✅ 16KB page size compliant
    ✅ All new issues documented in knowledge file

---

## Build Logs

All build logs are saved to `Play/logs/<build-name>.log` with timestamps and durations.

---

## Communication Style

- Be concise and action-oriented
- Report progress systematically
- Use checkmarks for completed fixes
- Provide final build summary with file sizes
- Don't ask permission for standard fixes
- Document any new issues to the knowledge file
