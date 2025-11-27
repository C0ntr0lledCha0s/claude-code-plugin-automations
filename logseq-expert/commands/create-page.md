---
description: Create a new page in Logseq with optional properties and content
argument-hint: <page-title>
allowed-tools: Read, Bash
---

# Create Logseq Page

Create a new page in your Logseq graph.

## Arguments

- `$ARGUMENTS` - The page title (required)

## Usage

Create a page titled "$ARGUMENTS" in Logseq.

## How to create:

Use the Logseq HTTP API:

```python
import json
import urllib.request
import os

def create_page(title, properties=None, content=None):
    token = os.environ.get("LOGSEQ_API_TOKEN", "")
    url = os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315")

    # Check if page exists
    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.Editor.getPage", "args": [title]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        existing = json.loads(resp.read())["result"]

    if existing:
        return {"error": f"Page already exists: {title}", "page": existing}

    # Create page
    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({
            "method": "logseq.Editor.createPage",
            "args": [title, properties or {}, {"createFirstBlock": True}]
        }).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        page = json.loads(resp.read())["result"]

    # Add content if provided
    if content and page:
        req = urllib.request.Request(
            f"{url}/api",
            data=json.dumps({"method": "logseq.Editor.getPageBlocksTree", "args": [title]}).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(req) as resp:
            blocks = json.loads(resp.read())["result"]

        if blocks:
            req = urllib.request.Request(
                f"{url}/api",
                data=json.dumps({
                    "method": "logseq.Editor.updateBlock",
                    "args": [blocks[0]["uuid"], content]
                }).encode(),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
            )
            urllib.request.urlopen(req)

    return {"success": True, "page": page}

# Create the page
result = create_page("$ARGUMENTS")
print(json.dumps(result, indent=2))
```

## Examples:

- `/logseq-expert:create-page Meeting Notes` - Create basic page
- `/logseq-expert:create-page Project/Alpha` - Create namespaced page
- `/logseq-expert:create-page Books/The Pragmatic Programmer` - Create in namespace

## After creation:

The page is created with an empty first block. You can then use:
- `/logseq-expert:add-block` to add content
- `/logseq-expert:get-page` to verify creation
