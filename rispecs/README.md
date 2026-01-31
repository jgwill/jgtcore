# JGTCore RISE Specifications

> Reverse-engineer → Intent-extract → Specify → Export

This directory contains RISE-compliant specifications for the JGTCore library - the foundational configuration and settings layer for all JGT trading packages.

## Quick Start

1. **Start Here**: [`app.specs.md`](./app.specs.md) - Master specification
2. **Configuration**: [`config.spec.md`](./config.spec.md) - Configuration loading
3. **Settings**: [`settings.spec.md`](./settings.spec.md) - Settings management

## Specification Map

```
app.specs.md                    ← Master specification (start here)
├── config.spec.md              ← Configuration loading and credentials
├── settings.spec.md            ← Settings management and hierarchy
└── environment.spec.md         ← Environment detection and setup
```

## RISE Framework Compliance

Each specification follows these principles:

✅ **Desired Outcome Definition** - What users CREATE, not problems to solve  
✅ **Structural Tension** - Current reality vs desired state drives progression  
✅ **Natural Advancement** - Clear flow from current to desired  
✅ **Autonomous Specification** - Another LLM could implement from spec alone  
✅ **Type Definitions** - Complete Python type hints

## For LLM Implementers

These specifications are designed to be self-contained. You can re-implement the entire JGTCore library using only these specs without accessing the original source code.

## Key Concepts

### Configuration Hierarchy
- System-level `/etc/jgt/`
- User-level `~/.jgt/`
- Process-level (environment variables)
- Custom paths

### Core Modules
- **core.py** - Main configuration and settings access
- **constants.py** - Shared constants across JGT packages
- **env/** - Environment detection utilities
- **fx/** - FX-specific helpers

## Specification Version

- **Version**: 1.0
- **Framework**: RISE
- **Created**: 2026-01-31
