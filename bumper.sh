#!/bin/sh

# Read the current version from pyproject.toml
CURRENT_VERSION=$(grep -Po '(?<=version = ")[^"]*' pyproject.toml)

# Check if grep was successful
if [ $? -ne 0 ]; then
    echo "Failed to extract the version from pyproject.toml."
    exit 1
fi

# Split the version into major, minor, and patch components
MAJOR=$(echo "$CURRENT_VERSION" | cut -d. -f1)
MINOR=$(echo "$CURRENT_VERSION" | cut -d. -f2)
PATCH=$(echo "$CURRENT_VERSION" | cut -d. -f3)

# Determine which part of the version to increment
case "$1" in
    major)
        MAJOR=$(expr $MAJOR + 1)
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$(expr $MINOR + 1)
        PATCH=0
        ;;
    patch)
        PATCH=$(expr $PATCH + 1)
        ;;
    *)
        echo "Usage: $0 {major|minor|patch}"
        exit 1
        ;;
esac

# Construct the new version
NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# Determine the OS type to use appropriate sed syntax
if [ "$(uname)" = "Darwin" ]; then
    # macOS
    sed -i '' "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
else
    # Linux
    sed -i "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
fi

echo "Version bumped to $NEW_VERSION"