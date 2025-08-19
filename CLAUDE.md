# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of utility commands intended for a ~/bin directory. The repository currently contains only basic setup files (README.md and LICENSE) and is ready for adding utility scripts.

## Repository Structure

This is a utility scripts repository with two types of tools:

### Simple Scripts (root directory)
- Executable files (shell scripts, simple Python scripts, etc.)
- Self-contained utilities with minimal dependencies
- Named descriptively for their function

### Complex Tools (tools/ directory)
- Python tools with external dependencies in `tools/toolname/` subdirectories
- Each tool has its own `requirements.txt`, build scripts, and documentation
- Built as standalone binaries using PyInstaller for distribution
- Example: `tools/safetensor-info/` - utility for reading safetensor file metadata

## Development Workflow

### Simple Scripts
- Add new utility scripts directly to the root directory
- Make scripts executable with `chmod +x scriptname`
- Test scripts locally before committing
- Scripts should be portable and work across different environments

### Complex Tools
- Create new directory under `tools/toolname/`
- Add Python source, `requirements.txt`, build scripts
- Use `make build` or `python build.py` to create standalone binary
- Install binary to ~/bin with `make install`

## Common Tasks

### Simple Scripts
- **Make a script executable**: `chmod +x scriptname`
- **Test a script**: `./scriptname` (run directly from repository root)
- **Install to ~/bin**: Copy or symlink individual scripts to ~/bin directory

### Complex Tools
- **Build a tool**: `cd tools/toolname && make build`
- **Install a tool**: `cd tools/toolname && make install` 
- **Clean build artifacts**: `cd tools/toolname && make clean`
- **Development setup**: `cd tools/toolname && make dev-setup`

## Script Guidelines

- Scripts should include appropriate shebang lines (#!/bin/bash, #!/usr/bin/env python3, etc.)
- Include basic usage information or help flags where appropriate
- Keep dependencies minimal and well-documented
- Scripts should handle errors gracefully