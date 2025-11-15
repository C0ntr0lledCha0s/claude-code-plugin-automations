---
description: Compare multiple approaches, technologies, or implementations with trade-off analysis and recommendations
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
argument-hint: "[option A] vs [option B] (for context)"
model: claude-sonnet-4-5
---

# Compare Command

Systematically compare multiple approaches, technologies, tools, or implementations to help make informed decisions based on trade-offs and context.

## Arguments

- **`$ARGUMENTS`**: The comparison query (e.g., "REST vs GraphQL", "Redux vs Zustand for React", "SQL vs NoSQL for e-commerce")

## Workflow

When this command is invoked with `/compare <option A> vs <option B> [context]`:

1. **Parse Comparison**: Extract options to compare and context
2. **Research Each Option**: Gather comprehensive information about each
3. **Define Comparison Criteria**: Identify relevant evaluation dimensions
4. **Analyze Trade-offs**: Evaluate pros/cons for each option
5. **Consider Context**: Apply project-specific constraints and requirements
6. **Create Comparison Matrix**: Structure findings in clear tables
7. **Provide Recommendation**: Suggest best fit with clear rationale

## Comparison Dimensions

### Technical Factors
- Performance characteristics
- Scalability potential
- Complexity level
- Flexibility and extensibility
- Type safety and tooling
- Error handling approaches

### Practical Factors
- Learning curve
- Documentation quality
- Community support and ecosystem
- Maintenance and updates
- Migration difficulty
- Development speed

### Project Fit
- Team expertise
- Project size and scale
- Timeline constraints
- Budget considerations
- Long-term maintainability
- Integration with existing stack

## Examples

### Example Usage 1: Technology Comparison
```
/compare REST vs GraphQL for our API
```

Expected behavior:
1. Researches both REST and GraphQL current state (2025)
2. Analyzes project context (checks existing API if present)
3. Provides comprehensive comparison:

   **Comparison: REST vs GraphQL**

   #### Quick Summary
   - **REST**: Best for simple CRUD, public APIs, caching-heavy
   - **GraphQL**: Best for complex data needs, mobile apps, rapid iteration

   #### Detailed Comparison

   | Aspect | REST | GraphQL |
   |--------|------|---------|
   | **Data Fetching** | Multiple endpoints, may over/under-fetch | Single endpoint, request exactly what you need |
   | **Performance** | Can cache with HTTP caching | Requires additional caching layer |
   | **Versioning** | URL versioning (/v1/, /v2/) | Schema evolution, no versioning |
   | **Learning Curve** | Low, familiar to most devs | Medium, requires learning GraphQL concepts |
   | **Tooling** | Mature (Swagger, Postman) | Excellent (GraphiQL, Apollo DevTools) |
   | **Error Handling** | HTTP status codes | Errors in response body with 200 status |
   | **Type Safety** | Requires OpenAPI/Swagger | Built-in with schema |
   | **Mobile-Friendly** | Multiple requests may be needed | Fetch all data in one request |
   | **Real-time** | WebSockets or SSE | Subscriptions built-in |
   | **Complexity** | Low | Higher (schema, resolvers, N+1 problem) |

   #### Pros & Cons

   **REST**
   ✓ Pros:
   - Simple and well-understood
   - Great HTTP caching support
   - Stateless and scalable
   - Mature ecosystem
   - Works well with CDNs
   - Easy to monitor and debug

   ✗ Cons:
   - Over-fetching or under-fetching data
   - Multiple round trips for complex data
   - Versioning can be messy
   - No built-in type system
   - Documentation can become stale

   **GraphQL**
   ✓ Pros:
   - Fetch exactly what you need
   - Single request for complex data
   - Strong typing with schema
   - Self-documenting (introspection)
   - Great for mobile (reduces requests)
   - Rapid frontend iteration

   ✗ Cons:
   - More complex setup
   - Caching is harder
   - N+1 query problem
   - Learning curve for team
   - Potential for expensive queries
   - Rate limiting is more complex

   #### Code Examples

   **REST**
   ```typescript
   // Fetch user and their posts (2 requests)
   const user = await fetch('/api/users/123');
   const posts = await fetch('/api/users/123/posts');
   ```

   **GraphQL**
   ```graphql
   # Fetch user and posts (1 request)
   query {
     user(id: "123") {
       name
       email
       posts {
         title
         content
       }
     }
   }
   ```

   #### When to Choose

   **Choose REST if:**
   - Simple CRUD operations
   - Public API (easier for consumers)
   - Heavy caching requirements
   - Team unfamiliar with GraphQL
   - Microservices architecture
   - Third-party integrations

   **Choose GraphQL if:**
   - Complex, nested data requirements
   - Mobile apps (minimize requests)
   - Rapidly changing frontend needs
   - Multiple clients with different needs
   - Real-time features needed
   - Strong typing is priority

   #### Recommendation for Your Project
   Based on typical API needs:
   - **Start with REST** if building standard CRUD API
   - **Consider GraphQL** if building mobile app or complex dashboard

   **Hybrid Approach**: You can also use both:
   - REST for public API
   - GraphQL for internal/mobile clients

### Example Usage 2: Library Comparison
```
/compare Redux vs Zustand vs Jotai for React state management
```

Expected behavior:
1. Checks current state management in project
2. Researches all three libraries (2025 versions)
3. Provides multi-way comparison:

   **Comparison: Redux vs Zustand vs Jotai**

   #### Quick Summary
   - **Redux**: Best for large apps, complex state, team familiarity
   - **Zustand**: Best for simplicity, TypeScript, modern React
   - **Jotai**: Best for atomic state, fine-grained updates

   #### Comparison Table

   | Feature | Redux | Zustand | Jotai |
   |---------|-------|---------|-------|
   | **Bundle Size** | ~13KB (with RTK) | ~1KB | ~3KB |
   | **Boilerplate** | High | Low | Low |
   | **Learning Curve** | Steep | Gentle | Medium |
   | **TypeScript** | Good (RTK) | Excellent | Excellent |
   | **DevTools** | Excellent | Good | Good |
   | **Middleware** | Extensive | Simple | Flexible |
   | **Performance** | Good | Excellent | Excellent |
   | **Async** | Redux Thunk/Saga | Built-in | Built-in |
   | **Atomic Updates** | No | No | Yes |

   #### Code Comparison

   **Redux (with Redux Toolkit)**
   ```typescript
   // Store setup
   const counterSlice = createSlice({
     name: 'counter',
     initialState: { value: 0 },
     reducers: {
       increment: (state) => { state.value += 1; },
     },
   });

   const store = configureStore({
     reducer: { counter: counterSlice.reducer },
   });

   // Component usage
   const count = useSelector((state) => state.counter.value);
   const dispatch = useDispatch();
   dispatch(counterSlice.actions.increment());
   ```

   **Zustand**
   ```typescript
   // Store setup
   const useStore = create((set) => ({
     count: 0,
     increment: () => set((state) => ({ count: state.count + 1 })),
   }));

   // Component usage (that's it!)
   const { count, increment } = useStore();
   ```

   **Jotai**
   ```typescript
   // Atom definition
   const countAtom = atom(0);

   // Component usage
   const [count, setCount] = useAtom(countAtom);
   setCount(count + 1);
   ```

   #### When to Choose

   **Choose Redux if:**
   - Large, complex application
   - Team already knows Redux
   - Need extensive middleware ecosystem
   - Time-travel debugging is valuable
   - Multiple sources of state updates

   **Choose Zustand if:**
   - Want simplicity over features
   - TypeScript project
   - Modern React (hooks-based)
   - Don't need Redux DevTools complexity
   - Rapid development priority

   **Choose Jotai if:**
   - Atomic state model appeals
   - Need fine-grained updates
   - Want built-in async support
   - Like Recoil but want lighter weight
   - Bottom-up state composition

   #### Recommendation
   **For new projects in 2025**: Start with **Zustand**
   - Simplest API
   - Great TypeScript support
   - Minimal boilerplate
   - Easy to learn and teach

   **Upgrade to Redux if** you outgrow Zustand (rare).

### Example Usage 3: Architecture Comparison
```
/compare monorepo vs polyrepo for our team
```

Expected behavior:
1. Analyzes project context (team size, current setup)
2. Researches both approaches
3. Provides decision framework:

   **Comparison: Monorepo vs Polyrepo**

   #### Overview
   - **Monorepo**: Single repository containing multiple projects/packages
   - **Polyrepo**: Separate repository for each project/package

   #### Comparison Matrix

   | Aspect | Monorepo | Polyrepo |
   |--------|----------|----------|
   | **Code Sharing** | Easy, direct imports | Requires publishing packages |
   | **Atomic Changes** | Yes, change multiple packages in one commit | No, requires multiple PRs |
   | **Versioning** | Simplified | Complex (each repo versioned separately) |
   | **CI/CD** | Complex, requires smart caching | Simple, per-repo |
   | **Build Times** | Slower (more code) | Faster (isolated) |
   | **Tooling** | Requires monorepo tools (Nx, Turborepo) | Standard git workflows |
   | **Onboarding** | One clone, see everything | Clone multiple repos |
   | **Access Control** | Coarse-grained | Fine-grained per repo |
   | **Scaling** | Can get large | Naturally bounded |

   #### Pros & Cons

   **Monorepo**
   ✓ Pros:
   - Simplified dependency management
   - Atomic refactoring across projects
   - Consistent tooling and configs
   - Easier code discovery and reuse
   - Single source of truth

   ✗ Cons:
   - Large repository size
   - Slower git operations
   - Requires monorepo tooling
   - CI/CD complexity
   - All or nothing access

   **Polyrepo**
   ✓ Pros:
   - Smaller, focused repositories
   - Fast git operations
   - Independent deployment
   - Clear ownership boundaries
   - Granular access control

   ✗ Cons:
   - Cross-repo changes are painful
   - Dependency hell with versions
   - Duplicated configs and tooling
   - Harder to discover code
   - More maintenance overhead

   #### Tooling

   **Monorepo Tools**:
   - Nx: Full-featured, smart caching
   - Turborepo: Fast, simple, growing
   - Lerna: Classic, still used
   - pnpm workspaces: Built-in, efficient

   **Polyrepo Tools**:
   - Standard git
   - Package registries (npm, private)
   - CI/CD per repo

   #### Decision Criteria

   **Choose Monorepo if:**
   - High code interdependence
   - Frequent cross-project changes
   - Small to medium team (<50 devs)
   - Want consistent tooling
   - Rapid iteration on shared code

   **Choose Polyrepo if:**
   - Independent products/services
   - Large organization (>50 devs)
   - Need strict access control
   - Projects on different cadences
   - Prefer simplicity over features

   #### Recommendation for Your Team
   [Based on detected team size and project structure]

   **For small teams (2-10 devs)**: Monorepo
   - Easier collaboration
   - Simpler mental model
   - Tools are mature now

   **For large organizations**: Polyrepo or Monorepo per team
   - Scale challenges are real
   - Access control matters
   - But consider monorepo per team/domain

### Example Usage 4: Pattern Comparison
```
/compare class components vs functional components in React
```

Expected behavior:
Provides historical context and current best practices with migration guidance.

## Output Format

```markdown
# Comparison: [Option A] vs [Option B] [vs Option C]

## Quick Summary
[One-sentence summary of when to use each option]

## Overview
**[Option A]**: [Brief description]
**[Option B]**: [Brief description]

## Detailed Comparison

| Aspect | Option A | Option B |
|--------|----------|----------|
| [Criterion 1] | [Assessment] | [Assessment] |
| [Criterion 2] | [Assessment] | [Assessment] |

## Pros & Cons

### Option A
✓ **Pros**:
- [Pro 1]
- [Pro 2]

✗ **Cons**:
- [Con 1]
- [Con 2]

### Option B
✓ **Pros**:
- [Pro 1]
- [Pro 2]

✗ **Cons**:
- [Con 1]
- [Con 2]

## Code Examples
[Side-by-side code showing both approaches]

## When to Choose

**Choose [Option A] if:**
- [Criterion]
- [Criterion]

**Choose [Option B] if:**
- [Criterion]
- [Criterion]

## Recommendation
[Context-specific recommendation with rationale]

## Migration Path (if applicable)
[How to move from one to the other]

## Resources
- [Link to docs for Option A]
- [Link to docs for Option B]
```

## Important Notes

- Research current state of both options (2025)
- Be objective—present facts, not opinions
- Consider project-specific context
- Provide concrete examples
- Note that "it depends" is often the honest answer
- Explain trade-offs clearly
- Cite sources for claims

## Error Handling

### If comparison query is unclear:
```
Error: Unclear comparison.

Usage: /compare <option A> vs <option B> [context]

Examples:
  /compare REST vs GraphQL
  /compare Redux vs Zustand for React
  /compare SQL vs NoSQL for e-commerce app
  /compare microservices vs monolith
```

### If options are too similar:
Note similarities and highlight subtle differences.

### If asking to compare incomparable things:
Explain why comparison doesn't make sense and suggest alternatives.

## Advanced Usage

### Multi-way comparison:
```
/compare Redux vs Zustand vs Jotai vs Context API
```
Compares multiple options (up to 4-5 recommended).

### Context-specific:
```
/compare PostgreSQL vs MongoDB for real-time chat app
```
Focuses comparison on specific use case.

### Current implementation vs alternatives:
```
/compare our current auth approach vs OAuth 2.0
```
Evaluates existing implementation against alternatives.

---

**Pro Tip**: Use /compare when deciding between options, /best-practice to learn the standard approach, and /research for deep dive into your choice.
