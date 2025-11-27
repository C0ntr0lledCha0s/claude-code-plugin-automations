---
description: Define a new class (tag) for Logseq DB graphs with inherited properties
allowed-tools:
  - Read
  - WebFetch
argument-hint: "<class-name> [parent-class]"
---

# Define Logseq Class

Create a properly configured class (tag/supertag) definition for Logseq DB graphs.

**Input:** $ARGUMENTS

## Class Concepts

In Logseq DB:
- **Classes** = Tags = Supertags (same thing)
- Classes can have **properties** that auto-apply to tagged blocks
- Classes support **inheritance** (extends parent classes)
- Classes are themselves pages tagged with `#Tag`

## Class Definition Structure

```clojure
{:db/ident :user.class/ClassName          ; Unique identifier
 :block/title "ClassName"                  ; Display name
 :block/tags [:logseq.class/Tag]          ; Makes it a class
 :logseq.property.class/extends :logseq.class/Root  ; Parent class
 :logseq.property/schema-classes           ; Properties for this class
   [:user.property/prop1
    :user.property/prop2]}
```

## Built-in Classes to Extend

| Class | Purpose | Inherits |
|-------|---------|----------|
| `:logseq.class/Root` | Base class | - |
| `:logseq.class/Page` | Regular pages | Root |
| `:logseq.class/Task` | Tasks with status | Root |
| `:logseq.class/Query` | Saved queries | Root |
| `:logseq.class/Asset` | File attachments | Root |

## Process

1. Parse class name from input
2. Determine parent class (default: Root)
3. Identify needed properties
4. Generate class definition
5. Generate associated property definitions

## Common Class Patterns

### Simple Class
```clojure
;; #Book class
{:db/ident :user.class/Book
 :block/title "Book"
 :block/tags [:logseq.class/Tag]
 :logseq.property.class/extends :logseq.class/Root}
```

### Class with Properties
```clojure
;; #Person with contact info
{:db/ident :user.class/Person
 :block/title "Person"
 :block/tags [:logseq.class/Tag]
 :logseq.property.class/extends :logseq.class/Root
 :logseq.property/schema-classes
   [:user.property/email
    :user.property/phone
    :user.property/company]}
```

### Inherited Class
```clojure
;; #Audiobook extends #Book
{:db/ident :user.class/Audiobook
 :block/title "Audiobook"
 :block/tags [:logseq.class/Tag]
 :logseq.property.class/extends :user.class/Book
 :logseq.property/schema-classes
   [:user.property/narrator
    :user.property/duration]}
```

## Output Format

```markdown
## Class: [name]

### Class Definition
\`\`\`clojure
{:db/ident :user.class/[name]
 :block/title "[Name]"
 :block/tags [:logseq.class/Tag]
 :logseq.property.class/extends :[parent]
 :logseq.property/schema-classes [...]}
\`\`\`

### Associated Properties
\`\`\`clojure
;; Property 1
{:db/ident :user.property/prop1
 :block/title "Prop1"
 :logseq.property/type :default}

;; Property 2
...
\`\`\`

### Usage

**Tag a block:**
\`\`\`
- My Item #[Name]
\`\`\`

**Query all instances:**
\`\`\`clojure
[:find (pull ?b [*])
 :where
 [?b :block/tags ?t]
 [?t :block/title "[Name]"]]
\`\`\`

### Hierarchy
\`\`\`
:logseq.class/Root
└── :[parent]
    └── :user.class/[name]
\`\`\`
```

Generate the class definition for: **$ARGUMENTS**
