#!/bin/bash

# Remove existing distribution files in the dist directory
echo "Cleaning the dist directory..."
rm -rf dist/*

# Build the Python package
echo "Building the Python package..."
python -m build

echo "Build completed."
