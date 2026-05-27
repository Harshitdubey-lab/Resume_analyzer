#!/usr/bin/env bash
# Render Build Script
# This runs during the build phase on Render

set -o errexit  # Exit on error

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Create required directories
mkdir -p uploads
mkdir -p artifacts
