---
description: Build Unity Android export for Play Store (parallel, 6 subagents)
argument-hint: <folder-path>
disable-model-invocation: true
---

# /unity-play-build-parallel

Build a Unity Android export for Google Play Store using the parallel (6 subagents + orchestrator) approach.

## Resources

**Read these for guidance**:
- `.claude/skills/unity-play-build/SKILL.md` — Skill overview, logging, reporting, success criteria
- `.claude/skills/unity-play-build/references/subagent-guide.md` — Follow this guide exactly

## Input

**Folder path (required):** `$ARGUMENTS`

Example: `/unity-play-build-parallel Play/hex2.0.0/`

## Process

Follow `subagent-guide.md` exactly. It contains the full parallel workflow: spawn 6 subagents, orchestrator creates new files + IL2CPP detection, spot-check subagent work, build, iterate.
