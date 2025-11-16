#!/usr/bin/env python3
"""
Research Cache Manager

Manage cached research findings to avoid redundant research and build institutional knowledge.

Usage:
    python cache-manager.py list [category]
    python cache-manager.py search <query>
    python cache-manager.py show <cache-id>
    python cache-manager.py add <category> <topic> <file>
    python cache-manager.py invalidate <cache-id>
    python cache-manager.py clear [--all|--expired|--category <cat>]
    python cache-manager.py stats
"""

import os
import re
import sys
import json
import yaml
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

# Cache directory
CACHE_DIR = Path(__file__).parent.parent / '.research-cache'
CATEGORIES = ['investigations', 'best-practices', 'patterns', 'comparisons']

# Default cache expiry (30 days)
DEFAULT_EXPIRY_DAYS = 30

class CacheEntry:
    """Represents a cached research entry"""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.metadata = {}
        self.content = ""
        self._load()

    def _load(self):
        """Load entry from file"""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Cache file not found: {self.filepath}")

        text = self.filepath.read_text()

        # Extract YAML frontmatter
        if text.startswith('---\n'):
            parts = text.split('---\n', 2)
            if len(parts) >= 3:
                try:
                    self.metadata = yaml.safe_load(parts[1])
                    self.content = parts[2].strip()
                except yaml.YAMLError as e:
                    print(f"Warning: Could not parse YAML frontmatter: {e}")
                    self.content = text
            else:
                self.content = text
        else:
            self.content = text

    @property
    def cache_id(self) -> str:
        """Get cache ID (filename without extension)"""
        return self.filepath.stem

    @property
    def category(self) -> str:
        """Get category from parent directory"""
        return self.filepath.parent.name

    @property
    def topic(self) -> str:
        """Get topic from metadata or filename"""
        return self.metadata.get('topic', self.cache_id.replace('-', ' '))

    @property
    def date(self) -> Optional[datetime]:
        """Get date from metadata"""
        date_str = self.metadata.get('date')
        if date_str:
            try:
                return datetime.fromisoformat(str(date_str))
            except:
                pass
        return None

    @property
    def expiry(self) -> Optional[datetime]:
        """Get expiry date from metadata"""
        expiry_str = self.metadata.get('expiry')
        if expiry_str:
            try:
                return datetime.fromisoformat(str(expiry_str))
            except:
                pass
        return None

    @property
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        if self.expiry:
            return datetime.now() > self.expiry
        return False

    @property
    def tags(self) -> List[str]:
        """Get tags from metadata"""
        return self.metadata.get('tags', [])

    @property
    def related_files(self) -> List[str]:
        """Get related files from metadata"""
        return self.metadata.get('related_files', [])

    def matches_query(self, query: str) -> bool:
        """Check if entry matches search query"""
        query_lower = query.lower()

        # Search in topic
        if query_lower in self.topic.lower():
            return True

        # Search in tags
        if any(query_lower in tag.lower() for tag in self.tags):
            return True

        # Search in content
        if query_lower in self.content.lower():
            return True

        return False

def list_cache(category: Optional[str] = None, show_expired: bool = True) -> List[CacheEntry]:
    """List all cache entries, optionally filtered by category"""
    entries = []

    categories_to_search = [category] if category else CATEGORIES

    for cat in categories_to_search:
        cat_dir = CACHE_DIR / cat
        if not cat_dir.exists():
            continue

        for file in cat_dir.glob('*.md'):
            try:
                entry = CacheEntry(file)
                if show_expired or not entry.is_expired:
                    entries.append(entry)
            except Exception as e:
                print(f"Warning: Could not load {file}: {e}", file=sys.stderr)

    return sorted(entries, key=lambda e: e.date or datetime.min, reverse=True)

def search_cache(query: str) -> List[CacheEntry]:
    """Search cache entries by query"""
    all_entries = list_cache()
    return [entry for entry in all_entries if entry.matches_query(query)]

def show_entry(cache_id: str) -> Optional[CacheEntry]:
    """Show a specific cache entry"""
    # Search in all categories
    for category in CATEGORIES:
        filepath = CACHE_DIR / category / f"{cache_id}.md"
        if filepath.exists():
            return CacheEntry(filepath)

    return None

def add_entry(category: str, topic: str, source_file: Path,
              tags: List[str] = None, related_files: List[str] = None,
              codebase_hash: str = None) -> Path:
    """Add a new cache entry"""
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category: {category}. Must be one of {CATEGORIES}")

    # Generate cache ID
    date_str = datetime.now().strftime('%Y-%m-%d')
    topic_slug = re.sub(r'[^a-z0-9]+', '-', topic.lower()).strip('-')
    cache_id = f"{topic_slug}-{date_str}"

    # Read source content
    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    content = source_file.read_text()

    # Create metadata
    metadata = {
        'research_type': category.rstrip('s'),  # Remove plural
        'topic': topic,
        'date': date_str,
        'expiry': (datetime.now() + timedelta(days=DEFAULT_EXPIRY_DAYS)).strftime('%Y-%m-%d'),
        'tags': tags or [],
        'related_files': related_files or [],
    }

    if codebase_hash:
        metadata['codebase_hash'] = codebase_hash

    # Create cache file
    cat_dir = CACHE_DIR / category
    cat_dir.mkdir(parents=True, exist_ok=True)

    cache_file = cat_dir / f"{cache_id}.md"

    # Write with YAML frontmatter
    yaml_str = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
    cache_file.write_text(f"---\n{yaml_str}---\n\n{content}")

    return cache_file

def invalidate_entry(cache_id: str) -> bool:
    """Invalidate (delete) a cache entry"""
    entry = show_entry(cache_id)
    if entry:
        entry.filepath.unlink()
        return True
    return False

def clear_cache(all_entries: bool = False, expired_only: bool = False,
                category: Optional[str] = None) -> int:
    """Clear cache entries based on criteria"""
    count = 0

    entries = list_cache(category=category, show_expired=True)

    for entry in entries:
        should_delete = False

        if all_entries:
            should_delete = True
        elif expired_only and entry.is_expired:
            should_delete = True

        if should_delete:
            entry.filepath.unlink()
            count += 1

    return count

def get_stats() -> Dict:
    """Get cache statistics"""
    entries = list_cache(show_expired=True)

    stats = {
        'total': len(entries),
        'by_category': {},
        'expired': 0,
        'active': 0,
        'by_month': {},
        'top_tags': {},
    }

    for entry in entries:
        # Count by category
        stats['by_category'][entry.category] = stats['by_category'].get(entry.category, 0) + 1

        # Count expired
        if entry.is_expired:
            stats['expired'] += 1
        else:
            stats['active'] += 1

        # Count by month
        if entry.date:
            month_key = entry.date.strftime('%Y-%m')
            stats['by_month'][month_key] = stats['by_month'].get(month_key, 0) + 1

        # Count tags
        for tag in entry.tags:
            stats['top_tags'][tag] = stats['top_tags'].get(tag, 0) + 1

    # Sort top tags
    stats['top_tags'] = dict(sorted(stats['top_tags'].items(),
                                    key=lambda x: x[1], reverse=True)[:10])

    return stats

def print_entry_summary(entry: CacheEntry, detailed: bool = False):
    """Print a summary of a cache entry"""
    status = "⏰ EXPIRED" if entry.is_expired else "✓"
    date_str = entry.date.strftime('%Y-%m-%d') if entry.date else "Unknown"

    print(f"{status} [{entry.category}] {entry.topic}")
    print(f"   ID: {entry.cache_id}")
    print(f"   Date: {date_str}")

    if entry.tags:
        print(f"   Tags: {', '.join(entry.tags)}")

    if detailed:
        if entry.expiry:
            print(f"   Expiry: {entry.expiry.strftime('%Y-%m-%d')}")
        if entry.related_files:
            print(f"   Related files: {len(entry.related_files)}")
        print(f"   Content: {len(entry.content)} chars")

    print()

def cmd_list(args):
    """Handle list command"""
    entries = list_cache(category=args.category, show_expired=not args.hide_expired)

    if not entries:
        print("No cache entries found.")
        return

    print(f"Found {len(entries)} cache entries:\n")
    for entry in entries:
        print_entry_summary(entry, detailed=args.verbose)

def cmd_search(args):
    """Handle search command"""
    entries = search_cache(args.query)

    if not entries:
        print(f"No cache entries found matching '{args.query}'")
        return

    print(f"Found {len(entries)} matching entries:\n")
    for entry in entries:
        print_entry_summary(entry, detailed=args.verbose)

def cmd_show(args):
    """Handle show command"""
    entry = show_entry(args.cache_id)

    if not entry:
        print(f"Cache entry not found: {args.cache_id}")
        sys.exit(1)

    # Print metadata
    print(f"{'='*60}")
    print(f"Cache Entry: {entry.topic}")
    print(f"{'='*60}\n")
    print(f"ID: {entry.cache_id}")
    print(f"Category: {entry.category}")
    print(f"Date: {entry.date.strftime('%Y-%m-%d') if entry.date else 'Unknown'}")
    print(f"Expired: {'Yes' if entry.is_expired else 'No'}")
    if entry.expiry:
        print(f"Expiry: {entry.expiry.strftime('%Y-%m-%d')}")
    if entry.tags:
        print(f"Tags: {', '.join(entry.tags)}")
    if entry.related_files:
        print(f"Related files: {', '.join(entry.related_files)}")

    print(f"\n{'='*60}")
    print("Content:")
    print(f"{'='*60}\n")
    print(entry.content)

def cmd_add(args):
    """Handle add command"""
    source_file = Path(args.file)

    cache_file = add_entry(
        category=args.category,
        topic=args.topic,
        source_file=source_file,
        tags=args.tags.split(',') if args.tags else None,
        related_files=args.related_files.split(',') if args.related_files else None,
        codebase_hash=args.codebase_hash
    )

    print(f"✓ Cache entry created: {cache_file.stem}")
    print(f"  Category: {args.category}")
    print(f"  File: {cache_file}")

def cmd_invalidate(args):
    """Handle invalidate command"""
    if invalidate_entry(args.cache_id):
        print(f"✓ Cache entry invalidated: {args.cache_id}")
    else:
        print(f"✗ Cache entry not found: {args.cache_id}")
        sys.exit(1)

def cmd_clear(args):
    """Handle clear command"""
    if args.all:
        confirm = input("Clear ALL cache entries? [y/N]: ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return
        count = clear_cache(all_entries=True)
    elif args.expired:
        count = clear_cache(expired_only=True)
    elif args.category:
        count = clear_cache(category=args.category)
    else:
        print("Specify --all, --expired, or --category")
        sys.exit(1)

    print(f"✓ Cleared {count} cache entries")

def cmd_stats(args):
    """Handle stats command"""
    stats = get_stats()

    print(f"\n{'='*60}")
    print("Research Cache Statistics")
    print(f"{'='*60}\n")

    print(f"Total entries: {stats['total']}")
    print(f"  Active: {stats['active']}")
    print(f"  Expired: {stats['expired']}\n")

    if stats['by_category']:
        print("By Category:")
        for cat, count in stats['by_category'].items():
            print(f"  {cat}: {count}")
        print()

    if stats['top_tags']:
        print("Top Tags:")
        for tag, count in list(stats['top_tags'].items())[:5]:
            print(f"  {tag}: {count}")
        print()

    if stats['by_month']:
        print("Recent Activity:")
        for month, count in sorted(stats['by_month'].items(), reverse=True)[:3]:
            print(f"  {month}: {count} entries")

    print(f"\n{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(description='Manage research cache')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List cache entries')
    list_parser.add_argument('category', nargs='?', choices=CATEGORIES, help='Filter by category')
    list_parser.add_argument('--hide-expired', action='store_true', help='Hide expired entries')
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed info')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search cache entries')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed info')

    # Show command
    show_parser = subparsers.add_parser('show', help='Show a cache entry')
    show_parser.add_argument('cache_id', help='Cache entry ID')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add cache entry')
    add_parser.add_argument('category', choices=CATEGORIES, help='Category')
    add_parser.add_argument('topic', help='Research topic')
    add_parser.add_argument('file', help='Source file with research content')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    add_parser.add_argument('--related-files', help='Comma-separated related file paths')
    add_parser.add_argument('--codebase-hash', help='Git commit hash')

    # Invalidate command
    invalidate_parser = subparsers.add_parser('invalidate', help='Invalidate (delete) cache entry')
    invalidate_parser.add_argument('cache_id', help='Cache entry ID')

    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear cache entries')
    clear_group = clear_parser.add_mutually_exclusive_group(required=True)
    clear_group.add_argument('--all', action='store_true', help='Clear all entries')
    clear_group.add_argument('--expired', action='store_true', help='Clear expired entries only')
    clear_group.add_argument('--category', choices=CATEGORIES, help='Clear category')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show cache statistics')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    cmd_map = {
        'list': cmd_list,
        'search': cmd_search,
        'show': cmd_show,
        'add': cmd_add,
        'invalidate': cmd_invalidate,
        'clear': cmd_clear,
        'stats': cmd_stats,
    }

    cmd_map[args.command](args)

if __name__ == '__main__':
    main()
