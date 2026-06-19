#!/usr/bin/env bash
# One-time GitHub setup for the LeafGuard repo.
# Usage:
#   1. Edit the two variables below.
#   2. Create an EMPTY repo named "leafguard" on github.com (no README/license).
#   3. Run:  bash setup-github.sh
set -e

GITHUB_USERNAME="YOUR-USERNAME"          # <-- change this
GIT_EMAIL="wiseprojectv@gmail.com"       # <-- change if needed

if [ "$GITHUB_USERNAME" = "YOUR-USERNAME" ]; then
  echo "ERROR: edit GITHUB_USERNAME at the top of this script first."
  exit 1
fi

git init
git config user.name "$GITHUB_USERNAME"
git config user.email "$GIT_EMAIL"

git add .
git commit -m "Initial commit: LeafGuard capstone (backend, frontend, ml, showcase)"
git branch -M main
git remote add origin "https://github.com/${GITHUB_USERNAME}/leafguard.git"
git push -u origin main

echo
echo "Pushed to https://github.com/${GITHUB_USERNAME}/leafguard"
echo "Next: Settings -> Pages -> Source: main, folder /docs  (serves docs/index.html)"
