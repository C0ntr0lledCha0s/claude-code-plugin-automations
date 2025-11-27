---
description: Sync conversation notes to a Logseq page with automatic timestamp
argument-hint: <title>
allowed-tools: Read, Bash
---

# Sync Notes to Logseq

Save conversation notes or summaries to your Logseq graph with automatic timestamps.

## Arguments

- `$ARGUMENTS` - Title for the notes (will be prefixed with "Claude Notes/")

## Usage

Sync notes to "Claude Notes/$ARGUMENTS".

This command is designed for saving Claude conversation summaries, research findings, or any notes you want to preserve in Logseq.

## How it works:

1. Creates or opens "Claude Notes/$ARGUMENTS" page
2. Appends content with timestamp header
3. Adds type and metadata properties

## How to sync:

```python
import json
import urllib.request
import os
from datetime import datetime

def sync_notes(title, notes, page_prefix="Claude Notes"):
    token = os.environ.get("LOGSEQ_API_TOKEN", "")
    url = os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315")
    page_title = f"{page_prefix}/{title}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Get or create page
    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.Editor.getPage", "args": [page_title]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        page = json.loads(resp.read())["result"]

    if not page:
        req = urllib.request.Request(
            f"{url}/api",
            data=json.dumps({
                "method": "logseq.Editor.createPage",
                "args": [page_title, {"type": "Claude Notes", "created": timestamp.split()[0]}, {"createFirstBlock": True}]
            }).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(req) as resp:
            page = json.loads(resp.read())["result"]

    # Format content with timestamp
    content = f"## {timestamp}\\n\\n{notes}\\n\\n---"

    # Get blocks and append
    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.Editor.getPageBlocksTree", "args": [page_title]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        blocks = json.loads(resp.read())["result"]

    if blocks:
        parent_uuid = blocks[-1]["uuid"]
        sibling = True
    else:
        parent_uuid = page["uuid"]
        sibling = False

    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({
            "method": "logseq.Editor.insertBlock",
            "args": [parent_uuid, content, {"sibling": sibling}]
        }).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        block = json.loads(resp.read())["result"]

    return {"success": True, "page": page_title, "block": block}

# Use the command
title = "$ARGUMENTS"
```

After running this command, I will gather the relevant notes from our conversation and sync them to Logseq.

## Examples:

- `/logseq-expert:sync-notes Project Discussion` - Save project notes
- `/logseq-expert:sync-notes Code Review` - Save code review findings
- `/logseq-expert:sync-notes Research/AI Models` - Save with sub-namespace

## What gets synced:

- Key decisions and conclusions
- Action items and next steps
- Important code snippets or references
- Questions and answers from the conversation
