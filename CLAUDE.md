# CLAUDE.md

This file provides guidance to Claude Code when working with Unity cross-platform export projects.

## Overview

This repository provides **Claude Code Skills** that automate fixing and building Unity Android Studio exports for app store submission. Drop in your Unity export, trigger the skill, and get a store-ready build.

## Available Skills

### Play Store Skill ✅
**Trigger:** `new Play build at Play/<folder>/`

Transforms Unity Android exports into Google Play Store ready AAB builds:
- Applies 26 systematic fixes automatically
- Handles API 35 compliance, NDK configuration, 16KB alignment
- Builds AAB format for Google Play submission
- Two execution modes: sequential (`/unity-play-build-solo`) or parallel (`/unity-play-build-parallel`)
- Iterates up to 4 times on build failures
- Documents any new issues discovered

### Amazon Skill 🚧 (Coming Soon)
**Trigger:** `new Amazon build at Amazon/<folder>/`

Will transform Unity Android exports for Amazon Appstore:
- Google Play Services removal
- Amazon Fire device compatibility
- RevenueCat Amazon IAP integration

### iOS Skill 🎯 (Planned)
Future support for Apple App Store builds.

## Project Structure

```
Unity Builds/
├── .claude/
│   ├── commands/
│   │   ├── unity-play-build-solo.md      # Sequential build command
│   │   └── unity-play-build-parallel.md  # Parallel build command
│   └── skills/
│       └── unity-play-build/        # Play Store skill
│           ├── SKILL.md             # Skill definition
│           └── references/          # Knowledge base
│               ├── knowledge.md          # All fixes & solutions
│               ├── mainagent-guide.md    # Sequential build guide
│               ├── subagent-guide.md     # Parallel build guide
│               ├── 16kb-research.md      # 16KB compliance
│               └── edge-to-edge.md       # Android 15 requirements
├── scripts/
│   └── fix_elf_alignment.py         # 16KB ELF alignment tool
├── Play/
│   └── docs/                        # Google Play documentation (detailed)
├── Amazon/
│   └── docs/                        # Amazon Appstore documentation
└── iOS/
    └── docs/                        # iOS documentation (upcoming)
```

## Usage

### 1. Export from Unity
Export your Unity project as an Android Studio project.

### 2. Place in Platform Directory
```bash
# For Google Play
cp -r /path/to/unity-export Play/myapp-v1.0/

# For Amazon (when skill is ready)
cp -r /path/to/unity-export Amazon/myapp-v1.0/
```

### 3. Trigger the Skill
Tell Claude Code:
```
new Play build at Play/myapp-v1.0/
```

### 4. Wait for Build
The skill will:
1. Read the knowledge base
2. Analyze your export
3. Apply all fixes systematically
4. Build the AAB/APK
5. Iterate on failures (up to 4 attempts)
6. Play a sound when complete

## Platform Requirements

### Google Play Store
- **API Level:** 35+ (Google Play 2024+ requirement)
- **NDK:** 27.0.12077973
- **Java:** 17+
- **16KB Alignment:** Required for Android 15+ devices (Nov 2025)

### Amazon Appstore
- **API Level:** 35+
- **Architecture:** 32-bit only for Amazon IAP v2
- **No Google Services:** Complete removal required
- **DRM:** Amazon authentication key

## How Skills Work

Skills are Claude Code's way of encoding domain expertise. Each skill contains:

1. **SKILL.md** - Workflow definition and trigger
2. **references/** - Knowledge base with all fixes and solutions

When triggered, Claude Code:
- Reads the skill definition
- Consults the knowledge base
- Applies fixes systematically
- Builds and iterates on failures
- Documents new issues discovered

## Contributing

Found a new build issue? The skill will automatically document it in the knowledge base following this format:

```markdown
### [N.N] [Issue Name]
**Problem**: [What happens]
**Error Message**: [Exact error]
**File(s) Fixed**: [Which files]
**Solution**: [Code/config fix]
**Why This Happens**: [Root cause]
```

## Success Criteria

A successful build meets:
- ✅ AAB/APK generated
- ✅ API 35 compliant
- ✅ 16KB page size compliant
- ✅ All new issues documented
