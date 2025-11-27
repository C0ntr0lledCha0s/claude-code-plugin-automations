---
description: Add a new block to a Logseq page
argument-hint: <page-title> <content>
allowed-tools: Read, Bash
---

# Add Block to Logseq Page

Add a new block to an existing page in your Logseq graph.

## Arguments

- `$1` - The page title
- `$2` (and remaining) - The block content

## Usage

Add content to page "$1".

## How to add:

Use the Logseq HTTP API:

```python
import json
import urllib.request
import os
import sys

def append_to_page(title, content):
    token = os.environ.get("LOGSEQ_API_TOKEN", "")
    url = os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315")

    # Get or create page
    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.Editor.getPage", "args": [title]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        page = json.loads(resp.read())["result"]

    if not page:
        # Create page
        req = urllib.request.Request(
            f"{url}/api",
            data=json.dumps({
                "method": "logseq.Editor.createPage",
                "args": [title, {}, {"createFirstBlock": True}]
            }).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(req) as resp:
            page = json.loads(resp.read())["result"]

    # Get blocks
    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.Editor.getPageBlocksTree", "args": [title]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        blocks = json.loads(resp.read())["result"]

    # Insert after last block
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

    return {"success": True, "block": block}

# Parse arguments
page_title = "$1"
content = "$2"  # Content is everything after the page title

result = append_to_page(page_title, content)
print(json.dumps(result, indent=2))
```

## Examples:

- `/logseq-expert:add-block "Daily Notes" "- New task item"`
- `/logseq-expert:add-block "Meeting Notes" "## Action Items"`
- `/logseq-expert:add-block "Project/Alpha" "TODO Complete review"`

## Content formatting:

Content can include:
- Markdown formatting (`**bold**`, `*italic*`)
- Task markers (`TODO`, `DOING`, `DONE`)
- Page links (`[[Page Name]]`)
- Tags (`#tag`)
- Properties (`property:: value`)
