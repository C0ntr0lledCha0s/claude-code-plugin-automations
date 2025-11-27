---
description: Search for content across your Logseq graph
argument-hint: <search-query>
allowed-tools: Read, Bash
---

# Search Logseq

Search for content across all pages and blocks in your Logseq graph.

## Arguments

- `$ARGUMENTS` - The search query (required)

## Usage

Search for "$ARGUMENTS" in Logseq.

## How to search:

Use the Logseq HTTP API:

```python
import json
import urllib.request
import os

def search_logseq(query, limit=50):
    token = os.environ.get("LOGSEQ_API_TOKEN", "")
    url = os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315")

    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.App.search", "args": [query]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )

    with urllib.request.urlopen(req) as resp:
        results = json.loads(resp.read())["result"]

    formatted = []
    for r in results[:limit]:
        formatted.append({
            "uuid": r["block"]["uuid"],
            "content": r["block"]["content"],
            "page": r["block"].get("page", {}).get("name", "unknown")
        })

    return {"query": query, "count": len(formatted), "results": formatted}

result = search_logseq("$ARGUMENTS")
print(json.dumps(result, indent=2))
```

## Search tips:

- Use quotes for exact phrases
- Search finds matches in block content
- Results include the page and block UUID for navigation

## Examples:

- `/logseq-expert:search meeting agenda` - Find meeting agendas
- `/logseq-expert:search #project` - Find tagged content
- `/logseq-expert:search TODO` - Find todo items
