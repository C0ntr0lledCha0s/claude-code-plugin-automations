---
description: Analyze and suggest AI-powered improvements for an existing agent
allowed-tools: Read, Grep, Glob, Bash
argument-hint: [agent-name]
model: claude-sonnet-4-5
---

# Enhance Agent with AI-Powered Suggestions

Analyze and enhance the agent named: **$1**

## Your Task

Perform deep analysis and provide actionable improvement suggestions for an existing agent.

### 1. **Locate and Load Agent**
- Find the agent file (same logic as update command)
- Read the complete agent definition
- Parse structure and content

### 2. **Run Comprehensive Analysis**

Analyze the agent across multiple dimensions:

#### A. **Schema Compliance**
- Validate YAML frontmatter
- Check required fields present
- Verify optional fields if used
- Validate naming conventions
- Check description length and clarity

#### B. **Tool Permissions Audit**
- Are tools minimal and necessary?
- Any over-permissioned tools? (unnecessary Bash, Write)
- Any under-permissioned tools? (missing needed tools)
- Security implications of current tool set
- Suggest optimal tool configuration

#### C. **Model Selection**
- Is current model appropriate for task complexity?
- Could use faster/cheaper model? (haiku instead of sonnet)
- Need more capable model? (opus for complex reasoning)
- Cost/performance trade-off analysis

#### D. **Content Quality**
- **Role definition**: Clear and specific?
- **Capabilities**: Well-documented?
- **Workflow**: Step-by-step and actionable?
- **Examples**: Present and helpful?
- **Best practices**: Comprehensive?
- **Tone and clarity**: Professional and clear?

#### E. **Best Practices Alignment**
- Follows agent-builder skill guidelines?
- Uses current patterns and conventions?
- Security best practices applied?
- User experience considerations?
- Error handling present?

#### F. **Prompt Engineering**
- Clear instructions and structure?
- Good use of headings and sections?
- Examples and templates provided?
- Edge cases handled?
- Actionable and unambiguous?

### 3. **Generate Enhancement Report**

Present findings in structured format:

```markdown
# Enhancement Analysis: <agent-name>

## Overall Score: X/10

## Critical Issues (Must Fix) 🔴
- [Issue 1]: Description and impact
  **Suggestion**: Concrete fix
  **Priority**: Critical

## Important Improvements (Should Fix) 🟡
- [Issue 1]: Description and benefit
  **Suggestion**: Concrete improvement
  **Priority**: High

## Optional Enhancements (Nice to Have) 🟢
- [Enhancement 1]: Description and benefit
  **Suggestion**: Optional improvement
  **Priority**: Low

## Strengths ✅
- What the agent does well
- Patterns to maintain

## Detailed Analysis

### Schema & Structure
- [Analysis of YAML frontmatter]
- [Recommendations]

### Tool Permissions
Current: <tools>
Recommended: <suggested tools>
Rationale: <why these changes>

### Model Selection
Current: <model>
Recommended: <suggested model>
Rationale: <trade-off analysis>

### Content Quality
[Section-by-section analysis]

### Security Audit
[Security findings and recommendations]

### Prompt Engineering
[Clarity, structure, actionability analysis]

## Suggested Updates

### Quick Wins (Easy, High Impact)
1. [Suggestion 1]
2. [Suggestion 2]

### Content Improvements
1. [Suggestion 1]
2. [Suggestion 2]

### Advanced Enhancements
1. [Suggestion 1]
2. [Suggestion 2]

## Next Steps

1. Review suggestions and prioritize
2. Run `/agent-builder:agents:update <name>` to apply changes
3. Test agent after improvements
4. Re-run enhance to validate improvements

## Apply Automatically?

Would you like to automatically apply the quick wins? (y/n)
```

### 4. **Optional: Auto-Apply Quick Wins**

If user agrees, automatically apply:
- Fix obvious issues (typos, formatting)
- Optimize tool permissions (remove unnecessary)
- Add missing required sections
- Improve description clarity
- Add security validations

Then show diff and confirm before saving.

### 5. **Script Integration**

If available, run:
```bash
python3 agent-builder/skills/building-agents/scripts/enhance-agent.py <agent-path>
```

Parse and present results in user-friendly format.

### 6. **Self-Improvement Integration** (If Available)

Check if self-improvement plugin is installed and invoke quality analysis:

```bash
# Check if self-improvement plugin is available
if [ -d "self-improvement/skills/analyzing-component-quality" ]; then
    # Use self-improvement for deeper quality analysis
    /analyze-component <agent-path>
fi
```

**If self-improvement is available:**
- Invoke the `analyzing-component-quality` skill for comprehensive quality scoring
- Get dimension-specific scores (Description Clarity, Tool Permissions, Security, Usability)
- Receive concrete before/after improvement suggestions
- Integration provides automated quality scoring (1-5 scale)

**If self-improvement is NOT available:**
- Continue with agent-builder's built-in analysis
- Show message: "💡 Tip: Install self-improvement plugin for automated quality scoring and deeper analysis"
- Provide enhancement suggestions based on agent-builder heuristics

## Analysis Heuristics

### Tool Permission Analysis
```python
# Too permissive
if has_bash and (is_read_only_task or is_analysis_task):
    suggest: Remove Bash, security risk

if has_write and not explicitly_modifying_files:
    suggest: Remove Write, minimize permissions

# Under-permissioned
if task_needs_file_modification and not has_write_or_edit:
    suggest: Add Write or Edit

if task_needs_web_data and not has_webfetch:
    suggest: Add WebFetch
```

### Model Selection Analysis
```python
# Over-powered
if task_is_simple and model == "opus":
    suggest: Use haiku (10x faster, 30x cheaper)

if task_is_search_or_grep and model == "sonnet":
    suggest: Use haiku

# Under-powered
if task_needs_complex_reasoning and model == "haiku":
    suggest: Use sonnet or opus

if task_is_critical_decision and model != "opus":
    suggest: Consider opus for accuracy
```

### Content Quality Analysis
```python
# Missing sections
if not has_examples:
    suggest: Add concrete examples

if not has_workflow:
    suggest: Add step-by-step workflow

if not has_error_handling:
    suggest: Add error handling section

# Unclear content
if description too_vague:
    suggest: Be more specific about when to invoke

if workflow not_actionable:
    suggest: Add concrete steps
```

## Comparison with Best Practices

Compare agent against reference examples:
- `agent-builder/skills/building-agents/references/agent-examples.md`
- `agent-builder/skills/building-agents/templates/agent-template.md`

Identify gaps and suggest patterns from successful agents.

## Security Scoring

Calculate security score:
- **Tool minimalism**: Fewer unnecessary tools = higher score
- **Input validation**: Validates user input = higher score
- **Command injection prevention**: Proper escaping = higher score
- **Principle of least privilege**: Minimal permissions = higher score

## Usage Examples

### Basic Enhancement
```bash
/agent-builder:agents:enhance code-reviewer
# Gets detailed analysis and suggestions
```

### Enhancement + Auto-Apply
```bash
/agent-builder:agents:enhance code-reviewer
# Review suggestions
> Apply quick wins? y
# Auto-applies safe improvements
```

### Compare Before/After
```bash
/agent-builder:agents:enhance old-agent
# Apply some suggestions
/agent-builder:agents:enhance old-agent
# See improved score
```

## Output Format

Present findings in a way that's:
1. **Actionable**: Specific suggestions, not vague advice
2. **Prioritized**: Critical issues first
3. **Justified**: Explain why each suggestion matters
4. **Balanced**: Show strengths, not just weaknesses
5. **Practical**: Focus on high-impact, low-effort wins

## Integration Points

- **building-agents skill**: Provides best practices knowledge
- **validate-agent.py**: Schema validation
- **enhance-agent.py**: Deep analysis script (if exists)
- **agent-examples.md**: Reference implementations

## Related Commands

- `/agent-builder:agents:update [name]` - Apply suggested improvements
- `/agent-builder:agents:audit` - Audit all agents at once
- `/agent-builder:agents:compare [agent1] [agent2]` - Compare implementations

---

**Philosophy**: This command is a code review for your agent. It provides expert, AI-powered analysis without making changes. Use it before updating to understand what needs improvement.
