# Main Agent Guide — Sequential Build

The main agent reads the knowledge base, then assesses and fixes each file one at a time.

## Process

### 1. Start Timer

Extract the version from `<folder>` (e.g., `hex2.0.0b128` → `hex2.0.0`). Log file: `Play/logs/<version>.log`. Append, never overwrite.

```bash
mkdir -p Play/logs
echo "" >> Play/logs/<version>.log
echo "===" >> Play/logs/<version>.log
echo "Build: <build-name> | Folder: <folder>" >> Play/logs/<version>.log
echo "Started: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> Play/logs/<version>.log
```

### 2. Read Knowledge

Read the full knowledge base before touching any files:
- `<skill_dir>/references/knowledge.md` — all fixes, error patterns, solutions
- `<skill_dir>/references/edge-to-edge.md` — edge-to-edge opt-out requirements
- `<project_root>/scripts/fix_elf_alignment.py` — source for 16KB alignment script

### 3. Assess & Fix (Sequential)

For each file group below: **read the file, compare against the knowledge sections, apply needed fixes using the Edit tool.** If code is already correct, leave it alone.

**NEVER drop Unity-generated code** (`BuildIl2Cpp`, `getSdkDir`, `BuildIl2CppTask`, etc.)

| # | File(s) | Knowledge Sections |
|---|---------|-------------------|
| 1 | `gradle.properties`, `local.properties` | 1.2 NDK, 2.1 Java |
| 2 | `settings.gradle` | 4.8 (variant detection — check if `allprojects` exists in unityLibrary/build.gradle first) |
| 3 | `unityLibrary/build.gradle` | 1.1-1.4, 2.1-2.2, 3.1-3.5, 5.1 |
| 4 | `launcher/build.gradle` | 2.1-2.2, 4.8 (flatDir), 5.1-5.2, 6.1-6.2 |
| 5 | `unityLibrary/src/main/AndroidManifest.xml` | 4.1, 4.3-4.5, 4.10 (duplicate launcher) |
| 6 | `launcher/src/main/AndroidManifest.xml` | 4.2, 4.7, 4.9 (variant detection — grep library module manifests for `android:label` first) |

### 4. Create New Files

After fixing existing files, create these new files:

- **Copy** `fix_elf_alignment.py` from `<project_root>/scripts/` to `<folder>/`
- **Create** `<folder>/fix_16kb_alignment.gradle` — 16KB alignment Gradle task (knowledge 6.1)
- **Create** `<folder>/unityLibrary/src/main/res/xml/provider_paths.xml` (knowledge 4.6)
- **Create** `<folder>/unityLibrary/src/main/res/values-v35/styles.xml` — edge-to-edge opt-out (inherit splash screen config from `values-v31/styles.xml`)

### 5. Check IL2CPP Build Task (Knowledge 1.4)

This is critical — detect and fix missing IL2CPP compilation:

1. Check if `<folder>/unityLibrary/src/main/Il2CppOutputProject/` exists
2. Grep `<folder>/unityLibrary/build.gradle` for `BuildIl2CppTask`
3. If `Il2CppOutputProject/` exists but `BuildIl2CppTask` is missing:
   - Append the `getSdkDir()`, `BuildIl2Cpp()`, and `BuildIl2CppTask` block from knowledge 1.4 to the end of `unityLibrary/build.gradle`

### 6. Verify

Quick grep checks on critical items before building:

| Check | What to Grep |
|-------|-------------|
| Java home | `org.gradle.java.home` in `gradle.properties` |
| NDK | `ndk.dir` in `local.properties` |
| Settings | Variant A: `dependencyResolutionManagement` NOT in `settings.gradle`. Variant B: `PREFER_SETTINGS` in `settings.gradle` |
| Java 17 | `VERSION_17` in both build.gradle files |
| MultiDex | `multiDexEnabled` in `launcher/build.gradle` |
| 16KB | `fix_16kb_alignment` in `launcher/build.gradle` |
| IL2CPP | `BuildIl2CppTask` in `unityLibrary/build.gradle` (if Il2CppOutputProject exists) |

### 7. Build

**Timestamp "Configured"**:
```bash
echo "Configured: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> Play/logs/<version>.log
```

Build **AAB only** from `<folder>`:
```bash
cd <folder>
./gradlew clean
./gradlew bundleRelease
```

### 8. Iterate (Up to 4 Attempts)

For each build failure:
1. **Analyze** — Read full build error output
2. **Consult** — Search `<skill_dir>/references/knowledge.md` for matching error patterns
3. **Fix** — Apply the documented solution
4. **Rebuild** — Try again
5. **Track** — Log attempt and outcome

### 9. Log & Report

Follow the logging and reporting format defined in SKILL.md.

### 10. Notify

Follow the notification format defined in SKILL.md.
