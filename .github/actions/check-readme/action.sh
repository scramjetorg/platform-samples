#!/bin/bash

TARGET_FOLDERS=("python" "javascript" "typescript" )
README_FILE="README.md"
REPO_FOLDER="$PWD"
ERROR_COUNT=0

echo "REMEMBER: Your README.md should include a section that starts with # and ends with ___"

check_readme_syntax() {
    content=$(cat "$file")
    if [[ $content == *"#"* && $content != *"___"* ]]; then
        file=$(echo "$file" | sed 's/\/home\/runner\/work\/platform-samples\/platform-samples//')
        echo "Warning: syntax error in $file"
        ((ERROR_COUNT++))
    fi

}

check_readme_files() {
    local folder=$1
    while IFS= read -r -d '' file; do
        check_readme_syntax "$file"
    done < <(find "$folder" -maxdepth 2 -type f -iname "$README_FILE" -print0)
}

check_readme_files_in_folders() {
    for folder in "${TARGET_FOLDERS[@]}"; do
        folder_path="$REPO_FOLDER/$folder"
        if [ -d "$folder_path" ]; then
            check_readme_files "$folder_path"
        else
            echo "Folder $folder not found in repo"
        fi
    done
}

check_readme_files_in_folders
echo "Errors: $ERROR_COUNT"
echo "error_count_readme=$ERROR_COUNT" >> $GITHUB_ENV
