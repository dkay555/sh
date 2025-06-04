#!/bin/sh
# Extract the first URL found in the clipboard and save it to a file.
# Usage: ./extract_url_from_clipboard.sh [output_file]
# Default output file is clipboard_url.txt

OUTPUT_FILE=${1:-clipboard_url.txt}

# Determine which clipboard command is available
if command -v pbpaste >/dev/null 2>&1; then
    CLIP_TEXT=$(pbpaste)
elif command -v xclip >/dev/null 2>&1; then
    CLIP_TEXT=$(xclip -o -selection clipboard)
elif command -v xsel >/dev/null 2>&1; then
    CLIP_TEXT=$(xsel --clipboard)
else
    echo "No clipboard utility found (pbpaste, xclip, or xsel required)." >&2
    exit 1
fi

URL=$(printf '%s' "$CLIP_TEXT" | grep -oE 'https?://[^[:space:]]+' | head -n 1)

if [ -z "$URL" ]; then
    echo "No URL found in clipboard." >&2
    exit 1
fi

# Prompt for quantity (Anzahl) and name
printf "Anzahl: "
read -r ANZAHL
printf "Name: "
read -r NAME

# Append in the format "Name,Anzahl,Link" to the output file
printf '%s,%s,%s\n' "$NAME" "$ANZAHL" "$URL" >> "$OUTPUT_FILE"

echo "Entry appended to $OUTPUT_FILE"
