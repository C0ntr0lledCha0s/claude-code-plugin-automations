---
description: Apply label taxonomy preset (standard, comprehensive, or minimal)
allowed-tools: Bash, Read
argument-hint: "[preset-name]"
---

# Sync Label Taxonomy

Apply a predefined label taxonomy to the repository.

## Usage

```bash
/label-sync standard
/label-sync comprehensive
/label-sync minimal
```

## Arguments

- **First argument** (required): Preset name (standard | comprehensive | minimal)

## Presets

**Standard** (10 labels): Types, priorities, basic scopes
**Comprehensive** (28 labels): Full taxonomy with all categories
**Minimal** (6 labels): Essential labels only

## What This Does

1. Loads preset from assets/label-presets.json
2. Creates labels with proper colors and descriptions
3. Updates existing labels if they exist
4. Reports labels created/updated
