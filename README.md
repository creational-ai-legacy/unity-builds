# Unity Build Skills for Claude Code

Automate Unity Android Studio export fixes with Claude Code Skills. Drop in your Unity export, trigger the skill, get a store-ready build.

## What This Does

Unity's Android Studio exports require **12+ manual fixes** before they'll build for Google Play. This repo encodes all those fixes into a Claude Code Skill that applies them automatically.

**Before:** Hours of Googling error messages and manually editing gradle files
**After:** `new Play build at Play/myapp/` → store-ready AAB in minutes

## Quick Start

### Prerequisites
- [Claude Code](https://claude.ai/code) installed
- Android Studio with SDK/NDK configured
- Unity project exported as Android Studio project

### Usage

1. **Clone this repo**
   ```bash
   git clone https://github.com/creational-ai/unity-builds.git
   cd unity-builds
   ```

2. **Copy your Unity export**
   ```bash
   mkdir -p Play
   cp -r /path/to/unity-export Play/myapp-v1.0/
   ```

3. **Run Claude Code and trigger the skill**
   ```
   new Play build at Play/myapp-v1.0/
   ```

4. **Wait for build** (~2-5 minutes)
   - Skill reads knowledge base
   - Applies all fixes systematically
   - Builds AAB for Google Play
   - Retries up to 4x on failures
   - Plays sound when complete

## Available Skills

| Skill | Trigger | Status |
|-------|---------|--------|
| **Play Store** | `new Play build at Play/<folder>/` | ✅ Ready |
| **Amazon Appstore** | `new Amazon build at Amazon/<folder>/` | 🚧 Coming |
| **iOS App Store** | TBD | 🎯 Planned |

## What Gets Fixed

The Play Store skill handles:

- **NDK Configuration** - Removes hardcoded paths, configures correct version
- **Java 17** - Sets up Android Studio bundled JBR
- **API 35 Compliance** - Required for Google Play 2024+
- **16KB Page Alignment** - Mandatory for Android 15+ (Nov 2025)
- **Dependency Conflicts** - Kotlin, OkHttp, mediation SDK duplicates
- **AndroidManifest** - Package attributes, permissions, Firebase config
- **Build Optimizations** - noCompress patterns, MultiDex, legacy packaging

See `.claude/skills/unity-play-build/references/export-knowledge.md` for the complete list.

## Project Structure

```
unity-builds/
├── .claude/
│   ├── agents/                      # Agent definitions
│   │   ├── unity-play-builder.md
│   │   └── unity-amazon-builder.md
│   └── skills/
│       └── unity-play-build/        # Play Store skill
│           ├── SKILL.md             # Workflow definition
│           └── references/          # Knowledge base
│               ├── export-knowledge.md
│               ├── 16kb-research.md
│               └── edge-to-edge.md
├── scripts/
│   └── fix_elf_alignment.py         # 16KB ELF alignment tool
├── Play/                            # Your Unity exports go here (gitignored)
├── Amazon/                          # Amazon exports (gitignored)
├── iOS/                             # iOS exports (gitignored)
├── CLAUDE.md                        # Claude Code guidance
└── README.md
```

## Requirements

### For Google Play Builds
- Android Studio with SDK 35+
- NDK 27.0.12077973
- Java 17+
- Unity 2022.3.x export

### For Amazon Builds (Coming Soon)
- Same as above, plus Amazon-specific configuration

## How Skills Work

Claude Code Skills encode domain expertise:

1. **SKILL.md** defines the trigger and workflow
2. **references/** contains the knowledge base
3. When triggered, Claude reads the knowledge, applies fixes, builds, and iterates

The skill also **documents new issues** it encounters, growing the knowledge base over time.

## Contributing

### Found a new build error?

The skill auto-documents issues, but you can also add them manually to `references/export-knowledge.md`:

```markdown
### [N.N] Issue Name
**Problem**: What happens
**Error Message**: Exact error text
**File(s) Fixed**: Which files
**Solution**: Code/config fix
**Why This Happens**: Root cause
```

### Want to add a new platform?

1. Create `.claude/skills/unity-<platform>-build/`
2. Add `SKILL.md` with trigger and workflow
3. Add `references/` with platform-specific knowledge
4. Submit PR

## License

MIT - Use freely for your Unity projects.

---

**Built for Unity developers tired of gradle errors.**
