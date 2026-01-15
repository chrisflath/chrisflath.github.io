#!/bin/bash
# Deploy script for chrisflath.github.io

set -e

echo "=== Academic Website Deployment ==="

# Download profile image
echo "Downloading profile image..."
curl -L -o images/profile.jpg "https://www.wiwi.uni-wuerzburg.de/fileadmin/_processed_/f/9/csm_Chris_b59afa6bd4.jpg"

# Check if image downloaded successfully
if [ -s images/profile.jpg ]; then
    echo "✓ Profile image downloaded"
else
    echo "✗ Failed to download image. Please manually save your photo as images/profile.jpg"
fi

# Initialize git if needed
if [ ! -d .git ]; then
    git init
    git branch -m main
fi

# Configure git
git config user.email "christoph.flath@uni-wuerzburg.de"
git config user.name "Christoph Flath"

# Add remote if not exists
git remote get-url origin 2>/dev/null || git remote add origin https://github.com/chrisflath/chrisflath.github.io.git

# Stage all files
git add .

# Commit
git commit -m "Academic website - $(date +%Y-%m-%d)"

# Push
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "=== Deployment Complete ==="
echo "Your site will be live at: https://chrisflath.github.io"
echo "(May take a few minutes to propagate)"
