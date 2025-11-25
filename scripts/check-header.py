
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
Script to check if code files have required headers.
Skips files in .gitignore.
"""

import json
import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple, Callable

try:
    from gitignore_parser import parse_gitignore
except ImportError:
    print("Warning: gitignore-parser not installed. Install with: pip install gitignore-parser", file=sys.stderr)
    print("Continuing without .gitignore support...", file=sys.stderr)
    parse_gitignore = None


class HeaderChecker:
    """Checks if files have required headers."""
    
    def __init__(self, config_path: str = "header-config.json"):
        """Initialize with config file."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.ignore_patterns = self._load_gitignore()
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _load_gitignore(self) -> Optional[Callable]:
        """Load .gitignore patterns."""
        gitignore_path = Path(".gitignore")
        if parse_gitignore and gitignore_path.exists():
            try:
                return parse_gitignore(gitignore_path)
            except Exception as e:
                print(f"Warning: Error parsing .gitignore: {e}", file=sys.stderr)
        return None
    
    def _is_ignored(self, file_path: Path) -> bool:
        """Check if file should be ignored based on .gitignore."""
        if self.ignore_patterns:
            return self.ignore_patterns(str(file_path))
        return False
    
    def _is_supported_file(self, file_path: Path) -> bool:
        """Check if file extension is supported."""
        ext = file_path.suffix.lower()
        for extensions in self.config.get("file_extensions", {}).values():
            if ext in extensions:
                return True
        return False
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if file is binary."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(8192)
                return b'\x00' in chunk
        except Exception:
            return True
    
    def _has_header(self, content: str) -> bool:
        """Check if file has required header."""
        # Check for key markers in header
        markers = [
            "STRICTLY CONFIDENTIAL | DLP:OMI::STRICT",
            "OWNERSHIP NOTICE:",
            "Trace ID:"
        ]
        content_upper = content.upper()
        return all(marker.upper() in content_upper for marker in markers)
    
    def _check_file(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Check if a file has header.
        
        Returns:
            (has_header, error_message)
        """
        # Skip ignored files
        if self._is_ignored(file_path):
            return (True, None)  # Consider ignored files as OK
        
        # Skip unsupported files
        if not self._is_supported_file(file_path):
            return (True, None)  # Consider unsupported files as OK
        
        # Skip binary files
        if self._is_binary_file(file_path):
            return (True, None)  # Consider binary files as OK
        
        # Read and check content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            return (True, None)  # Skip files with encoding issues
        except Exception as e:
            return (False, f"Error reading file: {e}")
        
        if not self._has_header(content):
            return (False, "Missing required header")
        
        return (True, None)
    
    def check_files(self, file_paths: List[Path]) -> Tuple[List[Path], List[Tuple[Path, str]]]:
        """
        Check multiple files for headers.
        
        Returns:
            (files_with_header, [(file_path, error), ...])
        """
        files_with_header = []
        files_without_header = []
        
        for file_path in file_paths:
            if not file_path.exists():
                files_without_header.append((file_path, "File not found"))
                continue
            
            has_header, error = self._check_file(file_path)
            if has_header and error is None:
                files_with_header.append(file_path)
            else:
                files_without_header.append((file_path, error or "Missing header"))
        
        return files_with_header, files_without_header
    
    def check_directory(self, directory: Path, recursive: bool = True) -> Tuple[List[Path], List[Tuple[Path, str]]]:
        """
        Check all files in a directory.
        
        Args:
            directory: Directory to check
            recursive: If True, check subdirectories recursively
            
        Returns:
            (files_with_header, [(file_path, error), ...])
        """
        files_to_check = []
        
        if recursive:
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    files_to_check.append(file_path)
        else:
            for file_path in directory.iterdir():
                if file_path.is_file():
                    files_to_check.append(file_path)
        
        return self.check_files(files_to_check)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check if code files have required headers")
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to check")
    parser.add_argument("--config", default="header-config.json", help="Path to config file")
    parser.add_argument("--no-recursive", action="store_true", help="Don't check subdirectories")
    
    args = parser.parse_args()
    
    checker = HeaderChecker(args.config)
    
    all_files_with_header = []
    all_files_without_header = []
    
    for path_str in args.paths:
        path = Path(path_str)
        
        if path.is_file():
            has_header, error = checker._check_file(path)
            if has_header and error is None:
                all_files_with_header.append(path)
            else:
                all_files_without_header.append((path, error or "Missing header"))
        elif path.is_dir():
            files_with, files_without = checker.check_directory(path, recursive=not args.no_recursive)
            all_files_with_header.extend(files_with)
            all_files_without_header.extend(files_without)
        else:
            print(f"Error: Path not found: {path}", file=sys.stderr)
            all_files_without_header.append((path, "Path not found"))
    
    # Print results
    if all_files_without_header:
        print("Files missing required header:")
        print("=" * 80)
        for file_path, error in all_files_without_header:
            print(f"  [X] {file_path}: {error}")
        print("=" * 80)
        print(f"\nTotal: {len(all_files_without_header)} file(s) missing header")
        sys.exit(1)
    else:
        print(f"[OK] All {len(all_files_with_header)} file(s) have required headers")
        sys.exit(0)


if __name__ == "__main__":
    main()

