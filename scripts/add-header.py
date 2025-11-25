
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
Script to add header to code files.
Supports auto-fix mode to automatically add headers when missing.
"""

import json
import sys
import importlib.util
from pathlib import Path
from typing import Optional

# Import hash generation function from same directory
# Use importlib because filename has hyphen
_script_dir = Path(__file__).parent
spec = importlib.util.spec_from_file_location("generate_hash", _script_dir / "generate-hash.py")
generate_hash_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_hash_module)
generate_file_hash = generate_hash_module.generate_file_hash


class HeaderManager:
    """Manages header operations for code files."""
    
    def __init__(self, config_path: str = "header-config.json"):
        """Initialize with config file."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.templates_dir = Path(__file__).parent.parent / "templates"
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _get_language_from_extension(self, file_path: Path) -> Optional[str]:
        """Determine language from file extension."""
        ext = file_path.suffix.lower()
        for lang, extensions in self.config.get("file_extensions", {}).items():
            if ext in extensions:
                return lang
        return None
    
    def _load_template(self, language: str) -> Optional[str]:
        """Load template for given language."""
        template_path = self.templates_dir / f"{language}.template"
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading template for {language}: {e}", file=sys.stderr)
            return None
    
    def _has_header(self, content: str) -> bool:
        """Check if file already has header."""
        # Check for key markers in header
        markers = [
            "STRICTLY CONFIDENTIAL | DLP:OMI::STRICT",
            "OWNERSHIP NOTICE:",
            "Trace ID:"
        ]
        content_upper = content.upper()
        return all(marker.upper() in content_upper for marker in markers)
    
    def _generate_header(self, file_path: Path, language: str) -> Optional[str]:
        """Generate header content for a file."""
        template = self._load_template(language)
        if not template:
            return None
        
        # Generate file hash
        file_hash = generate_file_hash(file_path)
        if not file_hash:
            return None
        
        # Replace placeholders
        header = template.replace("{CUSTOMER}", self.config.get("customer", "[CUSTOMER]"))
        header = header.replace("{YEAR}", str(self.config.get("copyright_year", "2025")))
        header = header.replace("{PROJECT_CODE}", self.config.get("project_code", "[PROJECT_CODE]"))
        header = header.replace("{FILE_HASH}", file_hash)
        
        return header
    
    def add_header(self, file_path: Path, force: bool = False) -> bool:
        """
        Add header to a file.
        
        Args:
            file_path: Path to the file
            force: If True, replace existing header
            
        Returns:
            bool: True if header was added/replaced, False otherwise
        """
        # Resolve path to handle relative paths correctly
        if not file_path.is_absolute():
            file_path = file_path.resolve()
        
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            print(f"Current working directory: {Path.cwd()}", file=sys.stderr)
            return False
        
        # Check if file is binary
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(8192)
                if b'\x00' in chunk:
                    print(f"Skipping binary file: {file_path}")
                    return False
        except Exception:
            return False
        
        # Get language
        language = self._get_language_from_extension(file_path)
        if not language:
            print(f"Skipping unsupported file type: {file_path}")
            return False
        
        # Read current content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"Skipping file with encoding issues: {file_path}")
            return False
        except Exception as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            return False
        
        # Check if header already exists
        if self._has_header(content) and not force:
            print(f"Header already exists in: {file_path}")
            return False
        
        # Generate header
        header = self._generate_header(file_path, language)
        if not header:
            print(f"Error generating header for: {file_path}", file=sys.stderr)
            return False
        
        # Remove existing header if force
        if force and self._has_header(content):
            # Try to find and remove old header (simple approach: remove first 20 lines if they contain header markers)
            lines = content.split('\n')
            header_end = 0
            for i, line in enumerate(lines[:20]):
                if "Trace ID:" in line or "======================================================================" in line:
                    header_end = i + 1
                    break
            if header_end > 0:
                content = '\n'.join(lines[header_end:])
        
        # Add header
        new_content = header.rstrip() + '\n\n' + content.lstrip()
        
        # Write back
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            # Use simple checkmark to avoid encoding issues on Windows
            print(f"[OK] Added header to: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}", file=sys.stderr)
            return False


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Add header to code files")
    parser.add_argument("files", nargs="+", help="Files to add header to")
    parser.add_argument("--config", default="header-config.json", help="Path to config file")
    parser.add_argument("--force", action="store_true", help="Force replace existing header")
    
    args = parser.parse_args()
    
    manager = HeaderManager(args.config)
    
    success_count = 0
    for file_path_str in args.files:
        # Convert to Path and resolve relative to current directory
        file_path = Path(file_path_str).resolve()
        if manager.add_header(file_path, force=args.force):
            success_count += 1
    
    if success_count == 0:
        sys.exit(1)
    
    print(f"\nSuccessfully processed {success_count} file(s)")


if __name__ == "__main__":
    main()

