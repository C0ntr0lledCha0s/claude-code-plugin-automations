# Implementation Plan: testing-expert Plugin Improvements

**Created**: 2025-11-20  
**Based on**: PLUGIN_REVIEW.md findings  
**Estimated Total Effort**: 4-6 hours

---

## Overview

This plan addresses the critical issues identified in the plugin review, prioritized by impact and dependency order.

---

## Phase 1: Foundation Fixes (30 min)

### 1.1 Version Alignment
**Priority**: High | **Effort**: 5 min

- [ ] Update `plugin.json` version from 1.0.0 to 1.1.0
- [ ] Verify all skills have consistent versions

**Files to modify**:
- `testing-expert/.claude-plugin/plugin.json`

---

### 1.2 Add Capabilities to All Components
**Priority**: High | **Effort**: 15 min

- [ ] Add capabilities to `test-reviewer` agent
- [ ] Add capabilities to `jest-testing` skill
- [ ] Add capabilities to `analyzing-test-quality` skill

**Agent capabilities**:
```yaml
capabilities:
  - test-quality-review
  - coverage-gap-analysis
  - best-practices-enforcement
  - test-architecture-review
  - framework-specific-guidance
```

**jest-testing capabilities**:
```yaml
capabilities:
  - jest-configuration
  - matchers-assertions
  - mocking-strategies
  - snapshot-testing
  - code-coverage
  - react-testing-library
  - async-testing
```

**analyzing-test-quality capabilities**:
```yaml
capabilities:
  - quality-metrics
  - anti-pattern-detection
  - coverage-analysis
  - mutation-testing
  - test-pyramid-balance
  - reliability-assessment
```

---

### 1.3 Update Agent Tools
**Priority**: Medium | **Effort**: 5 min

- [ ] Add `Write` and `Edit` tools to test-reviewer agent (for creating reports)

---

## Phase 2: Jest Skill Expansion (2-3 hours)

### 2.1 Expand SKILL.md Content
**Priority**: High | **Effort**: 1.5 hours

Add sections to match playwright-testing depth:

- [ ] **React Testing Library** - Comprehensive patterns
  - Queries (getByRole, getByLabelText, etc.)
  - userEvent interactions
  - Custom render with providers
  - Testing hooks with renderHook

- [ ] **Network Mocking with MSW**
  - Setup and handlers
  - Request interception
  - Error responses
  - Dynamic responses

- [ ] **Advanced Mocking**
  - Partial mocks
  - Spy patterns
  - Manual mocks in __mocks__
  - Module factory patterns

- [ ] **Custom Matchers**
  - Creating custom matchers
  - Asymmetric matchers
  - Extending expect

- [ ] **Debugging**
  - jest.debug()
  - Test isolation issues
  - Finding slow tests
  - Memory leak detection

- [ ] **CI/CD Integration**
  - GitHub Actions workflow
  - Coverage thresholds
  - Parallelization
  - Caching

---

### 2.2 Create Jest Resources
**Priority**: High | **Effort**: 45 min

**references/jest-cheatsheet.md**:
- [ ] Common matchers quick reference
- [ ] Mock patterns quick reference
- [ ] Async patterns quick reference
- [ ] CLI commands

**assets/test-file.template.ts**:
- [ ] Unit test template
- [ ] Integration test template
- [ ] React component test template
- [ ] API test template

**scripts/check-jest-setup.sh**:
- [ ] Check for package.json
- [ ] Verify jest.config exists
- [ ] Check dependencies
- [ ] Validate coverage config

---

## Phase 3: Quality Skill Enhancement (1-1.5 hours)

### 3.1 Make Framework-Agnostic
**Priority**: High | **Effort**: 30 min

- [ ] Replace Jest-specific examples with:
  - Multi-framework examples (Jest + Vitest + Mocha)
  - Pseudocode for concepts
  - Framework-specific subsections

- [ ] Add framework detection guidance
- [ ] Remove `jest.mock` references from generic sections

---

### 3.2 Add Concrete Tooling
**Priority**: Medium | **Effort**: 30 min

- [ ] **Mutation Testing Setup**
  - Stryker installation
  - Configuration
  - Interpreting results
  - CI integration

- [ ] **Quality Scoring Algorithm**
  - Weighted metrics
  - Threshold definitions
  - Score calculation

---

### 3.3 Create Quality Resources
**Priority**: High | **Effort**: 30 min

**references/quality-checklist.md**:
- [ ] Printable checklist format
- [ ] Severity levels
- [ ] Quick fixes

**assets/quality-report.template.md**:
- [ ] Report structure
- [ ] Metrics table
- [ ] Issue tracking
- [ ] Recommendations format

**scripts/calculate-metrics.sh**:
- [ ] Test count metrics
- [ ] Coverage parsing
- [ ] Test/code ratio
- [ ] Execution time

---

## Phase 4: Command Enhancements (30 min)

### 4.1 analyze-coverage Command
**Priority**: Medium | **Effort**: 15 min

- [ ] Add concrete lcov.info parsing logic
- [ ] Add coverage-final.json parsing
- [ ] Reference skill scripts
- [ ] Show real output example

---

### 4.2 review-tests Command
**Priority**: Low | **Effort**: 10 min

- [ ] Add explicit agent spawn example
- [ ] Document when to use agent vs direct analysis
- [ ] Add real output example

---

### 4.3 suggest-tests Command
**Priority**: Low | **Effort**: 5 min

- [ ] Clarify required vs optional argument
- [ ] Add complete generated test example

---

## Phase 5: Integration & Polish (30 min)

### 5.1 Cross-Component References
**Priority**: Medium | **Effort**: 15 min

- [ ] Agent references which skills it leverages
- [ ] Skills reference when to escalate to agent
- [ ] Commands reference both skills and agent

---

### 5.2 Skill Differentiation
**Priority**: Medium | **Effort**: 10 min

Update descriptions to prevent overlap:

- [ ] **jest-testing**: "...or files matching *.test.{js,ts}. Does NOT handle general quality analysis - use analyzing-test-quality for that."
- [ ] **analyzing-test-quality**: "...for framework-agnostic quality analysis. Does NOT provide framework-specific patterns - use jest-testing or playwright-testing."

---

### 5.3 Optional: Add Hooks
**Priority**: Low | **Effort**: 5 min

- [ ] Pre-commit test quality reminder hook

---

## Implementation Order

```
Week 1 (Critical Path)
├── Phase 1: Foundation Fixes (30 min)
│   ├── 1.1 Version alignment
│   ├── 1.2 Add capabilities
│   └── 1.3 Update agent tools
│
├── Phase 2: Jest Expansion (2-3 hours)
│   ├── 2.1 Expand SKILL.md
│   └── 2.2 Create resources
│
└── Phase 3: Quality Enhancement (1-1.5 hours)
    ├── 3.1 Make framework-agnostic
    ├── 3.2 Add tooling
    └── 3.3 Create resources

Week 2 (Polish)
├── Phase 4: Commands (30 min)
└── Phase 5: Integration (30 min)
```

---

## Dependencies

```
Phase 1 ──┬──► Phase 2 (Jest needs capabilities first)
          │
          └──► Phase 3 (Quality needs capabilities first)

Phase 2 ──┬──► Phase 4 (Commands reference Jest patterns)
          │
Phase 3 ──┘

Phase 4 ──────► Phase 5 (Integration needs all commands ready)
```

---

## Validation Checklist

After implementation, verify:

### Skill Balance
- [ ] jest-testing SKILL.md is 400+ lines
- [ ] All skills have populated resources
- [ ] All skills have capabilities
- [ ] All code examples use TypeScript

### Resources
- [ ] jest-testing/references/ has cheatsheet
- [ ] jest-testing/assets/ has templates
- [ ] jest-testing/scripts/ has setup checker
- [ ] analyzing-test-quality/ has all resources

### Integration
- [ ] Agent mentions skill usage
- [ ] Skills reference agent for complex tasks
- [ ] Commands reference both

### Validation
- [ ] All components pass validation scripts
- [ ] No critical errors
- [ ] Plugin version is 1.1.0

---

## Success Metrics

| Metric | Before | After Target |
|--------|--------|--------------|
| jest-testing lines | 185 | 400+ |
| Skills with capabilities | 1/3 | 3/3 |
| Skills with resources | 1/3 | 3/3 |
| Plugin version | 1.0.0 | 1.1.0 |
| Framework examples consistent | No | Yes (TypeScript) |

---

## Risk Mitigation

### Risk: Time overrun on Jest expansion
**Mitigation**: Prioritize RTL and MSW sections first - these are most commonly needed

### Risk: Framework-agnostic examples too abstract
**Mitigation**: Use tabbed/collapsible format showing same concept in Jest/Vitest/Mocha

### Risk: Resources become outdated
**Mitigation**: Add version notes and "last updated" dates to resources

---

## Post-Implementation

After completing all phases:

1. **Re-run plugin review** to verify improvements
2. **Update PLUGIN_REVIEW.md** with new scores
3. **Test all commands** manually
4. **Validate skill auto-invocation** triggers
5. **Update README.md** with new capabilities

---

## Quick Start

To begin implementation immediately:

```bash
# Start with Phase 1.2 - Add capabilities
# Edit these files:

# 1. Agent
code testing-expert/agents/test-reviewer.md

# 2. Jest skill
code testing-expert/skills/jest-testing/SKILL.md

# 3. Quality skill
code testing-expert/skills/analyzing-test-quality/SKILL.md
```

Then proceed to Phase 2 (Jest expansion) which has the highest impact.
