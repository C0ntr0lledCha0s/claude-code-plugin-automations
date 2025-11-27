---
description: Get a page from Logseq by title with its content and blocks
argument-hint: <page-title>
allowed-tools: Read, Bash
---

# Get Logseq Page

Retrieve a page from your Logseq graph.

## Arguments

- `$ARGUMENTS` - The page title to retrieve (required)

## Usage

Get the page "$ARGUMENTS" from Logseq.

## How to retrieve:

Use the Logseq HTTP API to get the page:

```python
import json
import urllib.request
import os

def get_page(title):
    token = os.environ.get("LOGSEQ_API_TOKEN", "")
    url = os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315")

    # Get page info
    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.Editor.getPage", "args": [title]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        page = json.loads(resp.read())["result"]

    if not page:
        return {"error": f"Page not found: {title}"}

    # Get page blocks
    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.Editor.getPageBlocksTree", "args": [title]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        blocks = json.loads(resp.read())["result"]

    return {"page": page, "blocks": blocks}

result = get_page("$ARGUMENTS")
print(json.dumps(result, indent=2))
```

## Response includes:

- **page**: Page metadata (uuid, name, properties)
- **blocks**: Hierarchical block tree with content

## Examples:

- `/logseq-expert:get-page Meeting Notes` - Get meeting notes page
- `/logseq-expert:get-page Project/Alpha` - Get namespaced page
- `/logseq-expert:get-page 2024-01-15` - Get journal page by date
