#!/bin/bash

TARGET_FOLDERS=("python" "javascript" "typescript" )
PACKAGE_FILE="package.json"
REPO_FOLDER="$PWD"
ERROR_COUNT=0


check_json_file_syntax() {
    file="$1"
    
    if [ ! -f "$file" ]; then
        echo "Error: File $file does not exist."
        return 1
    fi
    
    required_fields=("name" "description" "keywords" "repository")
    missing_fields=()
    empty_fields=()
    
    for field in "${required_fields[@]}"; do
        if ! jq --exit-status ".$field" "$file" >/dev/null 2>&1; then
            missing_fields+=("$field")
        else
            # check if field is empty
            if [ -z "$(jq -r ".$field" "$file")" ]; then
                empty_fields+=("$field")
            fi
        fi
    done
    
    # check if repository url field exists and is not empty
    if ! jq --exit-status '.repository.url' "$file" >/dev/null 2>&1; then
        missing_fields+=("repository.url")
    else
        # check if repository url field is a valid URL
        if ! echo "$(jq -r '.repository.url' "$file")" | grep -P '^https?://.+' >/dev/null 2>&1; then
            empty_fields+=("repository.url is not a valid URL")
        fi
    fi


    if [ ${#empty_fields[@]} -gt 0 ]; then
        echo "Warning: The following fields are empty or invalid in $file:"
        ((ERROR_COUNT++))

        for field in "${empty_fields[@]}"; do
            echo "- $field"
        done
    fi

    if [ ${#missing_fields[@]} -gt 0 ]; then
        echo "Warning: File $file does not contain the required fields:"
        ((ERROR_COUNT++))

        for field in "${missing_fields[@]}"; do
            echo "- $field"
        done
    fi
    
    if [ ${#missing_fields[@]} -gt 0 ] || [ ${#empty_fields[@]} -gt 0 ]; then
        echo ""  # adds a new line for better readability
        return 1
    fi

    return 0
}


check_json_file_syntax() {
    file="$1"
    
    if [ ! -f "$file" ]; then
        echo "Error: File $file does not exist."
        return 1
    fi
    
    required_fields=("name" "description" "keywords" "repository")
    missing_fields=()
    
    for field in "${required_fields[@]}"; do
        if ! jq --exit-status ".$field" "$file" >/dev/null 2>&1; then
            missing_fields+=("$field")
        fi
    done
    
    if [ ${#missing_fields[@]} -gt 0 ]; then
        file=$(echo "$file" | sed 's/\/home\/runner\/work\/platform-samples\/platform-samples//')
        echo "Warning: File $file does not contain the required fields:"
        ((ERROR_COUNT++))

        for field in "${missing_fields[@]}"; do
            echo "- $field"
        done
        
        return 1
    fi
    
    return 0
}


check_package_files() {
    local folder=$1
    while IFS= read -r -d '' file; do
        check_json_file_syntax "$file"
    done < <(find "$folder" -maxdepth 2 -type f -iname "$PACKAGE_FILE" -print0)
}

check_package_files_in_folders() {
    for folder in "${TARGET_FOLDERS[@]}"; do
        folder_path="$REPO_FOLDER/$folder"
        if [ -d "$folder_path" ]; then
            check_package_files "$folder_path"
        else
            echo "Folder $folder not found in repo"
        fi
    done
}


check_package_files_in_folders
echo "Errors: $ERROR_COUNT"
echo "error_count_package=$ERROR_COUNT" >> $GITHUB_ENV

