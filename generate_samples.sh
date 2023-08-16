#!/bin/bash

set -eux

# This script is used to generate sample outputs using different parsing methods.

echo "Generating new pypandoc sample output"
python3 main.py README.md -p pypandoc -o README_parsed_with_pypandoc.csv || {
  echo "An error occurred while generating the pypandoc sample output."
  exit 1
}

echo "Generating new markdown sample output"
python3 main.py README.md -p markdown -o README_parsed_with_markdown.csv || {
  echo "An error occurred while generating the markdown sample output."
  exit 1
}