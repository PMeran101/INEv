# Remove all files with no extension from the Git index
for file in $(git ls-files | grep -E '^[^.]+$'); do
    git rm --cached "$file"
done

# Remove all .txt files from the Git index
for file in $(git ls-files '*.txt'); do
    git rm --cached "$file"
done