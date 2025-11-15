# Research Agent Plugin

Intelligent research capabilities for Claude Code, enabling deep investigation of codebases, discovery of best practices, and comprehensive pattern analysis.

## Overview

The Research Agent plugin transforms Claude into a powerful research assistant capable of investigating unfamiliar code, discovering industry best practices, analyzing architectural patterns, and providing evidence-based recommendations. Whether you're exploring a new codebase, evaluating technology choices, or seeking expert guidance, this plugin provides systematic research methodologies and actionable insights.

## Features

### 🔍 Deep Investigation
- Systematically explore unfamiliar codebases
- Trace execution flows and data paths
- Map component relationships and dependencies
- Understand architectural decisions
- Provide comprehensive analysis with file references

### 📚 Best Practice Research
- Look up current industry standards (2025)
- Compare approaches and methodologies
- Get context-specific recommendations
- Access curated best practice guides
- Stay current with evolving standards

### 🎯 Pattern Analysis
- Identify design patterns in code
- Recognize architectural patterns
- Extract naming conventions
- Find repeated code structures
- Spot anti-patterns and suggest improvements

### ⚖️ Comparative Analysis
- Compare technologies and frameworks
- Evaluate trade-offs systematically
- Get decision-making frameworks
- Receive context-aware recommendations
- Access side-by-side code comparisons

## Components

### Agent

#### Investigator
**File**: `agents/investigator.md`

Expert research analyst and investigator with deep expertise in software engineering, architectural patterns, and industry best practices. Conducts thorough, methodical investigations and provides comprehensive, well-researched insights.

**Capabilities**:
- Codebase investigation and mapping
- Best practice research and synthesis
- Pattern analysis and recognition
- Comparative research across implementations
- Architecture analysis and documentation
- Documentation discovery and organization

**Use when**: You need deep investigation, research best practices, analyze patterns, conduct comparative analysis, or understand complex systems.

### Skills

#### 1. Investigating Codebases
**Directory**: `skills/investigating-codebases/`

Systematic investigation techniques for understanding unfamiliar code.

**Auto-activates when**:
- "How does [feature/component] work?"
- "Where is [X] implemented?"
- "Explain the [component] code"
- Exploring new codebases
- Tracing execution flows
- Understanding integration points

**Methodology**:
1. High-level reconnaissance (structure, patterns)
2. Targeted investigation (search, read, analyze)
3. Deep dive analysis (trace flows, understand details)

#### 2. Researching Best Practices
**Directory**: `skills/researching-best-practices/`

Research capabilities for discovering and applying industry best practices.

**Auto-activates when**:
- "What's the best way to..."
- "How should I implement..."
- "Best practices for [topic]"
- Seeking recommendations
- Evaluating approaches
- Security/performance concerns

**Methodology**:
1. Understanding context (domain, constraints, requirements)
2. Research & discovery (codebase, standards, web research)
3. Analysis & recommendation (evaluate, contextualize, recommend)

#### 3. Analyzing Patterns
**Directory**: `skills/analyzing-patterns/`

Pattern recognition for design patterns, architectural patterns, and code organization.

**Auto-activates when**:
- "Find patterns in..."
- "Identify repeated code..."
- "Analyze the architecture..."
- "What design patterns are used..."
- Understanding code organization
- Recognizing structural similarities
- Identifying refactoring opportunities

**Methodology**:
1. Pattern discovery (structural, design, architectural)
2. Pattern analysis (document, evaluate, note variations)
3. Synthesis & reporting (categorize, identify meta-patterns, provide insights)

### Commands

#### `/research <topic>`
**File**: `commands/research.md`

Conduct comprehensive research on any topic with evidence and recommendations.

**Usage**:
```
/research how does authentication work in this app
/research what's the best way to handle API errors in Next.js 2025
/research compare REST vs GraphQL for our use case
/research latest React state management options 2025
```

**Provides**:
- Summary of findings
- Detailed analysis with evidence
- File references and code examples
- Trade-off evaluation
- Context-specific recommendations
- Additional resources and next steps

#### `/investigate <target>`
**File**: `commands/investigate.md`

Deep-dive investigation of code, features, or components.

**Usage**:
```
/investigate user authentication
/investigate ErrorBoundary component
/investigate /api/users endpoint
/investigate state management approach
```

**Provides**:
- Location and structure mapping
- Execution flow tracing
- Implementation details
- Component relationships
- Pattern analysis
- Related components
- Usage examples

#### `/best-practice <topic>`
**File**: `commands/best-practice.md`

Look up current best practices for technologies, patterns, or approaches.

**Usage**:
```
/best-practice React hooks
/best-practice API error handling
/best-practice PostgreSQL indexing
/best-practice Next.js project structure
```

**Provides**:
- Current standards (2025)
- Do's and don'ts
- Code examples
- Common pitfalls
- Implementation checklist
- Comparison with current implementation
- Migration path if applicable

#### `/compare <A> vs <B>`
**File**: `commands/compare.md`

Compare multiple approaches, technologies, or implementations.

**Usage**:
```
/compare REST vs GraphQL
/compare Redux vs Zustand for React
/compare SQL vs NoSQL for e-commerce
/compare monorepo vs polyrepo
```

**Provides**:
- Detailed comparison matrix
- Pros and cons for each option
- When to choose each
- Code examples side-by-side
- Context-specific recommendations
- Migration considerations

## Installation

### From Marketplace (when published)
```bash
claude plugin install research-agent
```

### From Local Development
1. Clone this repository
2. Navigate to the repository directory
3. Add to `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "local-plugins": {
      "source": {
        "source": "directory",
        "path": "/path/to/claude-code-plugin-automations"
      }
    }
  },
  "enabledPlugins": {
    "research-agent@local-plugins": true
  }
}
```

## Usage Examples

### Example 1: Understanding Unfamiliar Code
```
User: How does authentication work in this Next.js app?

Claude: [investigating-codebases skill auto-activates]
I'll investigate the authentication system in this Next.js application.

[Searches for auth-related files, reads implementations, traces flows]

Authentication Analysis:

The app uses JWT-based authentication with the following components:

1. **Login Flow** (src/app/api/auth/login/route.ts:15-88)
   - Validates credentials against database
   - Generates JWT token (src/lib/jwt.ts:42)
   - Sets HttpOnly cookie for security

2. **Auth Middleware** (src/middleware.ts:25-67)
   - Validates JWT on protected routes
   - Refreshes tokens if needed
   - Redirects to login if invalid

3. **Client Auth Context** (src/contexts/AuthContext.tsx:10-120)
   - Manages client-side auth state
   - Provides login/logout functions
   - Handles token refresh

Security measures:
- HttpOnly cookies prevent XSS
- CSRF tokens on mutations
- Token expiration: 15 minutes
- Refresh token: 7 days

[Full details with file references...]
```

### Example 2: Best Practice Lookup
```
User: /best-practice React Server Components in Next.js 15

Claude: [researching-best-practices skill provides guidance]

Best Practices: React Server Components (Next.js 15, 2025)

Core Principles:
1. Server Components by default
2. Use 'use client' only when needed
3. Compose Server and Client Components properly

[Detailed guide with code examples, do's/don'ts, checklist...]
```

### Example 3: Technology Comparison
```
User: /compare Prisma vs Drizzle for our PostgreSQL project

Claude: [Provides comprehensive comparison]

Comparison: Prisma vs Drizzle

Quick Summary:
- Prisma: Best for rapid development, migrations, type safety
- Drizzle: Best for performance, SQL control, lightweight

[Detailed comparison matrix, code examples, recommendations...]
```

### Example 4: Pattern Analysis
```
User: What design patterns are used in the codebase?

Claude: [analyzing-patterns skill auto-activates]
I'll analyze the codebase for design patterns.

[Searches for pattern indicators, examines implementations]

Design Patterns Found:

1. **Factory Pattern** (src/factories/userFactory.ts:10-35)
   - Creates user objects with different roles
   - Clean separation of construction logic

2. **Observer Pattern** (src/events/eventEmitter.ts:15-88)
   - Event-driven communication between components
   - Pub/sub for UI updates

[Complete pattern analysis with file references...]
```

## Best Practices

### When to Use Each Command

- **`/research`**: Broad questions, multiple sources, comprehensive analysis
- **`/investigate`**: Specific code/feature, detailed execution tracing
- **`/best-practice`**: Quick lookup of current standards
- **`/compare`**: Decision-making between options

### Getting Best Results

1. **Be Specific**: Instead of "research authentication", try "research JWT authentication in Next.js with security best practices"
2. **Provide Context**: Mention your tech stack, constraints, or goals
3. **Combine Commands**: Use `/investigate` first, then `/best-practice` to compare
4. **Ask Follow-ups**: Research is iterative—ask for clarification or deeper dives

## Contributing

This plugin is part of the [claude-code-plugin-automations](https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations) marketplace repository. Contributions are welcome!

### Adding Resources
Skills can reference additional resources in their directories:
- `skills/*/scripts/`: Helper scripts for analysis
- `skills/*/references/`: Curated guides and references
- `skills/*/assets/`: Templates and tools

### Improving Research Quality
- Add more comprehensive best practice references
- Expand pattern catalogs
- Include more code examples
- Add industry-specific research guides

## Technical Details

### Model Usage
- **Agent**: Sonnet (comprehensive analysis capabilities)
- **Skills**: Auto-activate based on user questions
- **Commands**: Sonnet for research depth

### Tools Available
- `Read`: Read files and analyze code
- `Grep`: Search for patterns and keywords
- `Glob`: Find files by pattern
- `WebSearch`: Current information (2025)
- `WebFetch`: Access documentation
- `Task`: Delegate complex investigations

### Progressive Disclosure
Skills use `{baseDir}` to reference resources, loading them only when needed for efficient context usage.

## License

MIT License - See [LICENSE](../LICENSE) for details.

## Support

For issues, questions, or contributions:
- **Repository**: [claude-code-plugin-automations](https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations)
- **Issues**: [GitHub Issues](https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations/issues)

---

**Research smarter, not harder.** Let the Research Agent help you understand code, discover best practices, and make informed technical decisions.
