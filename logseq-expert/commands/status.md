---
description: Check Logseq connection status and environment configuration
allowed-tools: Read, Bash
---

# Logseq Connection Status

Check the current Logseq integration status.

## Run diagnostic checks:

```bash
cd {projectRoot}
bash logseq-expert/scripts/preflight-checks.sh quick
```

For a more thorough check:

```bash
bash logseq-expert/scripts/preflight-checks.sh all
```

## What's checked:

- **Configuration**: `.claude/logseq-expert/env.json` exists and is valid
- **Dependencies**: Python 3 and Node.js available
- **API Token**: LOGSEQ_API_TOKEN environment variable set
- **HTTP API**: Logseq HTTP server reachable
- **Graph**: Current graph accessible

## Test connection directly:

```bash
python3 logseq-expert/scripts/test-connection.py --verbose
```

## Detect available backends:

```bash
python3 logseq-expert/scripts/detect-backend.py --json
```

## Troubleshooting:

If connection fails:
1. Ensure Logseq is running
2. Enable HTTP API: Settings > Features > HTTP APIs server
3. Check your token: Settings > Features > Authorization tokens
4. Verify port 12315 is not blocked
