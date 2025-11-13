---
description: Migrate agent to current schema version and best practices
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [agent-name]
model: claude-sonnet-4-5
---

# Migrate Agent to Current Standards

Migrate the agent named: **$1** to current schema and best practices.

## Your Task

Automatically detect and apply schema migrations and best practice updates to bring an agent up to current standards.

### 1. **Locate Agent**

Find the agent file:
- `.claude/agents/$1.md` (project-level)
- `~/.claude/agents/$1.md` (user-level)
- Plugin directories: `*/agents/$1.md`

If not found, search by pattern and ask user to specify.

### 2. **Analyze Current State**

Run comprehensive analysis:

```bash
# Schema validation
python3 agent-builder/skills/building-agents/scripts/validate-agent.py <path>

# Quality analysis
python3 agent-builder/skills/building-agents/scripts/enhance-agent.py $1
```

Identify:
- Current schema version (inferred from structure)
- Missing required fields
- Outdated patterns
- Security issues
- Quality gaps

### 3. **Present Migration Assessment**

Show user what will be migrated:

```
Migration Assessment: $1

Current State:
  Schema Version: [Detected version]
  Validation: PASS / FAIL
  Enhancement Score: X.X/10

Issues Found:
  ❌ Critical: [count] issues
  ⚠️  Warnings: [count] issues
  💡 Improvements: [count] opportunities

Migration Plan:
  1. [Migration step 1]
  2. [Migration step 2]
  3. [Migration step 3]
  ...

Estimated Changes:
  - Schema updates: [count]
  - Security fixes: [count]
  - Quality improvements: [count]

Apply migration? (y/n)
```

### 4. **Execute Migration**

If user confirms, apply migrations in priority order:

#### Priority 1: Critical Schema Fixes

**Add missing YAML frontmatter** (if pre-1.0):

```markdown
<!-- Before -->
# My Agent
You are...

<!-- After -->
---
name: my-agent
description: [Extracted from first paragraph or heading]
---

# My Agent
You are...
```

**Fix invalid name**:
```yaml
# Before
name: My_Agent_V2

# After
name: my-agent-v2
```

**Add missing description**:
```yaml
# Before
---
name: my-agent
---

# After
---
name: my-agent
description: [Extract from role statement or first paragraph, max 1024 chars]
---
```

#### Priority 2: Security Hardening

**Remove unnecessary Bash**:
- Analyze agent body for Bash usage
- If no shell commands referenced, remove Bash from tools
- If Bash needed but no validation docs, add validation section

**Minimize tool permissions**:
- Analyze what tools are actually needed
- Remove over-permissioned tools
- Update to minimal necessary set

**Add input validation** (if has Bash):
```markdown
## Input Validation

Before executing any commands:
1. Validate file paths (no ../)
2. Sanitize arguments (remove shell metacharacters)
3. Whitelist allowed commands
4. Use proper escaping/quoting
```

#### Priority 3: Best Practice Updates

**Update model field** (if using specific version):
```yaml
# Before
model: claude-sonnet-4-5

# After
model: sonnet  # Version alias (more maintainable)
```

**Improve description clarity**:
```yaml
# Before
description: Helps with code

# After
description: [What it does] [Specialization]. Use when [scenario 1], [scenario 2], or [scenario 3].
```

**Add missing content sections**:
- Role definition (if missing)
- Capabilities list
- Step-by-step workflow
- 2-3 concrete examples
- Best practices guidelines
- Error handling documentation

### 5. **Show Migration Diff**

Before applying, show complete diff:

```diff
--- a/.claude/agents/my-agent.md
+++ b/.claude/agents/my-agent.md
@@ -1,5 +1,8 @@
+---
+name: my-agent
+description: Clear description of what agent does
+tools: Read, Grep, Glob
+model: sonnet
+---
+
 # My Agent

-You are a code helper.
+You are a specialized code analyzer with expertise in security and quality.
+
+## Your Capabilities
+1. Security analysis
+2. Code quality review
+3. Best practice recommendations
+
+## Your Workflow
+1. Read target files
+2. Analyze for issues
+3. Generate report
+
+## Examples
+
+### Example 1: Security Review
+...
```

Confirm: "Apply these changes? (y/n)"

### 6. **Apply Changes**

If confirmed:

1. **Backup original**:
   ```bash
   cp .claude/agents/$1.md .claude/agents/$1.md.pre-migration
   ```

2. **Apply migrations** using Edit or Write tool

3. **Validate result**:
   ```bash
   python3 validate-agent.py .claude/agents/$1.md
   ```

4. **Re-run enhancement**:
   ```bash
   python3 enhance-agent.py $1
   ```

### 7. **Generate Migration Report**

Show results:

```
Migration Complete: $1

Changes Applied:
  ✅ Added YAML frontmatter
  ✅ Fixed agent name (my_agent → my-agent)
  ✅ Added description field
  ✅ Minimized tools (removed Bash)
  ✅ Updated model (claude-sonnet-4-5 → sonnet)
  ✅ Added examples section
  ✅ Added error handling section

Before:
  Validation: FAIL
  Score: 4.5/10

After:
  Validation: PASS ✅
  Score: 8.0/10

Improvement: +3.5/10 (78% better)

Backup: .claude/agents/$1.md.pre-migration

Next Steps:
  1. Test agent functionality
  2. Review changes: git diff .claude/agents/$1.md
  3. Commit: git add .claude/agents/$1.md && git commit
  4. Remove backup if satisfied

Rollback:
  If issues, restore backup:
  mv .claude/agents/$1.md.pre-migration .claude/agents/$1.md
```

### 8. **Optional: Commit Changes**

Ask user if they want to commit:

```bash
Commit migration? (y/n)
> y

# Generate commit message
git add .claude/agents/$1.md
git commit -m "migrate(agent): upgrade $1 to current schema

Schema updates:
- Added YAML frontmatter
- Fixed naming convention
- Added description

Security improvements:
- Minimized tool permissions
- Removed unnecessary Bash access

Quality improvements:
- Added examples section
- Added error handling
- Improved description clarity

Enhanced score: 4.5/10 → 8.0/10 (+78%)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Migration Strategies

### Detect Schema Version

Infer version from file structure:

```python
def detect_schema_version(agent_content):
    # No frontmatter = pre-1.0
    if not agent_content.startswith('---'):
        return 'pre-1.0'

    # Parse frontmatter
    frontmatter = parse_yaml_frontmatter(agent_content)

    # Check for version indicators
    if not frontmatter.get('name') or not frontmatter.get('description'):
        return '0.x (incomplete)'

    # Has all required fields
    return '1.0 (current)'
```

### Automated Fixes

These can be applied automatically without user input:

✅ **Always safe**:
- Fix YAML syntax errors
- Standardize frontmatter formatting
- Fix name to lowercase-hyphens
- Truncate description to 1024 chars
- Remove duplicate tool entries

⚠️ **Require confirmation**:
- Add missing frontmatter (need to extract values)
- Change tool permissions (may break functionality)
- Update model (changes cost/performance)
- Add content sections (need quality content)

### Manual Intervention Required

Some migrations need human review:

- **Extracting description**: May need domain knowledge
- **Choosing minimal tools**: Need to understand agent purpose
- **Writing examples**: Require scenario knowledge
- **Security validation docs**: Need specific implementation details

For these, show placeholder and ask user to fill in:

```yaml
description: "[TODO: Describe what this agent does and when to use it]"
```

## Migration Modes

### Mode 1: Quick Migration (Automatic)

Apply only safe, automatic fixes:
- Schema formatting
- Name conventions
- Field validation
- Remove duplicates

```bash
/agent-builder:agents:migrate my-agent
> Mode: quick
```

### Mode 2: Standard Migration (Interactive)

Default mode with user confirmation:
- Schema fixes (auto)
- Security hardening (confirm)
- Quality improvements (confirm)
- Content additions (manual)

```bash
/agent-builder:agents:migrate my-agent
# Interactive prompts for each change
```

### Mode 3: Comprehensive Migration (Full)

Apply all possible improvements:
- Everything from standard
- Add all missing sections (with placeholders)
- Optimize model selection
- Modernize all patterns
- Generate examples (AI-powered)

```bash
/agent-builder:agents:migrate my-agent
> Mode: comprehensive
```

## Integration with Other Tools

### Uses enhance-agent.py
- Detect issues to migrate
- Score before/after
- Generate recommendations

### Uses update-agent.py
- Some migrations use update logic
- Share diff preview code
- Share backup mechanisms

### Uses validate-agent.py
- Verify schema before/after
- Ensure valid result
- Catch regressions

### References migration-guide.md
- Follow documented migration paths
- Use standard procedures
- Apply known patterns

## Error Handling

### If Agent Not Found
- Search for similar names
- List available agents
- Ask user to specify path

### If Migration Fails
- Show error clearly
- Keep original file unchanged
- Suggest manual migration steps
- Provide rollback instructions

### If Validation Fails After Migration
- Show validation errors
- Offer to revert changes
- Suggest fixing specific issues
- Provide manual fix guidance

## Examples

### Example 1: Pre-1.0 Agent

**Before**:
```markdown
# Code Helper

You are a helpful coding assistant.
```

**Migration**:
1. Add YAML frontmatter
2. Extract name from heading
3. Generate description from role
4. Add default tools

**After**:
```markdown
---
name: code-helper
description: Helpful coding assistant for general programming tasks. Use when you need assistance with coding questions or implementations.
tools: Read, Write, Edit, Grep, Glob
model: sonnet
---

# Code Helper

You are a helpful coding assistant.

## Your Capabilities
[Generated or prompted]

## Your Workflow
[Generated or prompted]
```

### Example 2: Over-Permissioned Agent

**Before**:
```yaml
---
name: file-reader
description: Reads files
tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
---
```

**Migration**:
1. Analyze tool usage (only reads files)
2. Remove unnecessary tools
3. Improve description

**After**:
```yaml
---
name: file-reader
description: File reading and content extraction utility. Use when you need to read and analyze file contents.
tools: Read, Grep, Glob
model: haiku
---
```

### Example 3: Incomplete Modern Agent

**Before**:
```yaml
---
name: security-checker
description: Checks code security
tools: Read, Grep, Glob
---

# Security Checker

You check code for security issues.
```

**Migration**:
1. Schema is valid (no changes)
2. Add missing content sections
3. Improve description specificity

**After**:
```yaml
---
name: security-checker
description: Security-focused code analyzer for identifying vulnerabilities and insecure patterns. Use when reviewing code for security concerns or auditing authentication.
tools: Read, Grep, Glob
model: sonnet
---

# Security Checker

You check code for security issues.

## Your Capabilities
1. OWASP Top 10 vulnerability detection
2. Authentication/authorization review
3. Input validation analysis
4. Security best practice recommendations

## Your Workflow
1. Read target code files
2. Scan for known vulnerability patterns
3. Analyze authentication/authorization logic
4. Check input validation
5. Generate security report with findings

## Examples

### Example 1: Authentication Review
**Task**: Review auth.py for security issues
**Process**: Analyze authentication flows, check for weaknesses
**Output**: Security report with severity ratings

## Error Handling
- File not found: Search in common locations, ask for clarification
- Syntax errors: Report issues, suggest fixes
- Large files: Warn about processing time, offer to sample
```

## Related Commands

- `/agent-builder:agents:update [name]` - Interactive updates
- `/agent-builder:agents:enhance [name]` - Quality analysis
- `/agent-builder:agents:audit` - Project-wide audit

## Related Resources

- `references/migration-guide.md` - Detailed migration documentation
- `references/agent-update-patterns.md` - Common update scenarios
- `templates/agent-checklist.md` - Quality review checklist

---

**Philosophy**: Migration should be safe, transparent, and reversible. Always show what will change, create backups, and provide rollback options. Automated fixes are great, but human review ensures quality.
