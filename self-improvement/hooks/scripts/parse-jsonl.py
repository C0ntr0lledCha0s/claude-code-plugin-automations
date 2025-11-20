#!/usr/bin/env python3
"""
Parse Claude Code JSONL transcript files.

Claude Code stores conversations as JSONL files with entries like:
{"type":"user","message":{"role":"user","content":"..."},"timestamp":"..."}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"..."}]},"timestamp":"..."}

This script converts them to plain text for analysis.
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


def extract_text_content(content: Any) -> str:
    """Extract text from various content formats."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Content is array of objects with type/text
        texts = []
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'text':
                    texts.append(item.get('text', ''))
                elif item.get('type') == 'tool_use':
                    # Include tool use information
                    tool_name = item.get('name', 'unknown')
                    texts.append(f"[Tool: {tool_name}]")
                elif item.get('type') == 'tool_result':
                    # Include tool result summary
                    texts.append("[Tool Result]")
        return ' '.join(texts)
    elif isinstance(content, dict):
        # Single content object
        if content.get('type') == 'text':
            return content.get('text', '')
    return ''


def parse_jsonl_file(filepath: str) -> Dict[str, Any]:
    """
    Parse a Claude Code JSONL transcript file.

    Returns:
        Dict with:
        - messages: List of parsed messages
        - user_count: Number of user messages
        - assistant_count: Number of assistant messages
        - tool_uses: Number of tool invocations
        - total_lines: Total transcript lines
        - plain_text: Plain text version for analysis
    """
    messages = []
    user_count = 0
    assistant_count = 0
    tool_uses = 0
    plain_text_lines = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as e:
                    # Skip malformed lines but continue
                    continue

                msg_type = entry.get('type', '')
                message = entry.get('message', {})
                timestamp = entry.get('timestamp', '')

                if msg_type == 'user':
                    user_count += 1
                    content = message.get('content', '')
                    text = extract_text_content(content)
                    messages.append({
                        'role': 'user',
                        'content': text,
                        'timestamp': timestamp
                    })
                    plain_text_lines.append(f"User: {text}")

                elif msg_type == 'assistant':
                    assistant_count += 1
                    content = message.get('content', [])
                    text = extract_text_content(content)
                    messages.append({
                        'role': 'assistant',
                        'content': text,
                        'timestamp': timestamp
                    })
                    plain_text_lines.append(f"Assistant: {text}")

                elif msg_type == 'tool_use':
                    tool_uses += 1
                    tool_name = entry.get('name', 'unknown')
                    messages.append({
                        'role': 'tool_use',
                        'tool': tool_name,
                        'timestamp': timestamp
                    })

                elif msg_type == 'tool_result':
                    # Tool results can be included for analysis
                    content = entry.get('content', '')
                    if isinstance(content, str) and len(content) > 500:
                        content = content[:500] + '...'
                    messages.append({
                        'role': 'tool_result',
                        'content': extract_text_content(content),
                        'timestamp': timestamp
                    })

        return {
            'messages': messages,
            'user_count': user_count,
            'assistant_count': assistant_count,
            'tool_uses': tool_uses,
            'total_lines': len(messages),
            'plain_text': '\n'.join(plain_text_lines)
        }

    except FileNotFoundError:
        return {
            'error': f'File not found: {filepath}',
            'messages': [],
            'user_count': 0,
            'assistant_count': 0,
            'tool_uses': 0,
            'total_lines': 0,
            'plain_text': ''
        }
    except Exception as e:
        return {
            'error': f'Error parsing file: {str(e)}',
            'messages': [],
            'user_count': 0,
            'assistant_count': 0,
            'tool_uses': 0,
            'total_lines': 0,
            'plain_text': ''
        }


def write_plain_text(parsed_data: Dict[str, Any], output_path: str) -> bool:
    """Write plain text version to a file for analysis scripts."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(parsed_data['plain_text'])
        return True
    except Exception as e:
        print(f"Error writing plain text: {e}", file=sys.stderr)
        return False


def main():
    """
    Main entry point.

    Usage:
        python parse-jsonl.py <jsonl-file> [output-file]

    If output-file is provided, writes plain text there.
    Otherwise, outputs JSON summary to stdout.
    """
    if len(sys.argv) < 2:
        print("Usage: python parse-jsonl.py <jsonl-file> [output-file]", file=sys.stderr)
        print("  jsonl-file: Path to Claude Code JSONL transcript", file=sys.stderr)
        print("  output-file: Optional path to write plain text output", file=sys.stderr)
        sys.exit(1)

    jsonl_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Parse the JSONL file
    result = parse_jsonl_file(jsonl_path)

    if 'error' in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # If output path provided, write plain text there
    if output_path:
        if write_plain_text(result, output_path):
            print(f"Plain text written to: {output_path}", file=sys.stderr)
        else:
            sys.exit(1)

    # Output summary as JSON
    summary = {
        'user_count': result['user_count'],
        'assistant_count': result['assistant_count'],
        'tool_uses': result['tool_uses'],
        'total_lines': result['total_lines'],
        'total_turns': result['user_count'] + result['assistant_count']
    }

    print(json.dumps(summary))


if __name__ == '__main__':
    main()
