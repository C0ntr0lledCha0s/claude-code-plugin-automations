#!/usr/bin/env python3
"""
Real Code Quality Analysis Engine

Analyzes actual code blocks from conversations using:
- AST parsing for structural analysis
- Pattern detection for common issues
- Security vulnerability detection
- Code complexity metrics

This replaces naive keyword matching with semantic code analysis.
"""

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

# Issue severity levels
CRITICAL = "critical"
IMPORTANT = "important"
MINOR = "minor"


class CodeAnalysisResult:
    """Container for code analysis results."""

    def __init__(self):
        self.issues: list[dict] = []
        self.metrics: dict = {
            "total_code_blocks": 0,
            "python_blocks": 0,
            "javascript_blocks": 0,
            "other_blocks": 0,
            "total_functions": 0,
            "total_classes": 0,
            "total_lines": 0,
            "complexity_score": 0,
        }
        self.patterns: list[dict] = []
        self.learnings: list[dict] = []

    def add_issue(self, severity: str, issue_type: str, message: str, code_snippet: str = ""):
        """Add an issue found during analysis."""
        self.issues.append({
            "severity": severity,
            "type": issue_type,
            "message": message,
            "snippet": code_snippet[:200] if code_snippet else ""
        })

    def add_pattern(self, pattern_type: str, description: str, severity: str):
        """Add a detected pattern."""
        self.patterns.append({
            "type": pattern_type,
            "description": description,
            "severity": severity
        })

    def add_learning(self, key: str, text: str):
        """Add a learning point."""
        self.learnings.append({
            "key": key,
            "text": text
        })

    def to_json(self) -> str:
        """Convert results to JSON string."""
        return json.dumps({
            "issues": self.issues,
            "metrics": self.metrics,
            "patterns": self.patterns,
            "learnings": self.learnings
        }, indent=2)


def extract_code_blocks(text: str) -> list[dict]:
    """
    Extract code blocks from markdown-formatted text.

    Returns list of dicts with 'language' and 'code' keys.
    """
    # Match fenced code blocks with optional language specifier
    pattern = r"```(\w*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    blocks = []
    for lang, code in matches:
        blocks.append({
            "language": lang.lower() if lang else "unknown",
            "code": code.strip()
        })

    return blocks


def analyze_python_code(code: str, result: CodeAnalysisResult) -> None:
    """
    Analyze Python code using AST parsing.

    Detects:
    - Missing error handling
    - Security issues (eval, exec, etc.)
    - Code complexity
    - Missing docstrings
    - Bare exceptions
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        result.add_issue(
            IMPORTANT,
            "syntax_error",
            f"Python syntax error: {e.msg} at line {e.lineno}",
            code[:100]
        )
        return

    # Count functions and classes
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    async_functions = [node for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    result.metrics["total_functions"] += len(functions) + len(async_functions)
    result.metrics["total_classes"] += len(classes)

    # Analyze each function
    for func in functions + async_functions:
        analyze_function(func, code, result)

    # Security checks
    check_security_issues(tree, code, result)

    # Check for global code quality issues
    check_global_issues(tree, code, result)


def analyze_function(func: ast.FunctionDef | ast.AsyncFunctionDef, code: str, result: CodeAnalysisResult) -> None:
    """Analyze a single function for quality issues."""

    # Check for missing docstring
    if not ast.get_docstring(func):
        # Only flag if function is non-trivial (more than 5 lines)
        func_lines = func.end_lineno - func.lineno if hasattr(func, 'end_lineno') else 0
        if func_lines > 5:
            result.add_issue(
                MINOR,
                "missing_docstring",
                f"Function '{func.name}' lacks a docstring",
                ""
            )

    # Check for bare except clauses
    for node in ast.walk(func):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                result.add_issue(
                    IMPORTANT,
                    "bare_except",
                    f"Bare except clause in function '{func.name}' - catches all exceptions including KeyboardInterrupt",
                    ""
                )

    # Check function complexity (count branches)
    complexity = count_complexity(func)
    if complexity > 10:
        result.add_issue(
            IMPORTANT,
            "high_complexity",
            f"Function '{func.name}' has cyclomatic complexity of {complexity} (>10 is high)",
            ""
        )
        result.metrics["complexity_score"] += complexity

    # Check for too many arguments
    args = func.args
    total_args = len(args.args) + len(args.posonlyargs) + len(args.kwonlyargs)
    if total_args > 5:
        result.add_issue(
            MINOR,
            "too_many_arguments",
            f"Function '{func.name}' has {total_args} arguments (>5 may indicate need for refactoring)",
            ""
        )

    # Check for missing return type hint (Python 3.5+)
    if func.returns is None and func.name != "__init__":
        # Only flag for non-trivial functions
        if hasattr(func, 'end_lineno') and (func.end_lineno - func.lineno) > 3:
            result.add_issue(
                MINOR,
                "missing_type_hint",
                f"Function '{func.name}' lacks return type hint",
                ""
            )


def count_complexity(node: ast.AST) -> int:
    """
    Calculate cyclomatic complexity for a function.

    Counts decision points: if, for, while, except, and, or, ternary
    """
    complexity = 1  # Base complexity

    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            # and/or operations add complexity
            complexity += len(child.values) - 1
        elif isinstance(child, ast.IfExp):
            # Ternary expression
            complexity += 1

    return complexity


def check_security_issues(tree: ast.AST, code: str, result: CodeAnalysisResult) -> None:
    """Check for common security vulnerabilities in Python code."""

    for node in ast.walk(tree):
        # Check for dangerous function calls
        if isinstance(node, ast.Call):
            func_name = get_call_name(node)

            # eval() and exec()
            if func_name in ("eval", "exec"):
                result.add_issue(
                    CRITICAL,
                    "dangerous_eval",
                    f"Use of {func_name}() is dangerous - can execute arbitrary code",
                    get_node_source(node, code)
                )
                result.add_learning(
                    "avoid_eval_exec",
                    "Avoid eval() and exec() - use ast.literal_eval() for data parsing or explicit parsing"
                )

            # pickle with untrusted data
            if func_name in ("pickle.loads", "pickle.load"):
                result.add_issue(
                    CRITICAL,
                    "insecure_deserialization",
                    "pickle.load() can execute arbitrary code - don't use with untrusted data",
                    get_node_source(node, code)
                )

            # subprocess with shell=True
            if func_name in ("subprocess.call", "subprocess.run", "subprocess.Popen"):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        result.add_issue(
                            IMPORTANT,
                            "shell_injection",
                            "subprocess with shell=True can lead to command injection",
                            get_node_source(node, code)
                        )
                        result.add_learning(
                            "subprocess_shell_false",
                            "Use subprocess with shell=False and pass arguments as a list"
                        )

            # os.system()
            if func_name == "os.system":
                result.add_issue(
                    IMPORTANT,
                    "shell_injection",
                    "os.system() is vulnerable to command injection - use subprocess instead",
                    get_node_source(node, code)
                )

        # Check for hardcoded secrets (basic patterns)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id.lower()
                    if any(secret in var_name for secret in ("password", "secret", "api_key", "apikey", "token", "credential")):
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            if len(node.value.value) > 5:  # Non-trivial string value
                                result.add_issue(
                                    CRITICAL,
                                    "hardcoded_secret",
                                    f"Potential hardcoded secret in variable '{target.id}'",
                                    ""
                                )
                                result.add_learning(
                                    "use_env_vars_for_secrets",
                                    "Store secrets in environment variables or secure vaults, not in code"
                                )


def check_global_issues(tree: ast.AST, code: str, result: CodeAnalysisResult) -> None:
    """Check for code-wide quality issues."""

    # Check for wildcard imports
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    result.add_issue(
                        MINOR,
                        "wildcard_import",
                        f"Wildcard import from {node.module} - imports unknown names into namespace",
                        ""
                    )

    # Check for global variables (excluding constants)
    module_body = tree.body if hasattr(tree, 'body') else []
    for node in module_body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Skip if it looks like a constant (ALL_CAPS)
                    if not target.id.isupper():
                        # This is a module-level mutable variable
                        pass  # Don't flag - too noisy

    # Check for missing if __name__ == "__main__" guard
    has_main_guard = False
    has_top_level_calls = False

    for node in module_body:
        if isinstance(node, ast.If):
            if is_main_guard(node):
                has_main_guard = True
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            # Top-level function call
            has_top_level_calls = True

    if has_top_level_calls and not has_main_guard:
        # Only flag if there are actual function calls at module level
        result.add_issue(
            MINOR,
            "missing_main_guard",
            "Module has top-level code without if __name__ == '__main__' guard",
            ""
        )


def is_main_guard(node: ast.If) -> bool:
    """Check if an if statement is a __name__ == '__main__' guard."""
    if isinstance(node.test, ast.Compare):
        if len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq):
            left = node.test.left
            right = node.test.comparators[0] if node.test.comparators else None

            if isinstance(left, ast.Name) and left.id == "__name__":
                if isinstance(right, ast.Constant) and right.value == "__main__":
                    return True
    return False


def get_call_name(node: ast.Call) -> str:
    """Get the full name of a function call (e.g., 'os.path.join')."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    elif isinstance(node.func, ast.Attribute):
        parts = []
        current = node.func
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))
    return ""


def get_node_source(node: ast.AST, code: str) -> str:
    """Extract the source code for a given AST node."""
    if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
        lines = code.split('\n')
        start = node.lineno - 1
        end = node.end_lineno
        return '\n'.join(lines[start:end])
    return ""


def analyze_javascript_code(code: str, result: CodeAnalysisResult) -> None:
    """
    Analyze JavaScript code using pattern matching.

    Note: Full AST parsing would require a JS parser like esprima.
    This uses regex patterns for common issues.
    """

    # Check for eval()
    if re.search(r'\beval\s*\(', code):
        result.add_issue(
            CRITICAL,
            "dangerous_eval",
            "Use of eval() in JavaScript is dangerous - can execute arbitrary code",
            ""
        )
        result.add_learning(
            "avoid_eval_js",
            "Avoid eval() in JavaScript - use JSON.parse() for data or explicit parsing"
        )

    # Check for innerHTML with variables (potential XSS)
    if re.search(r'\.innerHTML\s*=\s*[^"\'`]', code):
        result.add_issue(
            CRITICAL,
            "potential_xss",
            "innerHTML assignment with variable - potential XSS vulnerability",
            ""
        )
        result.add_learning(
            "use_textcontent",
            "Use textContent instead of innerHTML when possible, or sanitize HTML input"
        )

    # Check for document.write
    if re.search(r'\bdocument\.write\s*\(', code):
        result.add_issue(
            IMPORTANT,
            "document_write",
            "document.write() is deprecated and can cause security issues",
            ""
        )

    # Check for console.log (should be removed in production)
    console_logs = len(re.findall(r'\bconsole\.log\s*\(', code))
    if console_logs > 5:
        result.add_issue(
            MINOR,
            "excessive_logging",
            f"Found {console_logs} console.log statements - remove before production",
            ""
        )

    # Check for var instead of let/const
    var_count = len(re.findall(r'\bvar\s+\w+', code))
    if var_count > 3:
        result.add_issue(
            MINOR,
            "use_let_const",
            f"Found {var_count} uses of 'var' - prefer 'let' or 'const' for block scoping",
            ""
        )

    # Check for ==  instead of ===
    loose_equality = len(re.findall(r'[^=!]==[^=]', code))
    if loose_equality > 0:
        result.add_issue(
            MINOR,
            "use_strict_equality",
            f"Found {loose_equality} uses of '==' - prefer '===' for strict comparison",
            ""
        )


def analyze_shell_code(code: str, result: CodeAnalysisResult) -> None:
    """Analyze shell/bash code for common issues."""

    # Check for unquoted variables
    if re.search(r'\$\w+(?!["\'])', code):
        if not re.search(r'"\$\w+"', code):  # Not all quoted
            result.add_issue(
                IMPORTANT,
                "unquoted_variable",
                "Unquoted shell variables can cause word splitting issues",
                ""
            )
            result.add_learning(
                "quote_shell_vars",
                "Always quote shell variables: use \"$var\" instead of $var"
            )

    # Check for rm -rf with variables
    if re.search(r'rm\s+-rf?\s+\$', code):
        result.add_issue(
            CRITICAL,
            "dangerous_rm",
            "rm -rf with variable path is dangerous - variable could be empty or wrong",
            ""
        )
        result.add_learning(
            "safe_rm_rf",
            "Use 'rm -rf \"${var:?}\"' to fail if variable is empty, or use explicit paths"
        )

    # Check for curl | bash pattern
    if re.search(r'curl.*\|\s*(?:ba)?sh', code):
        result.add_issue(
            CRITICAL,
            "curl_pipe_bash",
            "curl | bash is dangerous - downloads and executes untrusted code",
            ""
        )


def analyze_sql_code(code: str, result: CodeAnalysisResult) -> None:
    """Analyze SQL code for common issues."""

    # Check for string concatenation in queries (potential SQL injection)
    if re.search(r"['\"].*\+.*['\"]|f['\"].*\{.*\}.*['\"]", code):
        result.add_issue(
            CRITICAL,
            "sql_injection",
            "String concatenation in SQL query - use parameterized queries",
            ""
        )
        result.add_learning(
            "parameterized_queries",
            "Always use parameterized queries (?, :param, or %s) instead of string concatenation"
        )

    # Check for SELECT *
    if re.search(r'SELECT\s+\*', code, re.IGNORECASE):
        result.add_issue(
            MINOR,
            "select_star",
            "SELECT * can fetch unnecessary data - specify columns explicitly",
            ""
        )


def analyze_code_blocks(text: str) -> CodeAnalysisResult:
    """
    Main entry point: analyze all code blocks in the given text.

    Returns a CodeAnalysisResult with all findings.
    """
    result = CodeAnalysisResult()
    blocks = extract_code_blocks(text)

    result.metrics["total_code_blocks"] = len(blocks)

    for block in blocks:
        lang = block["language"]
        code = block["code"]

        result.metrics["total_lines"] += code.count('\n') + 1

        if lang in ("python", "py", "python3"):
            result.metrics["python_blocks"] += 1
            analyze_python_code(code, result)
        elif lang in ("javascript", "js", "typescript", "ts", "jsx", "tsx"):
            result.metrics["javascript_blocks"] += 1
            analyze_javascript_code(code, result)
        elif lang in ("bash", "sh", "shell", "zsh"):
            result.metrics["other_blocks"] += 1
            analyze_shell_code(code, result)
        elif lang in ("sql", "mysql", "postgresql", "postgres"):
            result.metrics["other_blocks"] += 1
            analyze_sql_code(code, result)
        else:
            result.metrics["other_blocks"] += 1

    # Generate patterns based on analysis
    generate_patterns(result)

    return result


def generate_patterns(result: CodeAnalysisResult) -> None:
    """Generate patterns based on the issues found."""

    # Count issues by type
    critical_count = sum(1 for i in result.issues if i["severity"] == CRITICAL)
    important_count = sum(1 for i in result.issues if i["severity"] == IMPORTANT)

    # Security issues pattern
    security_issues = [i for i in result.issues if i["type"] in (
        "dangerous_eval", "shell_injection", "sql_injection",
        "potential_xss", "hardcoded_secret", "insecure_deserialization",
        "dangerous_rm", "curl_pipe_bash"
    )]
    if security_issues:
        result.add_pattern(
            "security_vulnerabilities",
            f"Found {len(security_issues)} security issues in code",
            CRITICAL
        )

    # Code quality pattern
    if result.metrics["complexity_score"] > 20:
        result.add_pattern(
            "high_code_complexity",
            f"Code has high complexity score of {result.metrics['complexity_score']}",
            IMPORTANT
        )

    # Missing error handling pattern
    bare_excepts = sum(1 for i in result.issues if i["type"] == "bare_except")
    if bare_excepts > 0:
        result.add_pattern(
            "poor_error_handling",
            f"Found {bare_excepts} bare except clauses",
            IMPORTANT
        )

    # Overall quality assessment
    if critical_count >= 3:
        result.add_pattern(
            "critical_code_issues",
            f"Code has {critical_count} critical issues requiring immediate attention",
            CRITICAL
        )
    elif important_count >= 5:
        result.add_pattern(
            "code_quality_concerns",
            f"Code has {important_count} important issues to address",
            IMPORTANT
        )


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: analyze-code-quality.py <text-file> [output-file]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    result = analyze_code_blocks(text)

    output = result.to_json()

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
