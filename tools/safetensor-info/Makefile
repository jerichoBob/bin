# Makefile for safetensor-info tool
# Creates a standalone binary from Python source

.PHONY: build clean install test help

BINARY_NAME = safetensor-info
DIST_DIR = dist
BUILD_DIR = build
SPEC_FILE = safetensor_info.spec

# Default target
build:
	@echo "Building $(BINARY_NAME) binary..."
	python3 build.py
	@echo "Build complete. Binary at: $(DIST_DIR)/$(BINARY_NAME)"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	python3 build.py --clean
	@echo "Clean complete."

# Install to ~/bin
install: build
	@echo "Installing $(BINARY_NAME) to ~/bin..."
	@mkdir -p ~/bin
	cp $(DIST_DIR)/$(BINARY_NAME) ~/bin/$(BINARY_NAME)
	@echo "Installed to ~/bin/$(BINARY_NAME)"
	@echo "Make sure ~/bin is in your PATH"

# Test the binary
test: build
	@echo "Testing binary..."
	$(DIST_DIR)/$(BINARY_NAME) --help

# Quick development setup
dev-setup:
	@echo "Setting up development environment..."
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install -r requirements.txt
	./venv/bin/python -m pip install pyinstaller
	@echo "Development setup complete"
	@echo "Virtual environment created in ./venv"

# Show help
help:
	@echo "Available targets:"
	@echo "  build      - Build the standalone binary"
	@echo "  clean      - Clean build artifacts"
	@echo "  install    - Build and install to ~/bin"
	@echo "  test       - Build and test the binary"
	@echo "  dev-setup  - Install development dependencies"
	@echo "  help       - Show this help message"