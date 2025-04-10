# Folder MD Converter

A versatile Python utility that converts between folder structures and markdown tree representations.

## Overview

Folder MD Converter is a bidirectional tool that allows you to:

1. **Convert folder structures to markdown trees** (`to-md` mode)
2. **Convert markdown trees to folder structures** (`to-folder` mode)

This tool is useful for documenting project structures, generating scaffolding for new projects, and creating visual representations of directory hierarchies.

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone https://github.com/yourusername/folder-md-converter.git
   ```

2. Make the script executable:
   ```bash
   chmod +x folder_md_converter.py
   ```

3. No external dependencies required - it uses only Python standard library modules.

## Usage

### Converting Folders to Markdown

```bash
./folder_md_converter.py to-md [DIRECTORY] [-o OUTPUT_FILE] [-i IGNORE_LIST]
```

**Arguments:**
- `DIRECTORY`: The directory to convert (default: current directory)
- `-o, --output`: Output file (default: stdout)
- `-i, --ignore`: Files/directories to ignore (default: `.git`, `__pycache__`, `node_modules`, `.DS_Store`)

**Example:**
```bash
./folder_md_converter.py to-md my_project -o project_structure.md
```

### Converting Markdown to Folders

```bash
./folder_md_converter.py to-folder [-i INPUT_FILE] [-o OUTPUT_DIR] [-d]
```

**Arguments:**
- `-i, --input`: Input markdown file (default: stdin)
- `-o, --output-dir`: Output directory to create structure in (default: current directory)
- `-d, --dry-run`: Dry run mode (only show what would be created)

**Example:**
```bash
./folder_md_converter.py to-folder -i project_structure.md -o new_project/
```

## Features

- **Bidirectional Conversion**: Convert from folders to markdown and vice versa
- **Directory Visualization**: Clear visual representation of folder hierarchies
- **Project Scaffolding**: Quickly create project structures from templates
- **Dry Run Mode**: Preview changes before making them
- **Ignore List**: Skip specified files and directories
- **Interactive**: Confirmation prompts to prevent accidental changes
- **Stdin/Stdout Support**: Pipe inputs and outputs for shell scripting

## Markdown Format

The script generates and expects markdown in the following format:

```
root_directory/
├── subdirectory1/
│   ├── file1.txt
│   └── file2.txt
└── subdirectory2/
    ├── file3.txt
    └── subdirectory3/
        └── file4.txt
```

- Directories end with a `/`
- Files are represented without trailing characters
- The tree uses standard ASCII tree characters (`├──`, `└──`, `│`)

## Examples

### Document a Project Structure

```bash
./folder_md_converter.py to-md my_python_project -o project_docs/structure.md
```

### Create a New Project from a Template

```bash
./folder_md_converter.py to-folder -i template.md -o new_project/
```

### Use with Pipes in Shell Scripts

```bash
cat template.md | ./folder_md_converter.py to-folder -o new_project/
```

### Generate Multiple Projects from the Same Template

```bash
for project in project1 project2 project3; do
    ./folder_md_converter.py to-folder -i template.md -o $project/
done
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
