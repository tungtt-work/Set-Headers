
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
Pre-commit hook script to check headers on staged files.
Can be used with pre-commit framework or standalone.
"""

import subprocess
import sys
from pathlib import Path


def get_staged_files():
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True
        )
        files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return [Path(f) for f in files if Path(f).exists()]
    except subprocess.CalledProcessError as e:
        print(f"Error getting staged files: {e}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Error: git not found. Make sure git is installed.", file=sys.stderr)
        return []


def filter_supported_files(file_paths):
    """Filter files to only include supported code files."""
    # Get config to check supported extensions
    config_path = Path(__file__).parent.parent / "header-config.json"
    try:
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        supported_extensions = set()
        for extensions in config.get("file_extensions", {}).values():
            supported_extensions.update(extensions)
        
        supported_files = []
        for file_path in file_paths:
            if file_path.suffix.lower() in supported_extensions:
                supported_files.append(file_path)
        
        return supported_files
    except Exception:
        # Fallback: check common extensions
        common_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.h',
            '.cpp', '.cc', '.cxx', '.hpp', '.cs', '.go', '.php',
            '.html', '.htm', '.css', '.xml', '.sh', '.bash', '.rb', '.pl', '.pm'
        }
        return [f for f in file_paths if f.suffix.lower() in common_extensions]


def main():
    """Main entry point for pre-commit hook."""
    # Get staged files
    staged_files = get_staged_files()
    
    if not staged_files:
        # No staged files, exit successfully
        sys.exit(0)
    
    # Filter to supported files only
    supported_files = filter_supported_files(staged_files)
    
    if not supported_files:
        # No supported files staged, exit successfully
        sys.exit(0)
    
    # Run check-header.py on staged files
    script_dir = Path(__file__).parent
    check_script = script_dir / "check-header.py"
    
    if not check_script.exists():
        print(f"Error: check-header.py not found at {check_script}", file=sys.stderr)
        sys.exit(1)
    
    # Build command
    file_paths = [str(f) for f in supported_files]
    cmd = [sys.executable, str(check_script)] + file_paths
    
    # Run check
    try:
        result = subprocess.run(cmd, cwd=script_dir.parent)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running check-header.py: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

