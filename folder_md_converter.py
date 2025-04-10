#!/usr/bin/env python3
"""
folder_md_converter.py - Convert between folder structures and markdown representations
"""

import os
import sys
import argparse
import re


def scan_directory(directory_path, indent=0, is_last=False, prefix="", ignore_list=None):
    """
    Recursively scan a directory and generate a markdown representation
    
    Args:
        directory_path: Path to the directory to scan
        indent: Current indentation level
        is_last: Whether this is the last item in the parent directory
        prefix: String prefix for the current line
        ignore_list: List of files/directories to ignore
    
    Returns:
        List of strings representing the markdown tree
    """
    result = []
    
    if ignore_list is None:
        ignore_list = ['.git', '__pycache__', 'node_modules', '.DS_Store']
    
    # Get the directory name from the path
    dir_name = os.path.basename(directory_path)
    if not dir_name:  # For root directory
        dir_name = directory_path
    
    # Generate the line prefix based on indent level
    if indent == 0:
        # Root directory
        line = f"{dir_name}/"
    else:
        if is_last:
            line = f"{prefix}└── {dir_name}/"
        else:
            line = f"{prefix}├── {dir_name}/"
    
    result.append(line)
    
    try:
        # Get and sort items in the directory
        items = sorted(os.listdir(directory_path))
        
        # Skip hidden files and ignored directories
        items = [item for item in items if not item.startswith('.') and 
                item not in ignore_list]
        
        # Separate directories and files
        dirs = []
        files = []
        
        for item in items:
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)
        
        # Set prefixes for children items
        if indent > 0:
            if is_last:
                child_prefix = prefix + "    "
            else:
                child_prefix = prefix + "│   "
        else:
            child_prefix = ""
        
        # Process directories first
        for i, d in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and not files
            result.extend(
                scan_directory(
                    os.path.join(directory_path, d),
                    indent + 1,
                    is_last_dir,
                    child_prefix,
                    ignore_list
                )
            )
        
        # Process files
        for i, f in enumerate(files):
            is_last_file = (i == len(files) - 1)
            if is_last_file:
                result.append(f"{child_prefix}└── {f}")
            else:
                result.append(f"{child_prefix}├── {f}")
    
    except (PermissionError, FileNotFoundError):
        result.append(f"{prefix}│   (Permission denied or not found)")
    
    return result


def parse_markdown_tree(md_content):
    """
    Parse the markdown tree content and return a list of paths to create
    
    Args:
        md_content: String containing the markdown tree representation
    
    Returns:
        List of paths to create (files and directories)
    """
    paths = []
    lines = md_content.strip().split('\n')
    
    # Process the root directory first
    if not lines:
        return paths
    
    root = lines[0].rstrip('/')
    current_path = [root]
    
    # For each line after the root
    for line in lines[1:]:
        # Detect the indentation level based on the prefix
        indent_match = re.match(r'^(.*?)[└├]── (.+)$', line)
        if not indent_match:
            continue
            
        prefix, item = indent_match.groups()
        
        # Calculate the indentation level based on the prefix
        level = (len(prefix) // 4) + 1
        
        # Adjust the current path based on the level
        while len(current_path) > level:
            current_path.pop()
        
        # Add the new item to the current path
        is_dir = item.endswith('/')
        if is_dir:
            item = item.rstrip('/')
            current_path.append(item)
            paths.append((os.path.join(*current_path), True))
        else:
            paths.append((os.path.join(*current_path, item), False))
    
    return paths


def create_structure(paths, base_dir='.', dry_run=False):
    """
    Create the folder structure based on the parsed paths
    
    Args:
        paths: List of (path, is_directory) tuples
        base_dir: Base directory to create the structure in
        dry_run: If True, only print what would be created
    
    Returns:
        True if created successfully, False otherwise
    """
    if not paths:
        print("No paths to create. Check the markdown format.")
        return False

    # Print what will be created
    print(f"The following structure will be created in '{base_dir}':")
    for path, is_dir in paths:
        item_type = "directory" if is_dir else "file"
        print(f"  {item_type}: {path}")
    
    # If dry run, stop here
    if dry_run:
        return True
    
    # Confirm creation
    confirm = input("Proceed with creation? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return False
    
    # Create the structure
    for path, is_dir in paths:
        full_path = os.path.join(base_dir, path)
        
        if is_dir:
            os.makedirs(full_path, exist_ok=True)
            print(f"Created directory: {full_path}")
        else:
            # Create parent directories if they don't exist
            parent_dir = os.path.dirname(full_path)
            os.makedirs(parent_dir, exist_ok=True)
            
            # Create empty file
            with open(full_path, 'w') as f:
                pass
            print(f"Created file: {full_path}")
    
    print("Structure created successfully.")
    return True


def folder_to_md(args):
    """
    Convert folder structure to markdown
    """
    # Generate the markdown tree
    tree_lines = scan_directory(args.directory, ignore_list=args.ignore)
    
    # Output the result
    if args.output:
        with open(args.output, 'w') as f:
            for line in tree_lines:
                f.write(line + '\n')
        print(f"Markdown tree saved to {args.output}")
    else:
        for line in tree_lines:
            print(line)


def md_to_folder(args):
    """
    Convert markdown to folder structure
    """
    # Read the markdown content
    if args.input:
        with open(args.input, 'r') as f:
            md_content = f.read()
    else:
        print("Enter the markdown tree representation (Ctrl+D to finish):")
        md_content = sys.stdin.read()
    
    # Parse the markdown tree
    paths = parse_markdown_tree(md_content)
    
    # Create the structure
    create_structure(paths, args.output_dir, args.dry_run)


def main():
    parser = argparse.ArgumentParser(
        description='Convert between folder structures and markdown tree representations'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Folder to markdown parser
    to_md_parser = subparsers.add_parser('to-md', help='Convert folder structure to markdown')
    to_md_parser.add_argument('directory', nargs='?', default='.',
                             help='Directory to convert (default: current directory)')
    to_md_parser.add_argument('-o', '--output', type=str,
                             help='Output file (default: stdout)')
    to_md_parser.add_argument('-i', '--ignore', type=str, nargs='+', 
                             default=['.git', '__pycache__', 'node_modules', '.DS_Store'],
                             help='Files/directories to ignore')
    
    # Markdown to folder parser
    to_folder_parser = subparsers.add_parser('to-folder', help='Convert markdown to folder structure')
    to_folder_parser.add_argument('-i', '--input', type=str,
                                 help='Input markdown file (default: stdin)')
    to_folder_parser.add_argument('-o', '--output-dir', type=str, default='.',
                                 help='Output directory to create structure in (default: current directory)')
    to_folder_parser.add_argument('-d', '--dry-run', action='store_true',
                                 help='Dry run (only show what would be created)')
    
    args = parser.parse_args()
    
    if args.command == 'to-md':
        folder_to_md(args)
    elif args.command == 'to-folder':
        md_to_folder(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()