---
description: Define a new typed property for Logseq DB graphs with proper schema configuration
allowed-tools: Read, WebFetch
argument-hint: "<property-name> [type]"
---

# Define Logseq Property

Create a properly configured property definition for Logseq DB graphs.

**Input:** $ARGUMENTS

## Property Types

| Type | Use Case | Example Values |
|------|----------|----------------|
| `:default` | Text, rich content | "Hello world", blocks with children |
| `:number` | Numeric values | 42, 3.14, ratings |
| `:date` | Calendar dates | Links to journal pages |
| `:datetime` | Date + time | Scheduling with times |
| `:checkbox` | Boolean toggle | true/false |
| `:url` | Web links | https://example.com |
| `:node` | Page/block refs | [[Page Name]] |
| `:class` | Class entities | #Book, #Person |

## Property Configuration Options

```clojure
{:db/ident :user.property/property-name    ; Required: unique identifier
 :block/title "Property Name"               ; Required: display name
 :logseq.property/type :default             ; Required: value type
 :logseq.property/cardinality :one          ; :one or :many
 :logseq.property/hide? false               ; Hide by default
 :logseq.property.ui/position :properties   ; UI placement
 :logseq.property/closed-values [...]       ; Restricted choices (optional)
 :logseq.property/schema-classes [...]}     ; Associated classes (optional)
```

## UI Position Options

- `:properties` - Standard properties section
- `:block-beginning` - Before block content
- `:block-below` - After block content
- `:block-end` - At bottom of block

## Process

1. Parse property name from input
2. Infer or use specified type
3. Determine if closed values needed
4. Check for class association
5. Generate complete definition

## Output Format

```markdown
## Property: [name]

### Definition (EDN)
\`\`\`clojure
{:db/ident :user.property/[name]
 :block/title "[Display Name]"
 :logseq.property/type :[type]
 ...}
\`\`\`

### Usage

**In UI:** Add property "[name]" to any block

**In Query:**
\`\`\`clojure
[:find ?b
 :where [?b :user.property/[name] ?value]]
\`\`\`

**In Plugin:**
\`\`\`javascript
await logseq.Editor.upsertBlockProperty(uuid, '[name]', value)
\`\`\`

### Associate with Class (Optional)
To make this property appear on all blocks with a specific tag:
\`\`\`clojure
;; Add to class definition
{:db/ident :user.class/MyClass
 :logseq.property/schema-classes [:user.property/[name]]}
\`\`\`
```

Generate the property definition for: **$ARGUMENTS**
