# Analyzing Patterns Skill Resources

This directory contains resources for the analyzing-patterns skill.

## Directory Structure

### scripts/
Automation scripts for pattern detection and analysis:
- `pattern-detector.py` - Automated pattern recognition in code
- `duplicate-finder.sh` - Find duplicate/similar code blocks
- `convention-analyzer.py` - Extract naming and style conventions
- `architecture-mapper.py` - Visualize architectural patterns

### references/
Comprehensive pattern catalogs:
- `design-patterns-catalog.md` - Complete Gang of Four and modern patterns
- `architectural-patterns.md` - System-level pattern descriptions
- `refactoring-catalog.md` - Pattern-based refactoring techniques
- `anti-patterns.md` - Common anti-patterns and solutions

### assets/
Templates for documenting pattern findings:
- `pattern-template.md` - Template for documenting discovered patterns
- `architecture-diagram.md` - Template for architecture visualization
- `refactoring-checklist.md` - Checklist for pattern-based refactoring

## Usage

These resources are referenced in SKILL.md using the `{baseDir}` variable and are loaded on-demand when needed during pattern analysis.

Example:
```markdown
Refer to `{baseDir}/references/design-patterns-catalog.md` for detailed pattern descriptions.
```

## Contributing

To add new patterns or improve existing documentation:
1. Create/update files in the appropriate directory
2. Include code examples where helpful
3. Reference real-world use cases
4. Update this README if adding new file types

---

*Part of research-agent plugin*
