
# ======================================================================================
# STRICTLY CONFIDENTIAL | DLP:OMI::STRICT
# ======================================================================================
# OWNERSHIP NOTICE:
# This source code is the proprietary property of {CUSTOMER}.
# Developed by Ominext under MSA.
#
# COPYRIGHT (c) {YEAR} {CUSTOMER}. ALL RIGHTS RESERVED.
#
# WARNING: This file contains trade secrets and confidential information.
# Unauthorized copying or uploading to public networks  is prohibited.
#
# Project: {PROJECT_CODE}
# Trace ID: {FILE_HASH}
# ======================================================================================

"""
Script to migrate headers for existing files.
Scans repository and adds/updates headers with user confirmation.
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

# Import from other scripts in same directory
_script_dir = Path(__file__).parent
sys.path.insert(0, str(_script_dir))

# Import modules (need to use importlib because of hyphens in filenames)
import importlib.util
spec_check = importlib.util.spec_from_file_location("check_header", _script_dir / "check-header.py")
check_header_module = importlib.util.module_from_spec(spec_check)
spec_check.loader.exec_module(check_header_module)
HeaderChecker = check_header_module.HeaderChecker

spec_add = importlib.util.spec_from_file_location("add_header", _script_dir / "add-header.py")
add_header_module = importlib.util.module_from_spec(spec_add)
spec_add.loader.exec_module(add_header_module)
HeaderManager = add_header_module.HeaderManager


class HeaderMigrator:
    """Migrates headers for existing files."""
    
    def __init__(self, config_path: str = "header-config.json"):
        """Initialize with config file."""
        self.config_path = Path(config_path)
        self.checker = HeaderChecker(config_path)
        self.manager = HeaderManager(config_path)
    
    def find_files_needing_header(self, directory: Path, recursive: bool = True) -> List[Path]:
        """
        Find all files that need header migration.
        
        Args:
            directory: Directory to scan
            recursive: If True, scan subdirectories recursively
            
        Returns:
            List of file paths that need headers
        """
        files_needing_header = []
        
        if recursive:
            file_paths = list(directory.rglob("*"))
        else:
            file_paths = list(directory.iterdir())
        
        for file_path in file_paths:
            if not file_path.is_file():
                continue
            
            # Skip ignored files
            if self.checker._is_ignored(file_path):
                continue
            
            # Check if file needs header
            has_header, error = self.checker._check_file(file_path)
            if not has_header or error:
                files_needing_header.append(file_path)
        
        return files_needing_header
    
    def migrate_files(self, file_paths: List[Path], force: bool = False) -> Tuple[int, int]:
        """
        Migrate headers for multiple files.
        
        Args:
            file_paths: List of file paths to migrate
            force: If True, replace existing headers
            
        Returns:
            (success_count, failure_count)
        """
        success_count = 0
        failure_count = 0
        
        for file_path in file_paths:
            if self.manager.add_header(file_path, force=force):
                success_count += 1
            else:
                failure_count += 1
        
        return success_count, failure_count
    
    def interactive_migrate(self, directory: Path = Path("."), recursive: bool = True) -> bool:
        """
        Interactive migration with user confirmation.
        
        Args:
            directory: Directory to scan
            recursive: If True, scan subdirectories recursively
            
        Returns:
            True if migration was successful
        """
        print("Scanning for files needing header migration...")
        files_needing_header = self.find_files_needing_header(directory, recursive)
        
        if not files_needing_header:
            print("[OK] All files already have headers!")
            return True
        
        print(f"\nFound {len(files_needing_header)} file(s) needing header:")
        print("=" * 80)
        for i, file_path in enumerate(files_needing_header[:50], 1):  # Show first 50
            print(f"  {i}. {file_path}")
        if len(files_needing_header) > 50:
            print(f"  ... and {len(files_needing_header) - 50} more file(s)")
        print("=" * 80)
        
        # Ask for confirmation
        response = input(f"\nDo you want to add/update headers for these {len(files_needing_header)} file(s)? (yes/no): ").strip().lower()
        
        if response not in ['yes', 'y']:
            print("Migration cancelled.")
            return False
        
        # Ask about force mode
        force = False
        existing_headers = sum(1 for f in files_needing_header if self.checker._has_header(self._read_file_content(f)))
        if existing_headers > 0:
            force_response = input(f"Found {existing_headers} file(s) with existing headers. Replace them? (yes/no): ").strip().lower()
            force = force_response in ['yes', 'y']
        
        # Perform migration
        print("\nMigrating headers...")
        success_count, failure_count = self.migrate_files(files_needing_header, force=force)
        
        print(f"\nMigration complete:")
        print(f"  [OK] Success: {success_count} file(s)")
        if failure_count > 0:
            print(f"  [X] Failed: {failure_count} file(s)")
        
        return failure_count == 0
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read file content safely."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate headers for existing files")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--config", default="header-config.json", help="Path to config file")
    parser.add_argument("--no-recursive", action="store_true", help="Don't scan subdirectories")
    parser.add_argument("--force", action="store_true", help="Force replace existing headers")
    parser.add_argument("--non-interactive", action="store_true", help="Run without confirmation prompts")
    
    args = parser.parse_args()
    
    migrator = HeaderMigrator(args.config)
    directory = Path(args.directory)
    
    if not directory.exists():
        print(f"Error: Directory not found: {directory}", file=sys.stderr)
        sys.exit(1)
    
    if args.non_interactive:
        # Non-interactive mode
        files_needing_header = migrator.find_files_needing_header(directory, recursive=not args.no_recursive)
        if not files_needing_header:
            print("[OK] All files already have headers!")
            sys.exit(0)
        
        success_count, failure_count = migrator.migrate_files(files_needing_header, force=args.force)
        print(f"Migrated {success_count} file(s), {failure_count} failed")
        sys.exit(0 if failure_count == 0 else 1)
    else:
        # Interactive mode
        success = migrator.interactive_migrate(directory, recursive=not args.no_recursive)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

