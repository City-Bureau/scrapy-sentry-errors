#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Introductory message
printf "${GREEN}Starting project setup...${NC}\n"
echo "This script will set up your development environment for the project."

# Check if pipenv is installed
if ! command -v pipenv &> /dev/null
then
    printf "${RED}pipenv could not be found.${NC} Please install pipenv from the official website:\n"
    echo "https://pipenv.pypa.io/en/latest/#install-pipenv-today"
    exit 1
else
    printf "${GREEN}pipenv is already installed.${NC}\n"
fi

# Inform about Sentry DSN requirement
printf "${YELLOW}A Sentry DSN is required for local development.${NC}\n"

# Check for .env file and SENTRY_DSN
if [ ! -f .env ]; then
    echo ".env file does not exist. Creating one."
    touch .env
fi

if grep -q "SENTRY_DSN" .env; then
    printf "${GREEN}SENTRY_DSN found in .env file.${NC}\n"
else
    echo "SENTRY_DSN not found in your .env file."
    read -p "Please enter your Sentry DSN: " sentry_dsn
    echo "SENTRY_DSN=$sentry_dsn" >> .env
    printf "${GREEN}SENTRY_DSN added to .env file.${NC}\n"
fi

# Install project dependencies including dev dependencies
printf "${GREEN}Installing project dependencies...${NC}\n"
pipenv install --dev --python 3.8

# Set up pre-commit hook
printf "${GREEN}Setting up pre-commit hooks...${NC}\n"
pipenv run pre-commit install

# Final message
printf "${GREEN}Project setup is complete! You can now start development.${NC}\n"

# Start pipenv shell session
printf "${GREEN}Starting pipenv shell session...${NC}\n"
pipenv shell
