---
description: Explain Logseq DB schema concepts, terminology, and architecture in detail
allowed-tools: Read, WebFetch, WebSearch
argument-hint: "<concept>"
---

# Explain Logseq DB Concept

Provide a detailed explanation of Logseq DB schema concepts, terminology, or architecture.

**Input:** $ARGUMENTS

## Core Concepts to Explain

### Data Model
- **Nodes** - Unified concept for pages and blocks
- **Datascript** - The underlying database engine
- **EAV Model** - Entity-Attribute-Value structure
- **Schema** - Attribute definitions and constraints

### Entity Types
- **Pages** - Top-level named entities
- **Blocks** - Content units within pages
- **Classes** - Tags/supertags with properties
- **Properties** - Typed key-value metadata
- **Journals** - Date-based pages

### Schema Components
- **Attributes** - `:db/ident`, `:db/valueType`, `:db/cardinality`
- **Types** - `:default`, `:number`, `:date`, `:checkbox`, `:url`, `:node`
- **Cardinality** - `:one` vs `:many`
- **Validation** - Malli schemas

### Relationships
- **References** - `:block/refs`, `:block/tags`
- **Hierarchy** - `:block/parent`, `:block/page`
- **Inheritance** - `:logseq.property.class/extends`

### Queries
- **Datalog** - Query language
- **Pull syntax** - Entity retrieval
- **Rules** - Reusable query logic
- **Aggregations** - count, sum, avg, etc.

## Explanation Format

```markdown
## [Concept Name]

### What It Is
[Clear, concise definition]

### Why It Matters
[Practical importance in Logseq]

### Technical Details
[Schema representation, code examples]

### How to Use It
[Practical examples in Logseq UI and API]

### Common Patterns
[Typical use cases]

### Related Concepts
- [Related 1] - [brief connection]
- [Related 2] - [brief connection]

### MD vs DB Differences
| Aspect | MD Version | DB Version |
|--------|------------|------------|
| ... | ... | ... |

### Examples

**In UI:**
[How it appears/works in Logseq UI]

**In Datalog:**
\`\`\`clojure
[query example]
\`\`\`

**In Plugin:**
\`\`\`javascript
[API example]
\`\`\`

### Gotchas
- [Common mistake 1]
- [Common mistake 2]

### Further Reading
- [Resource 1]
- [Resource 2]
```

## Quick Reference Topics

If concept is unclear, offer these options:

| Category | Topics |
|----------|--------|
| **Basics** | nodes, pages, blocks, properties, tags |
| **Schema** | datascript, attributes, types, cardinality |
| **Classes** | inheritance, schema-classes, built-in classes |
| **Properties** | types, closed-values, namespaces |
| **Queries** | datalog, pull, rules, aggregations |
| **Migration** | MD vs DB, import, export |
| **Plugins** | API, block properties, queries |

Explain: **$ARGUMENTS**
