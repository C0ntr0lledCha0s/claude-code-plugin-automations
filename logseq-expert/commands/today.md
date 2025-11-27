---
description: Get today's journal page from Logseq
allowed-tools: Read, Bash
---

# Today's Journal

Get today's journal page from your Logseq graph.

## Usage

Retrieve the current day's journal with all its blocks.

## How to get today's journal:

```python
import json
import urllib.request
import os
from datetime import datetime

def get_today():
    token = os.environ.get("LOGSEQ_API_TOKEN", "")
    url = os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315")

    today = datetime.now()

    # Try common date formats used by Logseq
    formats = [
        today.strftime("%Y-%m-%d"),  # 2024-01-15
        today.strftime("%b %d, %Y"),  # Jan 15, 2024
        today.strftime("%B %d, %Y"),  # January 15, 2024
        today.strftime("%b %dst, %Y") if today.day == 1 else None,
        today.strftime("%b %dnd, %Y") if today.day == 2 else None,
        today.strftime("%b %drd, %Y") if today.day == 3 else None,
        today.strftime("%b %dth, %Y"),
    ]
    formats = [f for f in formats if f]

    for date_format in formats:
        req = urllib.request.Request(
            f"{url}/api",
            data=json.dumps({"method": "logseq.Editor.getPage", "args": [date_format]}).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        )
        try:
            with urllib.request.urlopen(req) as resp:
                page = json.loads(resp.read())["result"]
            if page:
                # Get blocks
                req = urllib.request.Request(
                    f"{url}/api",
                    data=json.dumps({"method": "logseq.Editor.getPageBlocksTree", "args": [page["name"]]}).encode(),
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
                )
                with urllib.request.urlopen(req) as resp:
                    blocks = json.loads(resp.read())["result"]
                return {"date": date_format, "page": page, "blocks": blocks}
        except:
            continue

    return {"error": "Today's journal not found", "tried": formats}

result = get_today()
print(json.dumps(result, indent=2))
```

## Output includes:

- **date**: The date format that matched
- **page**: Journal page metadata
- **blocks**: All blocks in the journal

## Related commands:

- `/logseq-expert:add-block` - Add content to today's journal
- `/logseq-expert:get-tasks` - See tasks from all journals
- `/logseq-expert:search` - Search across journals

## If journal not found:

The journal may not exist yet. Logseq creates journal pages when you first access them.
Try opening Logseq to create today's journal, or use `/logseq-expert:create-page` with the date.
