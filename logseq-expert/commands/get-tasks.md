---
description: Get TODO/DOING/DONE tasks from your Logseq graph
argument-hint: [status]
allowed-tools: Read, Bash
---

# Get Logseq Tasks

Retrieve tasks (TODO, DOING, DONE, etc.) from your Logseq graph.

## Arguments

- `$ARGUMENTS` - Optional status filter: TODO, DOING, DONE, NOW, LATER, WAITING (default: all)

## Usage

Get tasks with status: $ARGUMENTS (or all if not specified).

## How to get tasks:

```python
import json
import urllib.request
import os

def get_tasks(status=None, limit=100):
    token = os.environ.get("LOGSEQ_API_TOKEN", "")
    url = os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315")

    # Build query
    if status:
        query = f'''
        [:find (pull ?b [:block/uuid :block/content :block/marker :block/priority {{:block/page [:block/name]}}])
         :where
         [?b :block/marker ?m]
         [(= ?m "{status.upper()}")]]
        '''
    else:
        query = '''
        [:find (pull ?b [:block/uuid :block/content :block/marker :block/priority {:block/page [:block/name]}])
         :where
         [?b :block/marker ?m]
         [(contains? #{"TODO" "DOING" "DONE" "NOW" "LATER" "WAITING" "CANCELLED"} ?m)]]
        '''

    req = urllib.request.Request(
        f"{url}/api",
        data=json.dumps({"method": "logseq.DB.datascriptQuery", "args": [query]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )

    with urllib.request.urlopen(req) as resp:
        results = json.loads(resp.read())["result"]

    tasks = []
    for r in results[:limit]:
        block = r[0]
        tasks.append({
            "uuid": block.get("block/uuid"),
            "marker": block.get("block/marker"),
            "priority": block.get("block/priority"),
            "content": block.get("block/content"),
            "page": block.get("block/page", {}).get("block/name")
        })

    return {"status": status or "ALL", "count": len(tasks), "tasks": tasks}

status_filter = "$ARGUMENTS" if "$ARGUMENTS" else None
result = get_tasks(status_filter)
print(json.dumps(result, indent=2))
```

## Examples:

- `/logseq-expert:get-tasks` - Get all tasks
- `/logseq-expert:get-tasks TODO` - Get only TODO items
- `/logseq-expert:get-tasks DOING` - Get in-progress tasks
- `/logseq-expert:get-tasks DONE` - Get completed tasks

## Task statuses:

| Status | Description |
|--------|-------------|
| TODO | Not started |
| DOING | In progress |
| DONE | Completed |
| NOW | Immediate priority |
| LATER | Deferred |
| WAITING | Blocked/waiting |
| CANCELLED | Cancelled |

## Output:

Each task includes:
- **uuid**: Block identifier
- **marker**: Task status
- **priority**: Priority level (A, B, C)
- **content**: Full block content
- **page**: Source page name
