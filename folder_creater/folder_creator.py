#!/usr/bin/env python3
"""
Project Structure Creator

This script reads a markdown file containing a project structure (typically from a
code block with a tree-like representation) and creates the corresponding folders
and empty files.

Usage:
    python folder_creator.py <markdown_file> <output_directory> [--with-sample-content]

Example:
    python folder_creator.py project_structure.md ./frontier-tactics --with-sample-content
"""

import os
import re
import sys
import argparse
import shutil
from pathlib import Path


def extract_structure_from_markdown(markdown_file):
    """Extract the project structure from a markdown file."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for code blocks (```...```) containing tree structure
    code_blocks = re.findall(r'```(?:\w*)\n(.*?)\n```', content, re.DOTALL)
    
    # If no code blocks, try to find structure in normal text
    if not code_blocks:
        lines = content.split('\n')
        structure_lines = []
        for line in lines:
            if re.match(r'^[\s│├└─┬┼┤┴┌┐┘┗━┃┣┗┻╋┫┻╭╮╯╰]+\w+.*$', line) or '/' in line:
                structure_lines.append(line)
        if structure_lines:
            return '\n'.join(structure_lines)
            
    # Extract structure from code blocks
    for block in code_blocks:
        if '/' in block or '\\' in block:  # Simple check to see if it looks like a file structure
            return block
            
    # As a fallback, try to find any lines containing file paths
    all_structure_lines = []
    lines = content.split('\n')
    for line in lines:
        if re.search(r'[│├└─┬┼┤┴┌┐┘┗━┃┣┗┻╋┫┻╭╮╯╰]|\w+\/\w+|[\w-]+\.\w+', line):
            all_structure_lines.append(line)
    
    return '\n'.join(all_structure_lines)


def parse_structure(structure_text):
    """Parse the structure text and return a list of files and folders."""
    files_and_folders = []
    lines = structure_text.split('\n')
    
    for line in lines:
        # Remove leading whitespace, │, ├, └, ─, and similar characters
        cleaned_line = re.sub(r'^[│├└─┬┼┤┴┌┐┘┗━┃┣┗┻╋┫┻╭╮╯╰\s]+', '', line)
        
        # Skip empty lines and lines without valid content
        if not cleaned_line or cleaned_line.startswith('#'):
            continue
            
        # Check if it's a file path (contains '/' or '.')
        if '/' in cleaned_line or '.' in cleaned_line:
            # Replace Windows-style paths with Unix-style
            cleaned_line = cleaned_line.replace('\\', '/')
            # Remove any trailing comments
            cleaned_line = re.sub(r'\s+#.*$', '', cleaned_line)
            # Add to our list
            files_and_folders.append(cleaned_line)
    
    return files_and_folders


def create_structure(output_dir, files_and_folders, with_sample_content=False):
    """Create the folder structure and files in the output directory."""
    # Create the base output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Sample content for Python files
    python_template = '''"""
{module_name}
"""

'''
    
    created_items = []
    
    for item in files_and_folders:
        # Handle both folder/ and file.ext formats
        full_path = os.path.join(output_dir, item)
        
        # Create directory path
        dir_path = os.path.dirname(full_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            if dir_path not in created_items:
                created_items.append(dir_path)
                print(f"Created directory: {dir_path}")
        
        # If item ends with / or \, it's a directory
        if item.endswith('/') or item.endswith('\\'):
            if not os.path.exists(full_path):
                os.makedirs(full_path, exist_ok=True)
                created_items.append(full_path)
                print(f"Created directory: {full_path}")
        else:
            # It's a file - create it if it doesn't exist
            if not os.path.exists(full_path):
                # Create with sample content if requested
                if with_sample_content and full_path.endswith('.py'):
                    module_name = os.path.basename(full_path).split('.')[0].replace('_', ' ').title()
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(python_template.format(module_name=module_name))
                else:
                    # Just create an empty file
                    with open(full_path, 'w', encoding='utf-8') as f:
                        pass
                
                created_items.append(full_path)
                print(f"Created file: {full_path}")
    
    return created_items


def main():
    parser = argparse.ArgumentParser(description='Create a folder structure from a Markdown file.')
    parser.add_argument('markdown_file', help='Path to the markdown file containing the structure')
    parser.add_argument('output_directory', help='Directory where the structure will be created')
    parser.add_argument('--with-sample-content', action='store_true', 
                        help='Add sample content to Python files')
    
    args = parser.parse_args()
    
    try:
        structure_text = extract_structure_from_markdown(args.markdown_file)
        if not structure_text:
            print("Could not find a valid folder structure in the markdown file.")
            return 1
        
        files_and_folders = parse_structure(structure_text)
        if not files_and_folders:
            print("No valid files or folders found in the structure.")
            return 1
        
        created_items = create_structure(args.output_directory, files_and_folders, args.with_sample_content)
        
        print(f"\nCreated {len(created_items)} items in {args.output_directory}")
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
