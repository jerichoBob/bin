# SafeTensor Info Tool

A utility to read and display metadata from .safetensor files, compiled to a standalone binary.

## Features

- **Metadata Display**: Shows the `__metadata__` key-value pairs from safetensor files
- **Tensor Information**: Lists all tensors with shapes, dtypes, parameter counts, and sizes
- **File Statistics**: Shows file size, tensor count, and total parameters  
- **Multiple Output Formats**: Both human-readable text and JSON formats
- **Filtering Options**: View metadata-only, tensors-only, or full information
- **Self-contained**: No Python dependencies required after building

## Quick Start

### Build the Binary
```bash
make build
```

### Install to ~/bin
```bash
make install
```

### Usage Examples
```bash
# Basic usage - shows everything in text format
safetensor-info model.safetensors

# JSON output
safetensor-info model.safetensors --format json

# Show only metadata
safetensor-info model.safetensors --metadata-only

# Show only tensor information  
safetensor-info model.safetensors --tensors-only
```

## Development

### Setup Development Environment
```bash
make dev-setup
```

### Build Process
The build process uses PyInstaller to create a standalone binary:

1. **Install Dependencies**: Installs required Python packages
2. **PyInstaller Build**: Creates single-file executable
3. **Testing**: Automatically tests the built binary
4. **Output**: Binary placed in `dist/safetensor-info`

### Manual Build Commands
```bash
# Development setup
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller

# Build binary
python3 build.py

# Clean artifacts
python3 build.py --clean
```

### Available Make Targets
- `make build` - Build the standalone binary
- `make clean` - Clean build artifacts
- `make install` - Build and install to ~/bin  
- `make test` - Build and test the binary
- `make dev-setup` - Install development dependencies

## Binary Details

The resulting binary:
- Is completely self-contained (no Python installation required)
- Typically 15-25MB in size
- Works on the same platform it was built on
- Contains all necessary dependencies embedded within

## File Structure

```
tools/safetensor-info/
├── safetensor_info.py  # Main Python script
├── requirements.txt    # Python dependencies  
├── build.py           # Build script
├── Makefile          # Build automation
└── README.md         # This file
```