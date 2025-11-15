---
description: Deep-dive investigation of code, features, or components with execution tracing and detailed analysis
allowed-tools: Read, Grep, Glob, Task
argument-hint: "[feature/component to investigate]"
model: claude-sonnet-4-5
---

# Investigate Command

Perform deep investigation of code, features, or components to understand how they work, where they're implemented, and how they fit into the larger system.

## Arguments

- **`$ARGUMENTS`**: The feature, component, or code element to investigate (e.g., "user authentication", "payment processing", "ErrorBoundary component")

## Workflow

When this command is invoked with `/investigate <target>`:

1. **Define Investigation Scope**: Clarify what to investigate and depth needed
2. **Locate Relevant Code**: Use Grep and Glob to find all related files
3. **Map Structure**: Understand how components are organized
4. **Trace Execution**: Follow code paths and data flows
5. **Analyze Implementation**: Understand algorithms, patterns, and decisions
6. **Document Findings**: Create comprehensive report with file references
7. **Identify Related Components**: Note dependencies and integration points

## Investigation Strategies

### Feature Investigation
For investigating complete features:
```
1. Find entry points (routes, commands, UI triggers)
2. Trace through handlers/controllers
3. Follow to business logic/services
4. Track data layer interactions
5. Note UI/presentation components
6. Map the complete flow
```

### Component Investigation
For specific components or modules:
```
1. Locate component definition
2. Read implementation details
3. Find where it's used (imports)
4. Understand props/API
5. Check related components
6. Note patterns and conventions
```

### System Investigation
For understanding subsystems:
```
1. Map directory structure
2. Identify main modules
3. Trace component relationships
4. Understand data flows
5. Document architecture
6. Note design patterns
```

## Examples

### Example Usage 1: Feature Investigation
```
/investigate user authentication
```

Expected behavior:
1. Searches for auth-related files:
   ```bash
   grep -r "auth" --include="*.ts"
   glob "**/*auth*"
   ```
2. Identifies key components:
   - Login form: `src/components/LoginForm.tsx`
   - Auth context: `src/contexts/AuthContext.tsx`
   - Auth middleware: `src/middleware/auth.ts`
   - API handlers: `src/api/auth/login.ts`
   - Token utils: `src/utils/jwt.ts`

3. Traces authentication flow:
   ```
   LoginForm submission
   → POST /api/auth/login
   → Validate credentials (src/api/auth/login.ts:25)
   → Generate JWT (src/utils/jwt.ts:42)
   → Set cookie (src/api/auth/login.ts:55)
   → Update auth context (src/contexts/AuthContext.tsx:78)
   → Redirect to dashboard
   ```

4. Provides detailed report:
   - How authentication works
   - File locations with line numbers
   - Security measures in place
   - Session management approach
   - Related components and utilities

### Example Usage 2: Component Investigation
```
/investigate ErrorBoundary
```

Expected behavior:
1. Locates component:
   - Definition: `src/components/ErrorBoundary.tsx:1-89`

2. Reads implementation:
   - Class component using React error boundary
   - Catches errors in children
   - Displays fallback UI
   - Logs errors to service

3. Finds usage:
   ```bash
   grep -r "ErrorBoundary" --include="*.tsx"
   ```
   - App.tsx wraps entire app
   - Some route components have nested boundaries

4. Analyzes pattern:
   - React error boundary pattern
   - Graceful degradation
   - Error reporting integration

5. Provides summary:
   - What it does
   - How it's implemented
   - Where it's used
   - Related error handling patterns

### Example Usage 3: API Investigation
```
/investigate /api/users endpoint
```

Expected behavior:
1. Finds endpoint definition:
   ```bash
   grep -r "/api/users" --include="*.ts"
   grep -r "router.*users" --include="*.ts"
   ```

2. Locates handler:
   - Route: `src/api/routes.ts:45`
   - Controller: `src/api/users/controller.ts:15-88`
   - Service: `src/services/userService.ts:120-165`
   - Repository: `src/repositories/userRepository.ts:55-90`

3. Traces request flow:
   ```
   GET /api/users/:id
   → Auth middleware check (middleware/auth.ts:30)
   → Route handler (api/routes.ts:45)
   → User controller (api/users/controller.ts:25)
   → User service (services/userService.ts:130)
   → User repository (repositories/userRepository.ts:60)
   → Database query
   → Response formatting
   ```

4. Documents:
   - Endpoint purpose and behavior
   - Request/response format
   - Authentication/authorization
   - Error handling
   - Related endpoints

### Example Usage 4: System Investigation
```
/investigate state management
```

Expected behavior:
1. Scans for state management patterns:
   ```bash
   grep -r "useState\|useContext\|Redux\|Zustand" --include="*.ts"
   find . -type d -name "*store*" -o -name "*state*"
   ```

2. Identifies approach:
   - React Context for global state
   - Local state with useState for component state
   - Custom hooks for shared logic

3. Maps state structure:
   - AuthContext: `src/contexts/AuthContext.tsx`
   - ThemeContext: `src/contexts/ThemeContext.tsx`
   - User state: Local in components
   - Form state: react-hook-form

4. Analyzes patterns:
   - Context providers in App.tsx
   - Custom hooks for context consumption
   - State co-location where possible

5. Provides architectural overview:
   - State management strategy
   - When each approach is used
   - Benefits and trade-offs
   - Consistency assessment

## Output Format

Investigation reports are structured as:

```markdown
# Investigation: [Target]

## Summary
[Quick overview of what was found and key characteristics]

## Location

### Primary Files
- `path/to/main.ts:10-120` - [Role]
- `path/to/helper.ts:45-78` - [Role]

### Related Files
- `path/to/related.ts` - [How it relates]
- `path/to/another.ts` - [How it relates]

## How It Works

### Overview
[High-level explanation of functionality]

### Execution Flow
1. **[Step 1]** (`file.ts:42`)
   - [What happens]
   - [Key logic]

2. **[Step 2]** (`file.ts:88`)
   - [What happens]
   - [Key logic]

3. **[Step 3]** (`file.ts:120`)
   - [What happens]
   - [Key logic]

### Data Flow
```
[Input] → [Transformation 1] → [Transformation 2] → [Output]
```

## Implementation Details

### Key Components
1. **[Component Name]** (`path:line`)
   - Purpose: [What it does]
   - Responsibilities: [What it handles]
   - Dependencies: [What it uses]

### Patterns Used
- [Pattern name]: [How it's applied]
- [Pattern name]: [How it's applied]

### Notable Code
```language
// path/to/file.ts:42-55
[Interesting code snippet with explanation]
```

## Architecture

### Component Relationships
```
[Component A] → uses → [Component B]
[Component B] → calls → [Service]
[Service] → queries → [Repository]
```

### Integration Points
- [System/component it integrates with]: [How]
- [System/component it integrates with]: [How]

## Analysis

### Strengths
- [What's well done]
- [Good patterns observed]

### Considerations
- [Potential improvements]
- [Edge cases to note]
- [Complexity areas]

### Security/Performance Notes
- [Relevant security considerations]
- [Performance implications]

## Related Components

### Dependencies
- [Component/module]: [Why it's needed]

### Dependents
- [What uses this]: [How they use it]

## Usage Examples

### Example 1: [Common usage]
```language
// File: path/to/usage.ts:20
[Code showing how it's used]
```

### Example 2: [Another usage]
```language
// File: path/to/another-usage.ts:15
[Code showing different usage]
```

## Next Steps

For further investigation:
- [ ] Explore [related area]
- [ ] Trace [specific flow]
- [ ] Analyze [related component]
- [ ] Review [documentation]
```

## Important Notes

### Investigation Depth
- Adapt depth to complexity of target
- Start with overview, go deeper as needed
- Balance thoroughness with actionability

### Evidence & References
- Always include file paths with line numbers
- Show code snippets for clarity
- Reference related components
- Note where code is used

### Clarity & Organization
- Use clear headings and structure
- Make findings scannable
- Include diagrams/flows when helpful
- Separate what from why

### Context & Implications
- Explain not just what code does, but why
- Note design decisions and trade-offs
- Identify patterns and conventions
- Connect to broader system architecture

## Advanced Usage

### Investigate Multiple Related Features
```
/investigate user management and permissions
```
Investigates both user management and permission system and their interactions.

### Investigate with Specific Focus
```
/investigate payment processing security measures
```
Focuses investigation on security aspects specifically.

### Investigate Implementation Approach
```
/investigate how caching is implemented
```
Looks for caching patterns across the codebase.

## Error Handling

### If no target provided:
```
Error: No investigation target specified.

Usage: /investigate <feature/component/code>

Examples:
  /investigate user authentication
  /investigate ErrorBoundary component
  /investigate /api/users endpoint
  /investigate state management approach
```

### If target not found:
Report what was searched and suggest alternatives:
```
Investigation: [target]

No direct matches found for "[target]".

Searched:
- Files matching pattern: [pattern]
- Code containing: [search terms]

Suggestions:
- Did you mean [similar feature]?
- Try searching for [alternative terms]?
- Check [directory] for related code?
```

### If target is ambiguous:
Ask for clarification:
```
Multiple matches found for "[target]":

1. [Option 1 with location]
2. [Option 2 with location]
3. [Option 3 with location]

Which would you like to investigate?
Or use /investigate <more specific target>
```

## Tips for Effective Investigation

1. **Be Specific**: Instead of "investigate API", try "investigate /api/users CRUD endpoints"
2. **Start Broad**: Get overview first, then dive into specifics
3. **Follow Trails**: Let initial findings guide deeper investigation
4. **Cross-Reference**: Check multiple files to understand complete picture
5. **Note Patterns**: Identify conventions and patterns as you investigate

---

**Pro Tip**: Combine with /research for comprehensive understanding. First /investigate to see how something works, then /research to compare with best practices.
