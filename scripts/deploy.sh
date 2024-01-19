#!/bin/bash

# Check if 'twine' is installed
if ! command -v twine &>/dev/null; then
  echo "Error: 'twine' is not installed. Please install it using 'pip install twine'."
  exit 1
fi

# Upload the contents of the 'dist' directory using 'twine'
echo "Uploading Python package to the repository..."
twine upload dist/*

# Check the exit status of 'twine' upload
if [ $? -eq 0 ]; then
  echo "Deployment completed successfully."
else
  echo "Error: Deployment failed."
  exit 1
fi
