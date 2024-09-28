#!/bin/bash

# Navigate to the INEv directory
cd INEv

# Remove all files with no extension from the Git index within the INEv directory
for file in $(git ls-files | grep -E '^[^.]+$' | grep '^INEv/'); do
    git rm --cached "$file"
done

# Remove all .txt files from the Git index within the INEv directory
for file in $(git ls-files 'INEv/*.txt'); do
    git rm --cached "$file"
done

# Optionally, navigate back to the root directory
cd ..
