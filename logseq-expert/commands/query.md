---
description: Build a Datalog query for Logseq DB graphs based on natural language description
allowed-tools: Read, WebFetch, WebSearch
argument-hint: "<query-description>"
---

# Build Logseq Datalog Query

Generate an optimized Datalog query for Logseq DB graphs based on the user's description.

**Input:** $ARGUMENTS

## Query Building Process

1. **Parse the request** - Understand what data the user wants to find
2. **Identify entities** - Pages, blocks, tasks, or custom classes
3. **Determine filters** - Properties, tags, dates, relationships
4. **Choose output format** - Pull syntax, aggregations, or simple values
5. **Optimize** - Put selective clauses first, minimize wildcards

## Query Components

### Find Clause
- `(pull ?e [*])` - All attributes
- `(pull ?e [:block/title :user.property/rating])` - Specific attributes
- `?title ?author` - Multiple values
- `(count ?e)` - Aggregations

### Where Clause Patterns
- `[?b :block/tags ?t]` - Tag/class membership
- `[?t :block/title "Book"]` - String match
- `[?b :user.property/rating ?r]` - Property access
- `[(>= ?r 4)]` - Comparisons
- `(not [...])` - Negation
- `(or [...] [...])` - Disjunction

## Output Format

Provide:
1. **The Datalog query** - Ready to use
2. **Explanation** - What each clause does
3. **Usage** - How to run it (query block or API)
4. **Variations** - Alternative versions if applicable

## Example Transformations

| Natural Language | Query Pattern |
|------------------|---------------|
| "Find all books" | `[?b :block/tags ?t] [?t :block/title "Book"]` |
| "Books rated 5 stars" | Add `[?b :user.property/rating 5]` |
| "Unread books" | Add `[?b :user.property/status "To Read"]` |
| "Books by Stephen King" | Add `[?b :user.property/author "Stephen King"]` |
| "Count books per author" | Use `(count ?b)` with grouping |

## Response Template

```markdown
## Query: [Description]

### Datalog Query
\`\`\`clojure
[:find (pull ?b [:block/title ...])
 :where
 ...]
\`\`\`

### Explanation
- Line 1: ...
- Line 2: ...

### Usage

**In Query Block:**
\`\`\`
#+BEGIN_QUERY
{:title "..."
 :query [:find ...]}
#+END_QUERY
\`\`\`

**In Plugin (JavaScript):**
\`\`\`javascript
const results = await logseq.DB.datascriptQuery(\`...\`)
\`\`\`

### Variations
- To also include X: add `[...]`
- To exclude Y: add `(not [...])`
```

Generate the query now based on: **$ARGUMENTS**
