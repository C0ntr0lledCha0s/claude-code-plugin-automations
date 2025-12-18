---
description: Generate documentation for a file, function, class, or module
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "[file-path] [--type api|readme|module]"
---

# Documentation Generator

Generate documentation for the specified target.

**Target:** $ARGUMENTS

## Parsing Arguments

Parse the arguments to determine:
1. **File path**: Required - the file or directory to document
2. **Type flag**: Optional - `--type api`, `--type readme`, or `--type module`
   - `api`: Generate API documentation (JSDoc, docstrings, etc.)
   - `readme`: Generate a README file for the module/directory
   - `module`: Generate module-level documentation
   - Default: Infer from context

## Generation Process

### For API Documentation (`--type api`)
1. Read the target file
2. Identify all functions, classes, and exported items
3. Analyze the code to understand:
   - Parameter types and purposes
   - Return values
   - Side effects
   - Error conditions
4. Generate appropriate documentation:
   - JSDoc for JavaScript/TypeScript
   - Docstrings for Python
   - Doc comments for Go/Rust
5. Insert or update documentation in the file

### For README Generation (`--type readme`)
1. Analyze the directory/module structure
2. Identify key files and exports
3. Generate a README with:
   - Title and description
   - Installation instructions (if applicable)
   - Usage examples
   - API overview
   - Configuration options

### For Module Documentation (`--type module`)
1. Read all files in the module
2. Create module-level documentation
3. Document exports and public interface
4. Add usage examples

## Documentation Standards

Follow language-specific conventions:

### JavaScript/TypeScript
```javascript
/**
 * Brief description.
 *
 * @param {Type} name - Description
 * @returns {Type} Description
 * @throws {Error} When...
 * @example
 * const result = func(arg);
 */
```

### Python
```python
"""Brief description.

Longer description if needed.

Args:
    param: Description

Returns:
    Description

Raises:
    Error: When...

Example:
    >>> result = func(arg)
"""
```

## Output

- For API docs: Edit the file in place with new documentation
- For README: Create or update README.md in the target directory
- For module docs: Create or update module documentation file

Always show the user what was generated and ask for confirmation before making changes to existing documentation.
