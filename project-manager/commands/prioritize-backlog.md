---
description: Analyzes and prioritizes the entire backlog using RICE or other frameworks, updates labels, and reorganizes project boards
allowed-tools: Bash, Read, Write, Grep, Glob, Task
argument-hint: "[framework]"
---

# Prioritize Backlog Command

Comprehensive backlog prioritization that analyzes all open issues, applies prioritization framework (RICE, MoSCoW, WSJF, or Value vs Effort), updates GitHub labels, and reorganizes project boards by priority.

## Arguments

- **`$1`**: Prioritization framework to use (optional, default: "rice")
  - `rice`: Reach × Impact × Confidence / Effort
  - `moscow`: Must/Should/Could/Won't have
  - `wsjf`: Weighted Shortest Job First (SAFe)
  - `value-effort`: Value vs Effort 2x2 matrix
  - `interactive`: Ask user for framework

## Workflow

When this command is invoked with `/project-manager:prioritize-backlog [framework]`:

### Phase 1: Backlog Discovery

1. **Fetch All Open Issues**:
   ```bash
   # Get all open issues across all milestones
   gh issue list --limit 1000 --state open --json number,title,labels,body,milestone,createdAt,updatedAt
   ```

2. **Analyze Current State**:
   - Total open issues
   - Issues with/without estimates
   - Issues with/without priority labels
   - Stale issues (>90 days old)
   - Issues without clear descriptions

3. **Invoke planning-sprints Skill**:
   - Automatically activates for backlog prioritization expertise
   - Provides framework guidance and best practices

### Phase 2: Issue Triage & Classification

4. **Delegate to workflow-orchestrator for Triage**:
   ```markdown
   For each issue lacking classification:
   Task → workflow-orchestrator: "Triage issue #X to classify type, check for duplicates, and identify relationships"
   ```

5. **Group Issues by Type**:
   - Features / Enhancements
   - Bugs / Defects
   - Technical Debt
   - Documentation
   - Infrastructure / DevOps
   - Research / Spikes

6. **Identify Dependencies**:
   - Issues that block other issues
   - Issues that are blocked
   - Related issue clusters

### Phase 3: Prioritization Scoring

7. **Apply Selected Framework**:

   **If RICE (default)**:
   ```markdown
   For each issue:
   - Reach: How many users affected? (0.5-10)
   - Impact: How much value? (0.25-3)
   - Confidence: How sure? (0.5-1.0)
   - Effort: How much work? (0.5-10)
   - Score = (R × I × C) / E

   For items needing research:
   - Delegate to investigator for complexity estimation
   - Delegate to workflow-orchestrator for similar issue analysis
   ```

   **If MoSCoW**:
   ```markdown
   For each issue:
   - Must Have: Critical for release
   - Should Have: Important but not critical
   - Could Have: Nice to have
   - Won't Have: Out of scope
   ```

   **If WSJF**:
   ```markdown
   For each issue:
   - Business Value: 1-10
   - Time Criticality: 1-10
   - Risk/Opportunity: 1-10
   - Job Size: 1-10
   - Score = (BV + TC + RO) / JS
   ```

   **If Value-Effort Matrix**:
   ```markdown
   For each issue:
   - Value: Low/Medium/High
   - Effort: Low/Medium/High
   - Quadrant: Do First/Do Next/Do Later/Avoid
   ```

8. **Rank All Issues**:
   - Sort by calculated score (descending)
   - Group by priority tier:
     - High Priority (top 20%)
     - Medium Priority (middle 50%)
     - Low Priority (bottom 30%)

### Phase 4: Label Management

9. **Ensure Label Taxonomy Exists**:
   - Delegate to workflow-orchestrator:
     ```markdown
     Task → workflow-orchestrator: "Ensure priority label taxonomy exists using /github-workflows:label-sync"
     ```

10. **Apply Priority Labels**:
    - Delegate to workflow-orchestrator:
      ```markdown
      For each issue, apply appropriate labels:
      - priority:high
      - priority:medium
      - priority:low
      ```

11. **Apply Classification Labels**:
    - type:feature
    - type:bug
    - type:tech-debt
    - type:docs
    - etc.

### Phase 5: Board Organization

12. **Update Project Boards**:
    - Delegate to workflow-orchestrator:
      ```markdown
      Task → workflow-orchestrator: "Reorganize backlog column by priority, moving high-priority items to top"
      ```

13. **Identify Issues for Next Sprint**:
    - Top 15-20 highest priority items
    - Ensure they're well-defined (ready for sprint planning)
    - Flag any that need refinement

### Phase 6: Reporting & Documentation

14. **Generate Prioritization Report**:
    ```markdown
    Create .claude-project/backlog-analysis-[date].md with:
    - Total issues analyzed
    - Framework used
    - Priority breakdown
    - Top 20 issues with scores
    - Issues needing refinement
    - Stale issues recommended for closure
    - Dependency highlights
    ```

15. **Create Summary**:
    - Issues by priority (counts and percentages)
    - Top priorities ready for sprint
    - Issues needing estimation or refinement
    - Recommended next actions

## Examples

### Example Usage 1: Default (RICE)
```
/project-manager:prioritize-backlog
```

Expected behavior:
1. Fetches all open issues
2. Applies RICE scoring framework
3. Calculates priority scores
4. Updates GitHub labels
5. Reorganizes board
6. Reports results

Output:
```markdown
✅ Backlog Prioritized (RICE Framework)

📊 Analyzed: 67 open issues

Priority Breakdown:
- 🔴 High Priority: 15 issues (22%)
- 🟡 Medium Priority: 32 issues (48%)
- ⚪ Low Priority: 20 issues (30%)

Top 5 Priorities:
1. #145: API rate limiting (RICE: 9.2)
2. #123: OAuth implementation (RICE: 8.2)
3. #156: Search optimization (RICE: 7.1)
4. #124: Dashboard redesign (RICE: 6.5)
5. #167: Export to CSV (RICE: 5.5)

📋 Ready for Sprint:  12 issues
⚠️  Need Refinement: 8 issues
🗑️  Recommend Closing: 3 stale issues

Labels updated, boards reorganized.
Report: .claude-project/backlog-analysis-2025-03-15.md
```

### Example Usage 2: MoSCoW Method
```
/project-manager:prioritize-backlog moscow
```

Expected behavior:
1. Fetches all open issues
2. Applies MoSCoW classification
3. Categorizes issues into Must/Should/Could/Won't
4. Updates labels accordingly
5. Reports results

Output:
```markdown
✅ Backlog Prioritized (MoSCoW Method)

Must Have (Critical): 12 issues
- #145: API rate limiting
- #123: OAuth implementation
[...]

Should Have (Important): 28 issues
- #156: Search optimization
[...]

Could Have (Nice-to-have): 22 issues
- #189: Dark mode
[...]

Won't Have (Out of scope): 5 issues
- #201: Mobile app (future release)
[...]
```

### Example Usage 3: Interactive
```
/project-manager:prioritize-backlog interactive
```

Expected behavior:
1. Prompts user to choose framework
2. Asks for any custom parameters
3. Applies chosen framework
4. Provides detailed scoring rationale

## Important Notes

### Prerequisites
- GitHub CLI (`gh`) must be installed and authenticated
- Repository must have open issues
- Recommended: Issues should have descriptions for accurate prioritization

### Delegation Points
This command delegates to:
- **planning-sprints skill**: Auto-invokes for prioritization expertise
- **workflow-orchestrator agent**: For issue triage, label management, board organization
- **investigator agent**: (Optional) For complexity estimation of unknowns

### State Changes
- Updates GitHub issue labels (priority:*, type:*)
- Reorganizes project board order
- Creates backlog analysis document
- May recommend closing stale issues (doesn't auto-close)

### Estimation Requirements
For accurate RICE/WSJF scoring:
- Issues ideally should have story point estimates
- If missing, command will use heuristics (title/description length, complexity keywords)
- Recommend running estimation session for top items

### Stale Issue Handling
Issues older than 90 days without activity:
- Flagged in report
- Recommended for review
- Not automatically closed (user decides)

## Interactive Prompts

### Framework Selection (if $1 = "interactive")
```
"Backlog Prioritization - Framework Selection

Choose prioritization framework:
1. RICE - Reach × Impact × Confidence / Effort (best for products)
2. MoSCoW - Must/Should/Could/Won't (best for releases)
3. WSJF - Weighted Shortest Job First (best for SAFe/enterprise)
4. Value-Effort Matrix - 2x2 matrix (best for quick analysis)

Selection [1-4]: [User input]
"
```

### Parameter Customization
```
"RICE Scoring - Parameters

Customize scoring ranges? (y/n) [Default: n]

If yes:
- Reach range [default: 0.5-10]: [User input]
- Impact range [default: 0.25-3]: [User input]
- Confidence range [default: 0.5-1.0]: [User input]
- Effort range [default: 0.5-10]: [User input]
"
```

## Error Handling

### No Open Issues
```
❌ Error: No open issues found.

The backlog appears empty. This command requires open issues to prioritize.

Next steps:
1. Create issues for planned work
2. Import issues from other sources
3. Check repository permissions (may not have access to issues)
```

### Invalid Framework
```
❌ Error: Unknown framework "$1"

Valid frameworks:
- rice (default)
- moscow
- wsjf
- value-effort
- interactive

Usage: /project-manager:prioritize-backlog [framework]
Example: /project-manager:prioritize-backlog rice
```

### Label Permission Issues
```
⚠️  Warning: Unable to update labels (permission denied)

Prioritization analysis complete, but couldn't update GitHub labels.

Options:
1. Run `gh auth refresh -s repo` to grant label permissions
2. Manually apply labels based on report
3. Ask repository admin for label permissions

Report saved: .claude-project/backlog-analysis-[date].md
```

## Output Format

```markdown
✅ Backlog Prioritization Complete!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Analysis Summary:
Framework: [Framework Name]
Total Issues: [X]
Analyzed: [Y] (new), [Z] (re-prioritized)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Priority Distribution:

High Priority ([X] issues, [Y]%):
- Ready for sprint: [Z] issues
- Need refinement: [W] issues

Medium Priority ([X] issues, [Y]%):
- Well-defined: [Z] issues
- Need estimation: [W] issues

Low Priority ([X] issues, [Y]%):
- Future work: [Z] issues
- Candidates for closure: [W] issues

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 Top 10 Priorities:

1. #[num]: [title] - Score: [X]
2. #[num]: [title] - Score: [X]
3. #[num]: [title] - Score: [X]
[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Sprint Planning Ready:
[X] issues are well-defined and ready for sprint planning.

Recommended next sprint candidates:
- #[num]: [title] ([points] pts)
- #[num]: [title] ([points] pts)
[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Issues Needing Attention:

Need Estimation: [X] issues
- #[num]: [title]
[...]

Need Refinement: [X] issues
- #[num]: [title] (missing acceptance criteria)
[...]

Stale (>90 days): [X] issues
- #[num]: [title] (last updated: [date])
[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 Resources:
- Detailed Report: .claude-project/backlog-analysis-[date].md
- Updated Boards: [Project Board URLs]

📝 Next Steps:
1. Review top priorities for sprint planning
2. Refine issues marked as needing attention
3. Consider closing stale issues
4. Run /project-manager:plan-sprint to create sprint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backlog prioritization completed in [X] seconds.
```

## Advanced Features

### Smart Estimation
- For issues without story points:
  - Analyzes description length and complexity keywords
  - Compares to similar previously estimated issues
  - Provides estimated effort for scoring

### Duplicate Detection
- Integrates with github-workflows triaging-issues
- Flags potential duplicates
- Recommends consolidation

### Dependency Awareness
- Prioritizes blocking issues higher
- Groups dependent work together
- Warns if high-priority work is blocked

### Trend Analysis
- If run periodically, tracks priority shifts
- Identifies issues that consistently rank low
- Highlights emerging priorities

### Export Options
- Markdown report (default)
- CSV export for spreadsheet analysis
- JSON export for custom tooling
