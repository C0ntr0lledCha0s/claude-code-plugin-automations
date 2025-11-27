---
description: Analyze a Logseq MD graph for DB migration compatibility and potential issues
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
argument-hint: "[graph-path]"
---

# Check Logseq Migration Compatibility

Analyze a Markdown-based Logseq graph for potential issues when migrating to DB format.

**Input:** $ARGUMENTS

## Analysis Steps

### 1. Graph Structure Analysis
- Count total pages and blocks
- Identify namespaced pages
- Find orphaned files
- Check for unusual file structures

### 2. Tag Analysis
```bash
# Find all tags in the graph
grep -roh '#[A-Za-z][A-Za-z0-9_-]*' pages/ journals/ | sort | uniq -c | sort -rn
```

Issues to flag:
- Tags that should become classes vs simple refs
- Nested tags (#parent/child)
- Inconsistent tag usage

### 3. Property Analysis
```bash
# Find all properties
grep -roh '^[a-zA-Z_-]*::' pages/ journals/ | sort | uniq -c | sort -rn
```

Issues to flag:
- Mixed property formats
- Properties that should be typed (dates, numbers)
- Properties with inconsistent values

### 4. Reference Analysis
```bash
# Find all page references
grep -roh '\[\[[^\]]*\]\]' pages/ journals/ | sort | uniq -c | sort -rn
```

Issues to flag:
- Broken references (to non-existent pages)
- Namespace references
- Alias issues

### 5. Query Analysis
```bash
# Find existing queries
grep -r '{{query' pages/ journals/ --include="*.md"
grep -r 'BEGIN_QUERY' pages/ journals/ --include="*.md"
```

Issues to flag:
- Queries using MD-specific attributes
- Complex queries needing updates

## Output Format

```markdown
## Migration Analysis: [Graph Name]

### Summary
| Metric | Count |
|--------|-------|
| Pages | X |
| Journals | X |
| Blocks (est.) | X |
| Tags | X |
| Properties | X |
| Queries | X |

### ✅ Ready for Migration
- [List items that will migrate cleanly]

### ⚠️ Needs Review
| Issue | Count | Recommendation |
|-------|-------|----------------|
| Namespaced pages | X | Decide: flatten or hierarchy |
| Mixed property types | X | Standardize before migration |
| Custom queries | X | Will need updating |

### ❌ Potential Problems
| Problem | Details | Solution |
|---------|---------|----------|
| Broken refs | X pages | Fix before migrating |
| Inconsistent tags | #Tag vs [[Tag]] | Standardize usage |

### Tag → Class Recommendations
| Tag | Usage Count | Recommend |
|-----|-------------|-----------|
| #Project | 50 | → Class with properties |
| #TODO | 200 | → Use built-in Task |
| #person | 30 | → Class: Person |

### Property Type Recommendations
| Property | Values Sample | Suggested Type |
|----------|---------------|----------------|
| rating:: | 1, 2, 3, 4, 5 | :number |
| due:: | 2024-01-15 | :date |
| done:: | true, false | :checkbox |

### Pre-Migration Checklist
- [ ] Back up entire graph
- [ ] Standardize tag format
- [ ] Fix broken references
- [ ] Document custom queries
- [ ] Plan class hierarchy
- [ ] Test with small subset first

### Migration Command
\`\`\`
1. Export: Settings → Export → EDN
2. Create new DB graph
3. Import with these settings:
   - Tags as classes: [recommended tags]
   - Property types: [infer/manual]
   - Namespaces: [flatten/hierarchy]
\`\`\`
```

Analyze the graph at: **$ARGUMENTS**

If no path provided, give general guidance on what to check.
