# ======================================================================================
# STRICTLY CONFIDENTIAL | DLP:OMI::STRICT
# ======================================================================================
# OWNERSHIP NOTICE:
# This source code is the proprietary property of [CUSTOMER].
# Developed by Ominext under MSA.
#
# COPYRIGHT (c) 2025 [CUSTOMER]. ALL RIGHTS RESERVED.
#
# WARNING: This file contains trade secrets and confidential information.
# Unauthorized copying or uploading to public networks  is prohibited.
#
# Project: [PROJECT_CODE]
# Trace ID: unique_file_hash
# ======================================================================================


#!/usr/bin/env python3
"""
Script to enable/disable header check in pre-commit hooks.
"""

import sys
import subprocess
from pathlib import Path


def get_git_root():
    """Get git root directory."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except Exception:
        return None


def is_enabled():
    """Check if header check is enabled."""
    git_root = get_git_root()
    if not git_root:
        return False
    
    # Check for flag file
    flag_file = git_root / ".header-check-enabled"
    if flag_file.exists():
        return True
    
    # Check git config
    try:
        result = subprocess.run(
            ["git", "config", "--get", "header-check.enabled"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().lower() == "true"
    except Exception:
        pass
    
    return False  # Default: disabled


def enable():
    """Enable header check."""
    git_root = get_git_root()
    if not git_root:
        print("Error: Not a git repository", file=sys.stderr)
        return False
    
    # Create flag file
    flag_file = git_root / ".header-check-enabled"
    flag_file.touch()
    
    # Also set git config
    try:
        subprocess.run(
            ["git", "config", "header-check.enabled", "true"],
            check=True
        )
    except Exception:
        pass
    
    print("[OK] Header check enabled")
    return True


def disable():
    """Disable header check."""
    git_root = get_git_root()
    if not git_root:
        print("Error: Not a git repository", file=sys.stderr)
        return False
    
    # Remove flag file
    flag_file = git_root / ".header-check-enabled"
    if flag_file.exists():
        flag_file.unlink()
    
    # Remove git config
    try:
        subprocess.run(
            ["git", "config", "--unset", "header-check.enabled"],
            check=False
        )
    except Exception:
        pass
    
    print("[OK] Header check disabled")
    return True


def status():
    """Show current status."""
    enabled = is_enabled()
    if enabled:
        print("[OK] Header check is ENABLED")
    else:
        print("[X] Header check is DISABLED")
    return enabled


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enable/disable header check in pre-commit hooks")
    parser.add_argument("action", choices=["enable", "disable", "status", "toggle"], 
                       help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "enable":
        enable()
    elif args.action == "disable":
        disable()
    elif args.action == "status":
        status()
    elif args.action == "toggle":
        if is_enabled():
            disable()
        else:
            enable()


if __name__ == "__main__":
    main()

