# Researching Best Practices Skill Resources

This directory contains resources for the researching-best-practices skill.

## Directory Structure

### scripts/
Automation scripts for analyzing code against best practices:
- `check-practices.py` - Analyze code against best practice checklists
- `pattern-matcher.py` - Identify design patterns in code
- `security-audit.sh` - Quick security best practices check

### references/
Comprehensive best practice guides:
- `design-patterns-2025.md` - Modern design patterns catalog
- `security-checklist.md` - OWASP Top 10 and security practices
- `performance-guide.md` - Performance optimization best practices
- `testing-strategies.md` - Testing approaches and methodologies
- `api-design-principles.md` - RESTful and GraphQL API best practices

### assets/
Templates for documenting research:
- `comparison-template.md` - Template for comparing different approaches
- `checklist-template.md` - Template for creating practice checklists
- `decision-matrix.md` - Template for evaluating technology options

## Usage

These resources are referenced in SKILL.md using the `{baseDir}` variable and are loaded on-demand when needed during research.

Example:
```markdown
See `{baseDir}/references/security-checklist.md` for comprehensive security guidelines.
```

## Contributing

To add new resources:
1. Create the file in the appropriate directory
2. Follow existing formatting conventions
3. Reference it in SKILL.md if needed
4. Update this README

---

*Part of research-agent plugin*
