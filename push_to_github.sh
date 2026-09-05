#!/bin/bash
# AEGIS One-Command GitHub Pusher
set -e

echo "========================================================"
echo "🛡️  AEGIS Private GitHub Repository Push Script"
echo "========================================================"

if [ -z "$1" ]; then
  echo "Usage: ./push_to_github.sh <GITHUB_REPO_URL_OR_TOKEN_URL>"
  echo ""
  echo "Example with Personal Access Token:"
  echo "  ./push_to_github.sh https://ghp_YOUR_TOKEN@github.com/your-username/aegis-autonomous-system.git"
  echo ""
  echo "Example standard URL (if SSH / Git Credential Manager configured):"
  echo "  ./push_to_github.sh git@github.com:your-username/aegis-autonomous-system.git"
  echo "========================================================"
  read -p "Enter your GitHub Remote URL: " REMOTE_URL
else
  REMOTE_URL="$1"
fi

if [ -z "$REMOTE_URL" ]; then
  echo "❌ Error: Remote URL cannot be empty."
  exit 1
fi

echo "Setting remote origin..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE_URL"

echo "Pushing branch 'main' to private repository..."
git branch -M main
git push -u origin main --force

echo "✅ AEGIS successfully pushed to private repository!"
