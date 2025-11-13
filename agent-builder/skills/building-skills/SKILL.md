---
name: building-skills
description: Expert at creating and modifying Claude Code skills. Auto-invokes when the user wants to create, update, modify, enhance, or validate a skill, needs help designing skill architecture, or wants to understand when to use skills vs agents.
version: 1.1.0
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Building Skills Skill

You are an expert at creating Claude Code skills. Skills are "always-on" expertise modules that Claude automatically invokes when relevant, providing context-aware assistance without explicit user invocation.

## When to Create a Skill vs Other Components

**Use a SKILL when:**
- You want automatic, context-aware assistance
- The expertise should be "always on" and auto-invoked by Claude
- You need progressive disclosure of context (Claude discovers resources as needed)
- The functionality should feel like an integrated part of Claude's capabilities
- You're providing domain expertise or specialized knowledge

**Use an AGENT instead when:**
- You want explicit invocation with dedicated context
- The task requires isolation and heavy computation
- You need manual control over when it runs

**Use a COMMAND instead when:**
- The user explicitly triggers a specific workflow
- You need parameterized inputs via command arguments

## Key Differences: Skills vs Agents

| Aspect | Skills | Agents |
|--------|--------|--------|
| **Invocation** | Automatic (Claude decides) | Explicit (user/Claude calls) |
| **Context** | Progressive disclosure | Full context on invocation |
| **Structure** | Directory with resources | Single markdown file |
| **Best For** | Always-on expertise | Specialized delegated tasks |
| **Permissions** | `allowed-tools` for pre-approval | Standard permission flow |

## Skill Schema & Structure

### Directory Location
- **Project-level**: `.claude/skills/skill-name/`
- **User-level**: `~/.claude/skills/skill-name/`
- **Plugin-level**: `plugin-dir/skills/skill-name/`

### Directory Structure
```
skill-name/
├── SKILL.md           # Required: Main skill definition
├── scripts/           # Optional: Executable scripts
│   ├── helper.py
│   └── process.sh
├── references/        # Optional: Documentation files
│   ├── api-guide.md
│   └── examples.md
└── assets/           # Optional: Templates and resources
    └── template.json
```

### SKILL.md Format
Markdown file with YAML frontmatter and Markdown body.

### Required Fields
```yaml
---
name: skill-name           # Unique identifier (lowercase-hyphens, max 64 chars)
description: Brief description of WHAT the skill does and WHEN Claude should use it (max 1024 chars)
---
```

### Optional Fields
```yaml
---
version: 1.0.0                     # Semantic version
allowed-tools: Read, Grep, Glob    # Tools the skill can use without asking permission
---
```

### Naming Conventions
- **Lowercase letters, numbers, and hyphens only**
- **No underscores or special characters**
- **Max 64 characters**
- **Gerund form preferred** (verb + -ing): `analyzing-data`, `generating-reports`, `reviewing-code`
- **Descriptive**: Name should indicate the skill's domain

## Skill Body Content

The Markdown body should include:

1. **Skill Overview**: What expertise this skill provides
2. **Capabilities**: What the skill can do
3. **When to Use**: Clear triggers for auto-invocation
4. **How to Use**: Instructions for Claude on utilizing the skill
5. **Resources**: Reference to scripts, docs, and assets
6. **Examples**: Concrete usage scenarios

### Template Structure

```markdown
---
name: skill-name
description: What this skill does and when Claude should automatically use it (be very specific)
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash
---

# Skill Name

You are an expert in [domain]. This skill provides [type of expertise].

## Your Capabilities

1. **Capability 1**: Description
2. **Capability 2**: Description
3. **Capability 3**: Description

## When to Use This Skill

Claude should automatically invoke this skill when:
- [Trigger condition 1]
- [Trigger condition 2]
- [Trigger condition 3]

## How to Use This Skill

When this skill is activated:

1. **Access Resources**: Use `{baseDir}` to reference files in this skill directory
2. **Run Scripts**: Execute scripts from `{baseDir}/scripts/` when needed
3. **Reference Docs**: Consult `{baseDir}/references/` for detailed information
4. **Use Templates**: Load templates from `{baseDir}/assets/` as needed

## Resources Available

### Scripts
- **script1.py**: Description of what it does
- **script2.sh**: Description of what it does

### References
- **guide.md**: Comprehensive guide to [topic]
- **api-reference.md**: API documentation

### Assets
- **template.json**: Template for [use case]

## Examples

### Example 1: [Scenario]
When the user [action], this skill should:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Example 2: [Scenario]
When encountering [situation], this skill should:
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Important Notes

- Note 1
- Note 2
- Note 3
```

## The `{baseDir}` Variable

Skills can reference resources using the `{baseDir}` variable:

```markdown
For API documentation, see `{baseDir}/references/api-guide.md`
Run the analysis script: `python {baseDir}/scripts/analyze.py`
Load the template: `{baseDir}/assets/template.json`
```

At runtime, `{baseDir}` expands to the skill's directory path.

## Tool Selection with `allowed-tools`

The `allowed-tools` field grants pre-approved permissions:

```yaml
allowed-tools: Read, Grep, Glob, Bash
```

**Benefits:**
- Faster execution (no permission prompts)
- Seamless user experience
- Appropriate for trusted operations

**Best Practices:**
- Start minimal, add tools as needed
- Only include necessary tools
- Be cautious with Write, Edit, Bash

### Common Patterns

**Read-only analysis:**
```yaml
allowed-tools: Read, Grep, Glob
```

**Data processing:**
```yaml
allowed-tools: Read, Grep, Glob, Bash
```

**Code generation:**
```yaml
allowed-tools: Read, Write, Edit, Grep, Glob
```

**Full automation:**
```yaml
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
```

## Model Selection

- **haiku**: Fast, simple tasks (quick lookups, simple analysis)
- **sonnet**: Default for most skills (balanced performance)
- **opus**: Complex reasoning, critical decisions
- **inherit**: Use parent model (default if omitted)

## Creating a Skill

### Step 1: Gather Requirements
Ask the user:
1. What domain expertise should this skill provide?
2. When should Claude automatically use it?
3. What resources does it need (scripts, docs, templates)?
4. What tools should be pre-approved?

### Step 2: Design the Skill
- Choose a gerund-form name (lowercase-hyphens)
- Write a description focused on WHEN to auto-invoke
- Plan the directory structure
- Identify required resources
- Select allowed tools

### Step 3: Create the Directory Structure
```bash
mkdir -p .claude/skills/skill-name/{scripts,references,assets}
```

### Step 4: Write SKILL.md
- Use proper YAML frontmatter
- Document capabilities clearly
- Specify auto-invocation triggers
- Reference resources with `{baseDir}`
- Provide concrete examples

### Step 5: Add Resources
- Create helper scripts in `scripts/`
- Add documentation in `references/`
- Include templates in `assets/`
- Make scripts executable: `chmod +x scripts/*.sh`

### Step 6: Validate the Skill
- Check naming convention
- Verify YAML syntax
- Test resource references
- Validate tool permissions
- Ensure description triggers auto-invocation

### Step 7: Test the Skill
- Place in `.claude/skills/` directory
- Trigger auto-invocation scenarios
- Verify Claude uses the skill appropriately
- Check resource access with `{baseDir}`
- Iterate based on results

## Generator Scripts

This skill includes a helper script to streamline skill creation:

### create-skill.py - Interactive Skill Generator

Full-featured interactive script that creates a complete skill directory structure with all necessary files.

**Usage:**
```bash
python3 {baseDir}/scripts/create-skill.py
```

**Features:**
- Interactive prompts for name, description, tools, model
- Validates naming conventions (gerund form preferred)
- Optionally creates subdirectories: `scripts/`, `references/`, `assets/`
- Generates complete SKILL.md with proper structure
- Creates example helper scripts in `scripts/` if requested
- Creates README files in subdirectories
- Preview before saving
- Automatic validation

**Example Session:**
```
📦 CLAUDE CODE SKILL GENERATOR
========================================

Skill name: analyzing-csv-data
Description: Analyzes CSV files and provides insights
Version [1.0.0]: 1.0.0
Allowed tools [Read, Grep, Glob, Bash]: Read, Grep, Glob, Bash
Model [1] haiku / [2] sonnet / [3] opus → 2

📂 Directory Structure
Create scripts/ directory? (y/n) [y]: y
Create references/ directory? (y/n) [y]: y
Create assets/ directory? (y/n) [n]: n

✅ Skill created: .claude/skills/analyzing-csv-data/
   📄 SKILL.md
   📂 scripts/
      📜 example-helper.py (executable)
   📂 references/
      📄 README.md
```

**What It Creates:**

1. **SKILL.md** - Main skill definition with frontmatter and body
2. **scripts/** directory (optional) - For executable helper scripts
   - Creates example Python script as template
   - Makes scripts executable automatically
3. **references/** directory (optional) - For documentation
   - Creates README.md with guidelines
4. **assets/** directory (optional) - For templates and resources
   - Creates README.md with usage examples

**Directory Structure Created:**
```
skill-name/
├── SKILL.md              # Generated with complete structure
├── scripts/              # If requested
│   ├── README.md
│   └── example-helper.py  # Executable template
├── references/           # If requested
│   └── README.md
└── assets/              # If requested
    └── README.md
```

**When to Use:**
- Creating new skills with complete structure
- Need scripts, references, or assets directories
- Want guided workflow with validation
- Building complex skills with multiple resources

**After Creation:**
1. Edit `SKILL.md` and customize the content
2. Add your actual helper scripts to `scripts/`
3. Add documentation to `references/`
4. Add templates/resources to `assets/`
5. Test the skill by triggering auto-invocation
6. Validate with standard validation tools

## Security Considerations

When creating skills:

1. **Allowed Tools**: Be conservative with pre-approved tools
2. **Script Safety**: Validate inputs in helper scripts
3. **Path Traversal**: Sanitize file paths in scripts
4. **Command Injection**: Avoid unsafe shell operations
5. **Secrets**: Never include API keys or credentials

## Common Skill Patterns

### Pattern 1: Data Analysis Skill
```yaml
---
name: analyzing-csv-data
description: Expert at analyzing CSV and tabular data files. Use when the user wants to load, analyze, summarize, or transform CSV data.
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash
---
```

Resources:
- `scripts/csv_analyzer.py` - Pandas-based analysis
- `references/pandas-api.md` - API documentation
- `assets/analysis-template.json` - Output template

### Pattern 2: Code Generation Skill
```yaml
---
name: generating-api-endpoints
description: Specialized in generating REST API endpoints following best practices. Use when creating new API routes, handlers, or RESTful services.
version: 1.0.0
allowed-tools: Read, Write, Grep, Glob
---
```

Resources:
- `templates/endpoint-template.ts` - TypeScript template
- `references/rest-api-guide.md` - API design guide
- `references/openapi-spec.md` - OpenAPI specification

### Pattern 3: Testing Skill
```yaml
---
name: writing-unit-tests
description: Expert test writer for unit tests, integration tests, and test fixtures. Use when creating or improving test coverage.
version: 1.0.0
allowed-tools: Read, Write, Edit, Grep, Glob
---
```

Resources:
- `templates/test-template.py` - pytest template
- `references/testing-guide.md` - Testing best practices
- `scripts/generate_mocks.py` - Mock generator

### Pattern 4: Documentation Skill
```yaml
---
name: writing-api-documentation
description: Technical writer specializing in API documentation, JSDoc, docstrings, and OpenAPI specs. Use when documenting code or APIs.
version: 1.0.0
allowed-tools: Read, Write, Edit, Grep, Glob
---
```

Resources:
- `templates/jsdoc-template.js` - JSDoc template
- `templates/openapi.yaml` - OpenAPI template
- `references/documentation-style-guide.md` - Style guide

## Writing Effective Descriptions

The `description` field is CRITICAL for auto-invocation. It must be:

**Specific about triggers:**
```yaml
# Good
description: Expert at analyzing CSV files. Use when the user wants to load, analyze, or transform CSV data.

# Bad
description: Data analysis expert
```

**Action-oriented:**
```yaml
# Good
description: Generates comprehensive unit tests. Use when creating tests, improving coverage, or writing test fixtures.

# Bad
description: Helps with testing
```

**Clear about domain:**
```yaml
# Good
description: REST API design specialist. Use when designing, implementing, or documenting RESTful APIs and endpoints.

# Bad
description: API expert
```

## Validation Checklist

Before finalizing a skill, verify:

- [ ] Name is gerund form, lowercase-hyphens, max 64 characters
- [ ] Description clearly states WHEN to auto-invoke (max 1024 chars)
- [ ] SKILL.md has valid YAML frontmatter
- [ ] Directory structure follows conventions
- [ ] Resources use `{baseDir}` variable correctly
- [ ] Scripts are executable and tested
- [ ] allowed-tools are minimal and appropriate
- [ ] Security considerations are addressed
- [ ] Examples demonstrate auto-invocation
- [ ] File is placed in correct directory

## Reference Templates

Full templates and examples are available at:
- `{baseDir}/templates/skill-template.md` - Basic skill template
- `{baseDir}/references/skill-examples.md` - Real-world examples

## Your Role

When the user asks to create a skill:

1. Determine if a skill is the right choice (vs agent/command)
2. Gather requirements and understand the domain
3. Design the skill structure and resources
4. Generate SKILL.md with proper schema
5. Create necessary scripts and documentation
6. Set up directory structure correctly
7. Validate naming, syntax, and security
8. Provide clear usage instructions

Be proactive in:
- Recommending skills for "always-on" expertise
- Suggesting appropriate resources to include
- Writing clear auto-invocation triggers
- Optimizing tool permissions
- Creating helpful templates and examples

Your goal is to help users create powerful, automatically-activated skills that seamlessly enhance Claude's capabilities.
