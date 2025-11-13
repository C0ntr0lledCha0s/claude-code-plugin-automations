---
description: Compare two agents side-by-side to understand differences and trade-offs
allowed-tools: Read, Grep, Glob
argument-hint: '[agent1] [agent2]'
model: claude-haiku-4-5
---

# Compare Two Agents

Compare agents: **$1** vs **$2**

## Your Task

Provide side-by-side comparison of two agents to help users understand differences and choose the right one.

### 1. **Locate Both Agents**

Find agent files:
- Agent 1: Search for `$1.md` in `.claude/agents/`, plugins, user directory
- Agent 2: Search for `$2.md` in same locations

If either not found:
- Show error with suggestions
- List available agents
- Ask user to provide correct names

### 2. **Load and Parse**

For each agent, extract:
- **Metadata**: name, description, tools, model
- **Content**: role, capabilities, workflow, examples
- **Stats**: file size, section count, word count

### 3. **Generate Comparison Report**

```markdown
# Agent Comparison: $1 vs $2

## Quick Summary

| Aspect | $1 | $2 |
|--------|-----|-----|
| **Purpose** | <brief description> | <brief description> |
| **Complexity** | <simple/moderate/complex> | <simple/moderate/complex> |
| **Tools** | <count> tools | <count> tools |
| **Model** | <model> | <model> |
| **Best For** | <use case> | <use case> |

## When to Use Which?

### Use $1 when:
- <scenario 1>
- <scenario 2>
- <scenario 3>

### Use $2 when:
- <scenario 1>
- <scenario 2>
- <scenario 3>

## Detailed Comparison

### Metadata

| Field | $1 | $2 |
|-------|-----|-----|
| **Name** | $1 | $2 |
| **Description** | <desc> | <desc> |
| **Tools** | <tools list> | <tools list> |
| **Model** | <model> | <model> |
| **Location** | <path> | <path> |

### Tool Permissions

**$1**: <tools>
- Security level: <high/medium/low>
- Can modify files: <yes/no>
- Can run commands: <yes/no>
- Web access: <yes/no>

**$2**: <tools>
- Security level: <high/medium/low>
- Can modify files: <yes/no>
- Can run commands: <yes/no>
- Web access: <yes/no>

**Analysis**:
- More permissive: <agent with more tools>
- More restrictive: <agent with fewer tools>
- Security implications: <explanation>

### Model Selection

**$1**: <model>
- Speed: <fast/medium/slow>
- Cost: <low/medium/high>
- Capability: <basic/standard/advanced>

**$2**: <model>
- Speed: <fast/medium/slow>
- Cost: <low/medium/high>
- Capability: <basic/standard/advanced>

**Analysis**:
- Faster: <agent>
- More capable: <agent>
- More cost-effective: <agent>

### Capabilities

**$1 can**:
- <capability 1>
- <capability 2>
- <capability 3>

**$2 can**:
- <capability 1>
- <capability 2>
- <capability 3>

**Unique to $1**:
- <unique capability>

**Unique to $2**:
- <unique capability>

**Shared capabilities**:
- <common capability>

### Workflow Comparison

**$1 approach**:
1. <step 1>
2. <step 2>
3. <step 3>

**$2 approach**:
1. <step 1>
2. <step 2>
3. <step 3>

**Key differences**:
- $1 focuses on: <approach>
- $2 focuses on: <approach>

### Content Quality

| Aspect | $1 | $2 |
|--------|-----|-----|
| **Role definition** | ✅/⚠️/❌ | ✅/⚠️/❌ |
| **Capabilities** | ✅/⚠️/❌ | ✅/⚠️/❌ |
| **Workflow** | ✅/⚠️/❌ | ✅/⚠️/❌ |
| **Examples** | ✅/⚠️/❌ | ✅/⚠️/❌ |
| **Best practices** | ✅/⚠️/❌ | ✅/⚠️/❌ |
| **Error handling** | ✅/⚠️/❌ | ✅/⚠️/❌ |
| **Documentation** | ✅/⚠️/❌ | ✅/⚠️/❌ |

### Statistics

| Metric | $1 | $2 |
|--------|-----|-----|
| **File size** | <size> | <size> |
| **Word count** | <count> | <count> |
| **Sections** | <count> | <count> |
| **Examples** | <count> | <count> |
| **Complexity** | <simple/medium/complex> | <simple/medium/complex> |

## Similarity Analysis

**Similarity score**: X% similar

**Shared characteristics**:
- Both use similar tool sets
- Both target same domain
- Both follow similar patterns

**Key differences**:
- Different approaches to <aspect>
- Different tool permissions
- Different complexity levels

**Overlap concerns**:
- ⚠️ These agents may have overlapping responsibilities
- 💡 Consider: Could they be merged or clarified?
- 💡 Consider: Clear boundaries between use cases?

## Trade-off Analysis

### Speed vs Capability
- **Faster**: <agent with haiku or simpler>
- **More capable**: <agent with sonnet/opus or complex>
- **Recommendation**: Use <agent> for speed-critical tasks, <agent> for complex tasks

### Security vs Functionality
- **More secure**: <agent with fewer tools>
- **More functional**: <agent with more tools>
- **Recommendation**: Use <agent> for untrusted inputs, <agent> for trusted operations

### Simplicity vs Comprehensiveness
- **Simpler**: <agent with less content>
- **More comprehensive**: <agent with more documentation>
- **Recommendation**: Use <agent> for quick tasks, <agent> for learning/complex work

## Recommendations

### If you want:
- ✅ **Speed**: Use <faster agent>
- ✅ **Security**: Use <more restrictive agent>
- ✅ **Capability**: Use <more capable agent>
- ✅ **Simplicity**: Use <simpler agent>
- ✅ **Comprehensive guidance**: Use <more documented agent>

### Consider merging if:
- [ ] Very high similarity (>80%)
- [ ] Overlapping responsibilities
- [ ] Same tool sets and model
- [ ] Could be single agent with modes

### Consider specializing if:
- [ ] Similar but serve different use cases
- [ ] Different security requirements
- [ ] Different performance needs
- [ ] Different user skill levels

## Usage Examples

### Example scenario 1: <use case>
**Better choice**: <agent> because <reason>

### Example scenario 2: <use case>
**Better choice**: <agent> because <reason>

### Example scenario 3: <use case>
**Either works**: <explanation>

## Next Steps

Based on this comparison:

1. **Choose the right agent** for your current task
2. **Update descriptions** if overlap is unclear
3. **Consider merging** if too similar
4. **Enhance the weaker one** using `/agent-builder:agents:enhance`
5. **Audit both** using `/agent-builder:agents:audit`

## Related Commands

- `/agent-builder:agents:enhance [name]` - Improve either agent
- `/agent-builder:agents:update [name]` - Update agent configuration
- `/agent-builder:agents:audit` - Audit all agents including these two

---

**Purpose**: This command helps you understand the differences between two agents and choose the right one for your task. It's useful when you have multiple agents that seem similar or when deciding which to enhance.
