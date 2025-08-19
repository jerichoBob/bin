#!/usr/bin/env python3
"""
Build script for safetensor-info tool

This script creates a standalone binary executable from the Python script
using PyInstaller. The resulting binary can be copied to ~/bin and used
without any Python dependencies.

Usage:
    python build.py [--clean]
    
Requirements:
    Creates and uses a virtual environment to avoid system-wide installs
"""

import argparse
import subprocess
import sys
from pathlib import Path
import shutil
import os


def run_command(cmd, cwd=None, env=None):
    """Run a command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, env=env, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        return False


def setup_venv(script_dir):
    """Set up virtual environment and return paths."""
    venv_dir = script_dir / "venv"
    
    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print("Creating virtual environment...")
        if not run_command([sys.executable, "-m", "venv", str(venv_dir)], cwd=script_dir):
            print("Failed to create virtual environment")
            return None, None
    
    # Determine venv python and pip paths
    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"
    
    return str(venv_python), str(venv_pip)


def check_pyinstaller(venv_python):
    """Check if PyInstaller is available in venv."""
    try:
        subprocess.run([venv_python, "-c", "import PyInstaller"], 
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Build safetensor-info binary")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    args = parser.parse_args()
    
    # Get paths
    script_dir = Path(__file__).parent
    source_file = script_dir / "safetensor_info.py"
    dist_dir = script_dir / "dist"
    build_dir = script_dir / "build"
    spec_file = script_dir / "safetensor_info.spec"
    venv_dir = script_dir / "venv"
    
    # Clean if requested
    if args.clean:
        print("Cleaning build artifacts...")
        for path in [dist_dir, build_dir, spec_file, venv_dir]:
            if path.exists():
                if path.is_file():
                    path.unlink()
                else:
                    shutil.rmtree(path)
        print("Clean complete.")
        return
    
    # Set up virtual environment
    print("Setting up virtual environment...")
    venv_python, venv_pip = setup_venv(script_dir)
    if not venv_python:
        print("Failed to set up virtual environment")
        sys.exit(1)
    
    # Upgrade pip in venv
    print("Upgrading pip in virtual environment...")
    if not run_command([venv_python, "-m", "pip", "install", "--upgrade", "pip"]):
        print("Warning: Failed to upgrade pip")
    
    # Install dependencies in venv
    print("Installing dependencies in virtual environment...")
    if not run_command([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], 
                      cwd=script_dir):
        print("Failed to install dependencies")
        sys.exit(1)
    
    # Check PyInstaller in venv
    if not check_pyinstaller(venv_python):
        print("PyInstaller not found in venv. Installing...")
        if not run_command([venv_python, "-m", "pip", "install", "pyinstaller"]):
            print("Failed to install PyInstaller")
            sys.exit(1)
    
    # Build binary using venv
    print("Building binary with PyInstaller...")
    pyinstaller_cmd = [
        venv_python, "-m", "PyInstaller",
        "--onefile",                    # Create a single executable
        "--name", "safetensor-info",   # Output name
        "--console",                   # Console application
        "--clean",                     # Clean cache
        str(source_file)
    ]
    
    if not run_command(pyinstaller_cmd, cwd=script_dir):
        print("PyInstaller build failed")
        sys.exit(1)
    
    # Check if binary was created
    binary_path = dist_dir / "safetensor-info"
    if not binary_path.exists():
        print(f"Binary not found at {binary_path}")
        sys.exit(1)
    
    print(f"\n✅ Build successful!")
    print(f"Binary created at: {binary_path}")
    print(f"Binary size: {binary_path.stat().st_size / 1024 / 1024:.1f} MB")
    print("\nTo install:")
    print(f"  cp {binary_path} ~/bin/safetensor-info")
    print("  # Or copy to any directory in your PATH")
    
    # Test the binary
    print("\n🧪 Testing binary...")
    test_result = subprocess.run([str(binary_path), "--help"], 
                                capture_output=True, text=True)
    if test_result.returncode == 0:
        print("✅ Binary test passed")
        print("First few lines of --help output:")
        print('\n'.join(test_result.stdout.split('\n')[:3]))
    else:
        print("❌ Binary test failed")
        print(f"Return code: {test_result.returncode}")
        if test_result.stderr:
            print(f"stderr: {test_result.stderr}")


if __name__ == "__main__":
    main()