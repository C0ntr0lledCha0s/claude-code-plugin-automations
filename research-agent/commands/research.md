---
description: Conduct comprehensive research on a topic, technology, or question with evidence and recommendations
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch, Task
argument-hint: "[research topic or question]"
model: claude-sonnet-4-5
---

# Research Command

Conduct thorough research on any topic, answering questions with comprehensive analysis, evidence, and actionable insights.

## Arguments

- **`$ARGUMENTS`**: The research question or topic to investigate (e.g., "authentication best practices for React 2025", "how does error handling work in this codebase")

## Workflow

When this command is invoked with `/research <topic>`:

1. **Parse Research Question**: Understand what's being asked and define scope
2. **Determine Research Strategy**: Decide on codebase search, web research, or both
3. **Gather Information**: Systematically collect evidence from all relevant sources
4. **Analyze Findings**: Synthesize information, identify patterns, and draw conclusions
5. **Organize Results**: Structure findings logically with clear sections
6. **Provide Recommendations**: Offer actionable insights or next steps
7. **Cite Sources**: Include file references, line numbers, URLs, and documentation links

## Research Approaches

### Codebase-Focused Research
Used when question is about existing code or implementation:
```
1. Search for relevant files and patterns
2. Read key implementations
3. Trace execution flows
4. Document findings with file references
5. Compare with best practices
```

### Best Practice Research
Used when question asks "how should I..." or "what's the best way...":
```
1. Check existing codebase patterns first
2. Research current industry standards (2025)
3. Compare multiple approaches
4. Evaluate trade-offs
5. Provide context-specific recommendations
```

### Comparative Research
Used when question compares multiple options:
```
1. Research each option thoroughly
2. Create comparison matrix
3. Analyze pros/cons for each
4. Consider project-specific context
5. Recommend based on fit
```

### Investigative Research
Used when question is exploratory:
```
1. Define investigation scope
2. Follow trails of discovery
3. Build comprehensive mental model
4. Document all findings
5. Synthesize insights
```

## Examples

### Example Usage 1: Codebase Investigation
```
/research how does authentication work in this app
```

Expected behavior:
1. Searches for auth-related files (grep, glob)
2. Reads authentication implementations
3. Traces login/logout flows
4. Documents authentication strategy
5. Provides report with file references:
   - Auth middleware: `src/middleware/auth.ts:15-45`
   - Login handler: `src/routes/auth.ts:88-120`
   - Token validation: `src/utils/jwt.ts:30-55`
6. Explains how it all works together
7. Notes security considerations

### Example Usage 2: Best Practice Lookup
```
/research what's the best way to handle API errors in Next.js 2025
```

Expected behavior:
1. Checks current error handling in project
2. Researches Next.js 15 error handling best practices
3. Web searches for current recommendations
4. Compares approaches (error boundaries, API routes, middleware)
5. Provides comparison table
6. Recommends approach with rationale
7. Includes implementation examples
8. Cites official docs and resources

### Example Usage 3: Comparative Analysis
```
/research compare REST vs GraphQL for our use case
```

Expected behavior:
1. Analyzes current project structure and requirements
2. Researches REST and GraphQL characteristics
3. Creates comparison matrix:
   - Feature comparison
   - Performance implications
   - Complexity and learning curve
   - Tooling and ecosystem
   - Team expertise required
4. Evaluates fit for specific context
5. Provides recommendation with justification
6. Includes migration considerations if applicable

### Example Usage 4: Technology Investigation
```
/research latest React state management options 2025
```

Expected behavior:
1. Web searches for current state management solutions
2. Researches major options (Context, Redux, Zustand, Jotai, etc.)
3. Checks what's used in current project (if any)
4. Compares approaches with pros/cons
5. Notes trends and community adoption
6. Recommends based on project size and complexity
7. Provides getting-started resources

## Output Format

Research results are structured as:

```markdown
# Research: [Topic]

## Summary
[One-paragraph overview of findings and key takeaway]

## Research Question
[Restated research question with clarifications]

## Findings

### [Finding Category 1]
[Detailed information with evidence]

Evidence:
- File: `path/to/file.ts:42-67` - [What this shows]
- Documentation: [Link to docs]
- Source: [Where info came from]

### [Finding Category 2]
[Detailed information with evidence]

Evidence:
- Implementation: `src/services/api.ts:88-120`
- Best practice: [Reference to standard]
- Example: [Code snippet or link]

## Analysis

### Key Insights
1. [Insight with supporting evidence]
2. [Insight with supporting evidence]
3. [Insight with supporting evidence]

### Trade-offs
| Aspect | Option A | Option B |
|--------|----------|----------|
| ...    | ...      | ...      |

## Recommendations

### Primary Recommendation
[Main recommendation with clear rationale]

**Why**: [Reasoning]
**How**: [Implementation approach]
**Considerations**: [Important notes]

### Alternative Approaches
1. **[Alternative]**: [When to use this instead]
2. **[Alternative]**: [When to use this instead]

## Implementation Guide (if applicable)
1. [Step-by-step implementation]
2. [Code examples]
3. [Configuration needed]

## Additional Resources
- [Relevant documentation]
- [Tutorial or guide]
- [Related files to explore]

## Next Steps
- [Actionable next step 1]
- [Actionable next step 2]
```

## Important Notes

### Research Quality
- Always cite sources with file paths (path:line) or URLs
- Cross-reference findings for accuracy
- Distinguish between facts and opinions
- Note when information is uncertain or needs verification
- Check currency of information (prefer 2025 sources)

### Context Awareness
- Consider project-specific constraints
- Check existing patterns before recommending changes
- Account for team skill levels
- Balance ideals with pragmatism

### Comprehensiveness
- Cover multiple angles of the question
- Include both current state and recommended state
- Provide examples and evidence
- Offer actionable next steps

### Clarity
- Use clear structure with headings
- Organize logically
- Make findings scannable
- Highlight key takeaways

## Error Handling

### If no research topic provided:
```
Error: No research topic specified.

Usage: /research <topic or question>

Examples:
  /research how does routing work in this app
  /research best practices for TypeScript error handling
  /research compare SQL vs NoSQL for this use case
```

### If topic is too vague:
Ask clarifying questions:
- What specific aspect are you interested in?
- Are you looking at existing code or new implementation?
- What's the context or use case?
- What level of detail do you need?

### If research requires external context:
Note what information would be helpful:
- Project requirements or constraints
- Technology stack details
- Performance/scale requirements
- Team skill levels

## Special Capabilities

### Multi-Source Research
- Codebase files and patterns (Grep, Glob, Read)
- Web search for current information (WebSearch)
- Documentation and guides (WebFetch)
- Task delegation for complex investigations (Task)

### Adaptive Depth
- Quick overviews for simple questions
- Deep dives for complex topics
- Appropriate level based on question complexity

### Evidence-Based
- Every claim backed by evidence
- File references with line numbers
- Links to authoritative sources
- Code examples demonstrating points

---

**Pro Tip**: Be specific in your research questions for better results. Instead of "research authentication", try "research JWT authentication implementation in src/auth/ and compare with OAuth best practices 2025".
