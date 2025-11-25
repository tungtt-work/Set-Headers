
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
Script to generate SHA256 hash from file content.
Used for generating unique Trace ID in file headers.
"""

import hashlib
import sys
from pathlib import Path


def generate_file_hash(file_path):
    """
    Generate SHA256 hash from file content.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: SHA256 hash in hexadecimal format (64 characters)
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            hash_obj = hashlib.sha256(content)
            return hash_obj.hexdigest()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return None


def generate_content_hash(content):
    """
    Generate SHA256 hash from content string or bytes.
    
    Args:
        content: String or bytes content
        
    Returns:
        str: SHA256 hash in hexadecimal format (64 characters)
    """
    if isinstance(content, str):
        content = content.encode('utf-8')
    hash_obj = hashlib.sha256(content)
    return hash_obj.hexdigest()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate-hash.py <file_path>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    hash_value = generate_file_hash(file_path)
    if hash_value:
        print(hash_value)
    else:
        sys.exit(1)

