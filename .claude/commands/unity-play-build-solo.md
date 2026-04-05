---
description: Build Unity Android export for Play Store (sequential, main agent)
argument-hint: <folder-path>
disable-model-invocation: true
---

# /unity-play-build-solo

Build a Unity Android export for Google Play Store using the sequential (main agent) approach.

## Resources

**Read these for guidance**:
- `.claude/skills/unity-play-build/SKILL.md` — Skill overview, logging, reporting, success criteria
- `.claude/skills/unity-play-build/references/mainagent-guide.md` — Follow this guide exactly

## Input

**Folder path (required):** `$ARGUMENTS`

Example: `/unity-play-build-solo Play/hex2.0.0/`

## Process

Follow `mainagent-guide.md` exactly. It contains the full sequential workflow: read knowledge, assess and fix each file, create new files, check IL2CPP, verify, build, iterate.
