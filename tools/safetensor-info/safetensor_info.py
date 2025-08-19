#!/usr/bin/env python3
"""
SafeTensor Info - A utility to read and display metadata from .safetensor files

This utility reads safetensor files and displays:
- File metadata (from __metadata__ key if present)
- Tensor information (names, shapes, dtypes, sizes)
- Overall file statistics

Usage:
    safetensor-info <file.safetensors> [--format json|text] [--metadata-only] [--tensors-only]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from safetensors import safe_open
except ImportError:
    print("Error: safetensors library not found.", file=sys.stderr)
    print("Install with: pip install safetensors", file=sys.stderr)
    sys.exit(1)


def format_bytes(bytes_count: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} PB"


def get_safetensor_info(file_path: Path) -> Dict[str, Any]:
    """Extract metadata and tensor info from safetensor file."""
    info = {
        'file_path': str(file_path),
        'file_size': file_path.stat().st_size,
        'metadata': None,
        'tensors': {},
        'tensor_count': 0,
        'total_parameters': 0
    }
    
    # Try different frameworks in order of preference
    frameworks_to_try = ["pt", "tf", "flax", "numpy"]
    
    last_error = None
    for framework in frameworks_to_try:
        try:
            with safe_open(file_path, framework=framework) as f:
                # Get metadata if present
                metadata = f.metadata()
                if metadata:
                    info['metadata'] = dict(metadata)
                
                # Get tensor information
                tensor_info = {}
                total_params = 0
                
                for key in f.keys():
                    tensor = f.get_tensor(key)
                    shape = list(tensor.shape)
                    dtype = str(tensor.dtype)
                    numel = tensor.numel()
                    
                    tensor_info[key] = {
                        'shape': shape,
                        'dtype': dtype,
                        'parameters': numel,
                        'size_bytes': tensor.nbytes
                    }
                    total_params += numel
                
                info['tensors'] = tensor_info
                info['tensor_count'] = len(tensor_info)
                info['total_parameters'] = total_params
                break  # Success, exit the loop
                
        except Exception as e:
            last_error = e
            continue  # Try next framework
    
    else:
        # All frameworks failed
        raise RuntimeError(f"Error reading safetensor file with all frameworks. Last error: {last_error}")
    
    return info


def format_as_json(info: Dict[str, Any], indent: int = 2) -> str:
    """Format info as pretty JSON."""
    # Make a copy for JSON serialization
    json_info = dict(info)
    json_info['file_size_human'] = format_bytes(info['file_size'])
    json_info['total_parameters_human'] = f"{info['total_parameters']:,}"
    
    return json.dumps(json_info, indent=indent, ensure_ascii=False)


def format_as_text(info: Dict[str, Any]) -> str:
    """Format info as human-readable text."""
    lines = []
    
    # File info
    lines.append(f"SafeTensor File: {info['file_path']}")
    lines.append(f"File Size: {format_bytes(info['file_size'])} ({info['file_size']:,} bytes)")
    lines.append(f"Tensor Count: {info['tensor_count']}")
    lines.append(f"Total Parameters: {info['total_parameters']:,}")
    lines.append("")
    
    # Metadata section
    if info['metadata']:
        lines.append("=== METADATA ===")
        for key, value in info['metadata'].items():
            lines.append(f"{key}: {value}")
        lines.append("")
    else:
        lines.append("=== METADATA ===")
        lines.append("No metadata found")
        lines.append("")
    
    # Tensors section
    if info['tensors']:
        lines.append("=== TENSORS ===")
        for name, tensor_info in info['tensors'].items():
            shape_str = "×".join(map(str, tensor_info['shape']))
            lines.append(f"{name}:")
            lines.append(f"  Shape: [{shape_str}]")
            lines.append(f"  Dtype: {tensor_info['dtype']}")
            lines.append(f"  Parameters: {tensor_info['parameters']:,}")
            lines.append(f"  Size: {format_bytes(tensor_info['size_bytes'])}")
            lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Read and display metadata from .safetensor files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  safetensor-info model.safetensors
  safetensor-info model.safetensors --format json
  safetensor-info model.safetensors --metadata-only
  safetensor-info model.safetensors --tensors-only --format json
        """
    )
    
    parser.add_argument('file', type=Path, help='Path to safetensor file')
    parser.add_argument('--format', choices=['json', 'text'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--metadata-only', action='store_true',
                       help='Show only metadata information')
    parser.add_argument('--tensors-only', action='store_true',
                       help='Show only tensor information')
    
    args = parser.parse_args()
    
    # Validate file
    if not args.file.exists():
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    if not args.file.is_file():
        print(f"Error: '{args.file}' is not a file.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Get safetensor info
        info = get_safetensor_info(args.file)
        
        # Filter output based on flags
        if args.metadata_only:
            filtered_info = {
                'file_path': info['file_path'],
                'metadata': info['metadata']
            }
        elif args.tensors_only:
            filtered_info = {
                'file_path': info['file_path'],
                'tensors': info['tensors'],
                'tensor_count': info['tensor_count'],
                'total_parameters': info['total_parameters']
            }
        else:
            filtered_info = info
        
        # Output in requested format
        if args.format == 'json':
            print(format_as_json(filtered_info))
        else:
            if args.metadata_only and filtered_info['metadata']:
                print("=== METADATA ===")
                for key, value in filtered_info['metadata'].items():
                    print(f"{key}: {value}")
            elif args.metadata_only:
                print("No metadata found")
            elif args.tensors_only:
                print("=== TENSORS ===")
                for name, tensor_info in filtered_info['tensors'].items():
                    shape_str = "×".join(map(str, tensor_info['shape']))
                    print(f"{name}:")
                    print(f"  Shape: [{shape_str}]")
                    print(f"  Dtype: {tensor_info['dtype']}")
                    print(f"  Parameters: {tensor_info['parameters']:,}")
                    print(f"  Size: {format_bytes(tensor_info['size_bytes'])}")
                    print()
            else:
                print(format_as_text(filtered_info))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()