---
description: Initialize Logseq integration environment with interactive setup wizard
allowed-tools: Read, Bash, Write
---

# Initialize Logseq Environment

Run the interactive setup wizard to configure Logseq integration.

## What this does:

1. Detects your operating system and Logseq installation
2. Locates your Logseq graph directory
3. Helps you configure the HTTP API token
4. Creates the environment configuration file
5. Tests the connection

## Run the initialization:

```bash
cd {projectRoot}
python3 logseq-expert/scripts/init-environment.py
```

If the script succeeds, it will create `.claude/logseq-expert/env.json` with your configuration.

## After initialization:

- Run `/logseq-expert:status` to verify connection
- Use `/logseq-expert:get-page` to test reading data
- Use `/logseq-expert:sync-notes` to test writing data

## Manual configuration:

If automatic detection fails, you can manually create `.claude/logseq-expert/env.json`:

```json
{
  "backend": "http",
  "http": {
    "url": "http://127.0.0.1:12315",
    "token": "your-api-token-here"
  }
}
```

Get your token from: Logseq Settings > Features > Authorization tokens
