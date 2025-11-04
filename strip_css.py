#!/usr/bin/env python3

import os
import sys
import re

# Regex to remove style="..." or style='...'
STYLE_RE = re.compile(r'\sstyle=(["\']).*?\1', re.IGNORECASE)

def strip_styles_from_file(input_path, output_path):
    """Read an HTML file line by line, remove style attributes, write to output."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(input_path, 'r', encoding='utf-8') as fin, \
         open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            new_line = STYLE_RE.sub('', line)
            fout.write(new_line)

def main():
    if len(sys.argv) != 3:
        print("Usage: python strip_styles.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(input_dir):
        print(f"Error: input directory '{input_dir}' does not exist.")
        sys.exit(1)

    # Check for at least one .html file
    has_html = any(
        fname.lower().endswith('.html')
        for root, _, files in os.walk(input_dir)
        for fname in files
    )
    if not has_html:
        print(f"No .html files found in '{input_dir}'")
        sys.exit(0)

    # Exit if output_dir exists and is not empty
    if os.path.exists(output_dir) and os.listdir(output_dir):
        print(f"Error: output directory '{output_dir}' exists and is not empty.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # Process files recursively
    for root, _, files in os.walk(input_dir):
        for fname in files:
            if fname.lower().endswith('.html'):
                input_path = os.path.join(root, fname)
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)
                strip_styles_from_file(input_path, output_path)
                print(f"Processed: {rel_path}")

    print("All HTML files processed successfully.")

if __name__ == "__main__":
    main()
