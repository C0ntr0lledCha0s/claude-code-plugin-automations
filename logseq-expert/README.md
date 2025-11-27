# Logseq Expert Plugin

Expert plugin for working with Logseq's new database-based architecture. Provides deep knowledge of the Datascript schema, built-in classes and properties, Datalog query building, plugin development, and MD-to-DB migration assistance.

## Features

### Agent
- **logseq-db-expert**: Orchestrator agent with comprehensive Logseq DB expertise

### Skills (Auto-Invoke)
| Skill | Triggers On |
|-------|-------------|
| `understanding-db-schema` | Questions about Datascript, classes, properties, schema |
| `building-logseq-plugins` | Plugin development, Logseq API, DB-compatible plugins |
| `querying-logseq-data` | Datalog queries, query optimization, pull syntax |
| `migrating-to-db` | MD to DB migration, import/export, compatibility |

### Commands
| Command | Purpose |
|---------|---------|
| `/logseq-expert:query <description>` | Build Datalog queries from natural language |
| `/logseq-expert:define-property <name>` | Define typed properties with schema |
| `/logseq-expert:define-class <name>` | Define classes with inherited properties |
| `/logseq-expert:check-migration [path]` | Analyze MD graph for DB compatibility |
| `/logseq-expert:explain <concept>` | Explain DB schema concepts |

## Installation

```bash
# Clone the plugins repository
git clone https://github.com/C0ntr0lledCha0s/claude-code-plugins.git

# Symlink to Claude Code plugins directory
ln -s $(pwd)/claude-code-plugins/logseq-expert ~/.claude/plugins/logseq-expert
```

## Usage Examples

### Build a Query
```
/logseq-expert:query find all books rated 5 stars by Stephen King
```

Output:
```clojure
[:find (pull ?b [:block/title :user.property/rating :user.property/author])
 :where
 [?b :block/tags ?t]
 [?t :block/title "Book"]
 [?b :user.property/rating 5]
 [?b :user.property/author "Stephen King"]]
```

### Define a Class
```
/logseq-expert:define-class Person
```

Output:
```clojure
{:db/ident :user.class/Person
 :block/title "Person"
 :block/tags [:logseq.class/Tag]
 :logseq.property.class/extends :logseq.class/Root
 :logseq.property/schema-classes
   [:user.property/email
    :user.property/phone
    :user.property/company]}
```

### Check Migration Compatibility
```
/logseq-expert:check-migration ~/logseq/my-graph
```

### Explain Concepts
```
/logseq-expert:explain datascript
/logseq-expert:explain classes vs tags
/logseq-expert:explain property types
```

## Logseq DB Schema Overview

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Nodes** | Unified term for pages and blocks |
| **Classes** | Tags with inherited properties (supertags) |
| **Properties** | Typed key-value metadata |
| **Datascript** | Clojure in-memory database engine |

### Property Types

| Type | Use Case | Example |
|------|----------|---------|
| `:default` | Text content | "Hello world" |
| `:number` | Numeric values | 42, 3.14 |
| `:date` | Calendar dates | Journal links |
| `:datetime` | Date + time | Scheduling |
| `:checkbox` | Boolean | true/false |
| `:url` | Web links | https://... |
| `:node` | References | [[Page]] |
| `:class` | Class refs | #Book |

### Built-in Classes

```
:logseq.class/Root
├── :logseq.class/Page
├── :logseq.class/Tag
├── :logseq.class/Property
├── :logseq.class/Task
├── :logseq.class/Query
├── :logseq.class/Asset
└── :logseq.class/Journal
```

## DB vs MD Comparison

| Feature | MD Version | DB Version |
|---------|------------|------------|
| Storage | Markdown files | SQLite |
| Tags | Page references | Classes with properties |
| Properties | Text strings | Typed values |
| Queries | Limited | Full Datalog |
| Sync | File-based | Real-time (Pro) |

## Current Status

⚠️ **Logseq DB is in alpha** (as of early 2025)

- Some features still in development (whiteboards)
- Plugin compatibility varies
- Multi-device sync requires subscription
- Export options limited

## Resources

- [Logseq DB Documentation](https://github.com/logseq/docs/blob/master/db-version.md)
- [Database Schema DeepWiki](https://deepwiki.com/logseq/logseq/4.2-views-and-tables)
- [Logseq Plugin SDK](https://plugins-doc.logseq.com/)
- [Logseq DB Unofficial FAQ](https://discuss.logseq.com/t/logseq-db-unofficial-faq/32508)

## Contributing

Found an issue or want to improve the Logseq expertise? Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT
