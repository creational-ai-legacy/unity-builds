# Subagent Guide — Parallel Build

5 subagents fix files in parallel while the orchestrator (you) handles settings.gradle, creates new files, and manages IL2CPP detection.

## Process

### 1. Start Timer

```bash
mkdir -p Play/logs
echo "Build: <build-name>" > Play/logs/<build-name>.log
echo "Started: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> Play/logs/<build-name>.log
```

### 2. Fix Phase (6 Parallel Tasks)

There are **6 workers** — 5 subagents and you (the orchestrator). Every worker follows the same pattern:
1. **Read** `references/knowledge.md` (understand what needs fixing)
2. **Read** assigned project file(s) (assess current state)
3. **Apply** fixes

**Message 1**: spawn the 5 subagents (`run_in_background: true`) + start your own reads (knowledge, sources, settings.gradle variant detection). **Message 2**: fix settings.gradle + create your new files once reads complete. Do NOT read project files that belong to subagents.

| # | Worker | File(s) Owned | Knowledge Sections |
|---|--------|--------------|-------------------|
| 1 | Subagent A | `gradle.properties`, `local.properties` | 1.2 NDK, 2.1 Java |
| 2 | Subagent B | `unityLibrary/build.gradle` | 1.1-1.3, 2.1-2.2, 3.1-3.5, 5.1 |
| 3 | Subagent C | `launcher/build.gradle` | 2.1-2.2, 4.8 (flatDir only), 5.1-5.2, 6.1-6.2 |
| 4 | Subagent D | `unityLibrary/src/main/AndroidManifest.xml` | 4.1, 4.3-4.5, 4.10 (duplicate launcher fix) |
| 5 | Subagent E | `launcher/src/main/AndroidManifest.xml` | 4.2, 4.7 |
| 6 | **Orchestrator (you)** | `settings.gradle` + new files + IL2CPP build task if missing + launcher manifest label fix if needed | 4.8 (variant detection), 4.9 (variant detection), 1.4, 4.6, 6.1, edge-to-edge |

### Subagent Prompt Requirements

Each subagent prompt must include:
1. The **absolute path** to their assigned project file(s) (e.g., `<project_root>/<folder>/gradle.properties`)
2. The **absolute path** to `<skill_dir>/references/knowledge.md` and which sections to read (e.g., "Read sections 1.1-1.3, 2.1-2.2, 3.1-3.5, 5.1")
3. Instructions: "Read the knowledge sections. Read your assigned file(s). Compare and apply all needed fixes using the Edit tool. Report what you changed."

### Subagent Guardrails

- Use **Edit tool only** for existing files — never rewrite a file from scratch
- **NEVER** drop Unity-generated code (`BuildIl2Cpp`, `getSdkDir`, `BuildIl2CppTask`, etc.)
- If code is already correct, leave it alone
- Report a summary of changes made when done

### Orchestrator Task (Task 6)

After spawning subagents, you:
1. Read `<skill_dir>/references/knowledge.md` — understand what new files the project needs
2. Read `<project_root>/scripts/fix_elf_alignment.py` — source for the alignment script
3. Read `<skill_dir>/references/edge-to-edge.md` — understand edge-to-edge opt-out requirements
4. **Fix `settings.gradle`** (knowledge 4.8 — variant detection):
   - Grep `<folder>/unityLibrary/build.gradle` for `allprojects`
   - **Variant A** (has `allprojects`): Remove the entire `dependencyResolutionManagement` block from `settings.gradle`
   - **Variant B** (no `allprojects`): Keep `dependencyResolutionManagement` but reconfigure with `PREFER_SETTINGS`, `google()`, `mavenCentral()`, local Firebase Maven repo, and `flatDir` using `${rootDir}/unityLibrary/libs`. Find the Firebase local Maven repo path from the Unity project's `Assets/GeneratedLocalRepo/Firebase/m2repository`
5. **Check for application label conflict** (knowledge 4.9 — variant detection):
   - Grep library module manifests for `android:label` (e.g., `grep -r 'android:label' <folder>/*/src/main/AndroidManifest.xml` excluding launcher)
   - **Variant A** (library declares a label — e.g., PaperPlaneToolsAlert): Add `tools:replace="android:label"` to the `<application>` element in `launcher/src/main/AndroidManifest.xml` (AFTER subagent E finishes)
   - **Variant B** (no library label conflict): No fix needed
6. **Check for missing IL2CPP build task** (knowledge 1.4):
   - Check if `<folder>/unityLibrary/src/main/Il2CppOutputProject/` exists (IL2CPP source present)
   - Grep `<folder>/unityLibrary/build.gradle` for `BuildIl2CppTask`
   - If `Il2CppOutputProject/` exists but `BuildIl2CppTask` is missing, append the `getSdkDir()`, `BuildIl2Cpp()`, and `BuildIl2CppTask` block from knowledge 1.4 to the end of `unityLibrary/build.gradle` (AFTER subagent B finishes)
7. Create the new files based on knowledge:
   - **Copy** `fix_elf_alignment.py` from `<project_root>/scripts/` to `<folder>/`
   - **Create** `<folder>/fix_16kb_alignment.gradle` — 16KB alignment Gradle task (knowledge 6.1)
   - **Create** `<folder>/unityLibrary/src/main/res/xml/provider_paths.xml` (knowledge 4.6)
   - **Create** `<folder>/unityLibrary/src/main/res/values-v35/styles.xml` — edge-to-edge opt-out (inherit splash screen config from `values-v31/styles.xml`)

### 3. Verify Subagent Work

As each subagent completes, **spot-check its work** — read key lines to confirm critical changes landed. Don't re-assess the whole file; just verify the most important items:

| Subagent | What to Spot-Check |
|----------|--------------------|
| A | `org.gradle.java.home` present, `ndk.dir` present |
| B | `VERSION_17`, `installreferrer:2.2`, `buildConfig = false` |
| C | `apply from: '../fix_16kb_alignment.gradle'`, `VERSION_17`, `multiDexEnabled true` |
| D | `removeAll` no xmlns, `AD_ID`, `MessagingUnityPlayerActivity` has `DEFAULT` not `LAUNCHER` |
| E | Activity declaration present, `tools:replace="android:hardwareAccelerated"` |

If a subagent missed something, fix it immediately. Don't wait for all subagents to verify — verify as they arrive.

### 4. Build (After All Verified)

**Timestamp "Configured"**:
```bash
echo "Configured: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> Play/logs/<build-name>.log
```

Once all 5 subagents have completed and been verified, build **AAB only** from `<folder>`:
```bash
cd <folder>
./gradlew clean
./gradlew bundleRelease
```

### 5. Iterate (Up to 4 Attempts)

For each build failure:
1. **Analyze** — Read full build error output
2. **Consult** — Search `<skill_dir>/references/knowledge.md` for matching error patterns
3. **Fix** — Apply the documented solution
4. **Rebuild** — Try again
5. **Track** — Log attempt and outcome

### 6. Log & Report

Follow the logging and reporting format defined in SKILL.md.

### 7. Notify

Follow the notification format defined in SKILL.md.
