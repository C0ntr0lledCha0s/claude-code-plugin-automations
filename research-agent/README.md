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

## Templates & Resources

### Investigation Template
A comprehensive template for documenting investigation findings is available at:
`skills/investigating-codebases/assets/investigation-template.md`

This template provides a structured format for capturing:
- Component location and file references
- Execution flow analysis
- Key components and their roles
- Data flow diagrams
- Pattern observations
- Security and performance notes
- Related components and dependencies
- Next steps for further investigation

**Usage**: Copy and fill out the template when conducting thorough investigations to ensure consistent, complete documentation.

### Additional Resources
- **Scripts**: Automation tools in `skills/*/scripts/` for mapping structure, finding entry points, and pattern detection
- **References**: Best practice guides, pattern catalogs, and checklists in `skills/*/references/`
- **Assets**: Templates and diagrams in `skills/*/assets/`

## Citation System

The Research Agent includes a comprehensive citation system to ensure research outputs are well-sourced, traceable, and credible.

### Citation Guide

A complete guide for citing sources in research outputs is available at [assets/citation-guide.md](assets/citation-guide.md).

**Supported Citation Types**:
1. **Code File References**: `` `src/auth/login.ts:42-88` `` (with line numbers)
2. **Web Resources**: Numbered citations `[1]` with URLs in References section
3. **Package Documentation**: Package name, version, and docs URL
4. **Code Examples**: Code blocks with source citations
5. **Design Patterns**: Pattern name + source reference
6. **API Endpoints**: HTTP method + path + implementation reference

**Example**:
```markdown
The authentication logic uses JWT tokens [1] implemented in `src/auth/jwt.ts:42`.

References:
[1] JWT Best Practices - https://datatracker.ietf.org/doc/html/rfc8725
```

### Citation Template

Use the [citation-template.md](assets/citation-template.md) as a starting point for creating well-cited research outputs. The template includes:
- Structured sections for findings
- File reference tables
- Best practices comparison
- Pattern identification
- Dependency tracking
- Complete references section

### Citation Analysis

Extract and analyze citations from research outputs:

```bash
python3 scripts/extract-citations.py research-output.md
```

**Features**:
- Extract all file, web, and package citations
- Analyze citation quality (0-100 score)
- Validate file references exist
- Identify code blocks with/without sources
- Count unique domains
- Generate citation report

**Example Output**:
```
Citation Analysis Report
========================================
Total Citations: 23
Quality Score: 87.5/100

File References (12):
  • `src/auth/login.ts:42-88`
  • `src/middleware/csrf.ts:15-67`
  ...

Web Citations (8):
  [1] OWASP Authentication...
      https://owasp.org/...
  ...

✅ Citations look good!
```

## Validation & Quality Assurance

The Research Agent includes comprehensive validation scripts to ensure research outputs meet quality standards. These scripts help verify completeness, accuracy, and proper evidence.

### Validation Scripts

Located in `scripts/`, these tools validate research output:

#### 1. `validate-research.py` - Quality Standards
Checks research output against 7 quality criteria:
- ✓ Has summary/overview section
- ✓ Includes file references with line numbers
- ✓ Contains evidence or examples
- ✓ Provides recommendations
- ✓ Has structured sections (minimum 3)
- ✓ Sufficient content length (200+ characters)
- ✓ Includes citations/sources

**Usage**:
```bash
python3 scripts/validate-research.py output/investigation-results.md
```

#### 2. `check-evidence.py` - File Reference Validation
Validates that all file references in the research output actually exist in the codebase and that line numbers are within bounds.

**Usage**:
```bash
python3 scripts/check-evidence.py output/investigation-results.md --codebase-dir /path/to/project
```

**Example Output**:
```
Found 15 file reference(s)
  ✓ `src/auth/login.ts:42` - Valid
  ✓ `src/middleware.ts:25-67` - Valid
  ✗ `src/utils/helper.ts:100` - Line range 100 exceeds file length (85 lines)
```

#### 3. `assess-completeness.py` - Completeness Assessment
Comprehensive assessment of research thoroughness with scoring across 7 dimensions:
- Section coverage (expected sections present)
- Evidence depth (file references, code blocks)
- Explanation quality (word count, detail level)
- Structural elements (organization, headings)
- Actionability (recommendations, next steps)
- Breadth vs depth balance
- Technical depth (specifics, terminology)

**Usage**:
```bash
python3 scripts/assess-completeness.py output/investigation-results.md --threshold 70
```

**Example Output**:
```
Overall Completeness: 85.7% - Excellent ✅

Detailed Metrics:
  • Section Coverage: 100%
  • Evidence Items: 12 (Strong: Yes)
  • Word Count: 1,847 (Sufficient: Yes)
  • Organization: Well-structured
  • Actionability: Yes
  • Topics Covered: 8
  • Avg Section Length: 231 words
  • Balance: Good
  • Technical Depth: Yes
```

#### 4. `validate-all.sh` - Comprehensive Validation
Master validation script that runs all three validators in sequence with formatted output.

**Usage**:
```bash
bash scripts/validate-all.sh output/investigation-results.md /path/to/project 80
```

**Arguments**:
- `research-output-file`: Path to research markdown file
- `codebase-dir`: Root directory of codebase (default: current directory)
- `threshold`: Minimum completeness percentage (default: 70)

**Example Output**:
```
╔════════════════════════════════════════════════════════════╗
║         Research Agent - Comprehensive Validation          ║
╚════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test 1: Quality Standards
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Quality validation passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test 2: Evidence & File References
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Evidence validation passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Test 3: Completeness Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Completeness assessment passed

✅ All validations passed!
```

### Validation Workflow

**Recommended workflow** for validating research outputs:

1. **During Research**: Keep validation criteria in mind while investigating
2. **After Research**: Run comprehensive validation:
   ```bash
   bash scripts/validate-all.sh my-research.md . 75
   ```
3. **Review Results**: Address any failures or warnings
4. **Iterate**: Improve research based on feedback
5. **Final Check**: Re-validate before sharing

### Quality Thresholds

Recommended completeness thresholds by use case:
- **Internal exploration**: 50% (basic completeness)
- **Team documentation**: 70% (good quality)
- **External sharing**: 85% (excellent quality)
- **Publication/training**: 90%+ (comprehensive)

## Research Caching

The Research Agent includes an intelligent caching system to preserve research findings across sessions, build institutional knowledge, and avoid redundant research.

### Why Use Caching?

**Benefits**:
- **Avoid Redundant Research**: Don't re-research the same topics
- **Build Knowledge Base**: Accumulate understanding over time
- **Team Sharing**: Share research findings across team members (optional)
- **Faster Responses**: Reuse existing research when still valid
- **Historical Tracking**: See how understanding evolved

### Cache Structure

```
research-agent/
└── .research-cache/
    ├── investigations/      # Codebase investigations
    ├── best-practices/      # Best practice research
    ├── patterns/            # Pattern analysis
    └── comparisons/         # Technology comparisons
```

### Cache Management

Use `cache-manager.py` to manage cached research:

**List cached research**:
```bash
python3 scripts/cache-manager.py list

# Filter by category
python3 scripts/cache-manager.py list investigations

# Hide expired entries
python3 scripts/cache-manager.py list --hide-expired
```

**Search cache**:
```bash
python3 scripts/cache-manager.py search "authentication"
```

**Show cache entry**:
```bash
python3 scripts/cache-manager.py show jwt-authentication-2025-01-15
```

**Add research to cache**:
```bash
python3 scripts/cache-manager.py add investigations \
  "user authentication system" \
  research-output.md \
  --tags "auth,jwt,middleware"
```

**Cache statistics**:
```bash
python3 scripts/cache-manager.py stats
```

**Example Output**:
```
============================================================
Research Cache Statistics
============================================================

Total entries: 23
  Active: 18
  Expired: 5

By Category:
  investigations: 8
  best-practices: 10
  patterns: 3
  comparisons: 2

Top Tags:
  react: 7
  security: 5
  auth: 4
```

**Clear expired cache**:
```bash
python3 scripts/cache-manager.py clear --expired
```

### Cache Entry Format

Each cached research includes metadata:

```yaml
---
research_type: investigation
topic: user authentication
date: 2025-01-15
expiry: 2025-02-15
codebase_hash: abc123  # Git commit hash
tags: [auth, jwt, security]
related_files:
  - src/auth/middleware.ts
  - src/utils/jwt.ts
---

[Research content here...]
```

### Cache Workflow

**Before Research**:
1. Check for existing research: `search <topic>`
2. Review if found and still valid
3. Decide: use cached or conduct new research

**After Research**:
1. Save research output to file
2. Add to cache with appropriate tags
3. Cache is available for future lookups

### Cache Invalidation

Automatic invalidation when:
- **Time-based**: Older than expiry date (default: 30 days)
- **Code-based**: Referenced files have changed (if codebase_hash provided)
- **Manual**: User requests cache clear

### Complete Guide

For comprehensive caching documentation, see [assets/caching-guide.md](assets/caching-guide.md).

Example cache entry: [.research-cache/investigations/example-jwt-authentication-2025-01-15.md](.research-cache/investigations/example-jwt-authentication-2025-01-15.md)

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
