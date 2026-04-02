# Unity Build Skills for Claude Code

![Claude Skill](https://img.shields.io/badge/Claude-Skill-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automate the 16+ fixes Unity Android exports need before they'll build for Google Play.

* `new Play build at Play/myapp/` — trigger phrase, fresh export to signed AAB
* 6 parallel subagents fix files end-to-end, orchestrator verifies and builds
* 16KB page alignment, API 35 compliance, IL2CPP compilation, dependency conflict resolution
* Up to 4 build retries with automatic error diagnosis from the knowledge base
* New issues auto-documented to `references/knowledge.md` for future builds

## Table of Contents

- [Getting Started](#getting-started)
- [Available Skills](#available-skills)
- [What Gets Fixed](#what-gets-fixed)
- [Build Workflow](#build-workflow)
- [Build Logs](#build-logs)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

Requires [Claude Code](https://claude.ai/code), Android Studio with SDK 35+, NDK 27.0.12077973, and Java 17+.

```bash
git clone https://github.com/creational-ai/unity-builds.git
cd unity-builds
```

Copy your Unity Android Studio export into the `Play/` directory:

```bash
cp -r /path/to/unity-export Play/myapp-v1.0/
```

Open Claude Code and trigger the skill:

```
new Play build at Play/myapp-v1.0/
```

The skill reads the knowledge base, dispatches 6 parallel subagents to fix all files, builds the AAB, and plays a sound when done. First-attempt builds typically complete in ~4-5 minutes.

## Available Skills

| Skill | Trigger | Status |
|-------|---------|--------|
| **Play Store** | `new Play build at Play/<folder>/` | Ready |
| **Amazon Appstore** | `new Amazon build at Amazon/<folder>/` | Coming Soon |
| **iOS App Store** | TBD | Planned |

## What Gets Fixed

| Category | Fixes |
|----------|-------|
| **Project Setup** | NDK path cleanup, `buildToolsVersion` removal, AGP 8.11+ |
| **Java & Build** | Java 17 via Android Studio JBR, `buildConfig` per-module |
| **Dependencies** | Kotlin/OkHttp JAR excludes, Play Core split migration, Install Referrer 2.2, mediation SDK dedup |
| **Manifests** | AD_ID permission, Firebase `tools:replace`, AndroidX migration, `provider_paths.xml`, `hardwareAccelerated` conflict |
| **Packaging** | `noCompress` pattern fix, MultiDex, `useLegacyPackaging true` |
| **Play Compliance** | 16KB ELF alignment, edge-to-edge opt-out, signing config |
| **IL2CPP** | Detects missing `BuildIl2Cpp` task and adds it when `Il2CppOutputProject/` exists |

Full details in `.claude/skills/unity-play-build/references/knowledge.md`.

## Build Workflow

```
Step 1  Read knowledge base
Step 2  Fix phase (parallel)
        ├── 6 background subagents fix files end-to-end
        └── Orchestrator creates new files (provider_paths, edge-to-edge, 16KB gradle)
Step 3  Verify subagent work (spot-check critical changes as each completes)
Step 4  Build AAB (./gradlew clean && ./gradlew bundleRelease)
Step 5  Iterate on failures (up to 4 attempts, consults knowledge base)
Step 6  Log timestamps to Play/logs/ and report summary
Step 7  Sound notification + "Build Complete"
```

Example output:

```
Build: hex2.0.0
AAB: 79MB
Attempts: 1/4

Configure: 2m 19s
Build: 2m 12s
Total: 4m 31s
```

## Build Logs

Each build writes timestamps to `Play/logs/<build-name>.log`:

```
Build: hex2.0.0
Started: 2026-04-01 23:12:28 PDT
Configured: 2026-04-01 23:14:47 PDT  (2m 19s)
Build Attempt 1: 2026-04-01 23:16:59 PDT — SUCCESS  (2m 12s)
Completed: 2026-04-01 23:16:59 PDT

Configure: 2m 19s
Build: 2m 12s
Total: 4m 31s
AAB: 79MB
```

## Project Structure

```
unity-builds/
├── .claude/
│   └── skills/
│       └── unity-play-build/           # Play Store skill
│           ├── SKILL.md                # Workflow definition
│           └── references/
│               ├── knowledge.md        # All fixes & solutions
│               ├── 16kb-research.md    # 16KB compliance research
│               └── edge-to-edge.md     # Android 15 edge-to-edge
├── scripts/
│   └── fix_elf_alignment.py            # 16KB ELF alignment tool
├── Play/                               # Unity exports (gitignored)
│   └── logs/                           # Build logs
├── CLAUDE.md
└── README.md
```

## Contributing

### Adding a new build fix

The skill auto-documents new issues it encounters. To add one manually, append to `references/knowledge.md`:

```markdown
### [N.N] Issue Name
**Problem**: What happens
**Error Message**: Exact error text
**File(s) Fixed**: Which files
**Solution**: Code/config fix
**Why This Happens**: Root cause
```

### Adding a new platform

1. Create `.claude/skills/unity-<platform>-build/`
2. Add `SKILL.md` with trigger and workflow
3. Add `references/` with platform-specific knowledge

## License

MIT
