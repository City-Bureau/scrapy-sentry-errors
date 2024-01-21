#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Introductory message
printf "${GREEN}Starting example scrapy project...${NC}\n"

# Enter scrapy project directory
cd example_project

# Trigger scrapy crawl
scrapy crawl example
