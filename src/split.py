import argparse
import os
from termcolor import colored
import re


def split_book(file_path):
    with open(file_path, "r") as f:
        lines_list = [x.strip() for x in f.readlines()]
    lines = "\n".join(lines_list)
    print(f"{colored('Processing file', 'green')}: {file_path}")
    # Count and print the number of lines in the file
    num_lines = len(lines_list)
    print(f"{colored('Number of lines', 'blue')}: {num_lines}")

    # chaps = re.split("^#.*$", lines, flags=re.MULTILINE)
    # Split the text into chapters based on markdown headers
    # # represents a section and ## represents chapters inside that section
    chaps = []
    current_chapter = ""

    for line in lines_list:
        # Check if the line is a chapter header (second level - ##)
        if line.startswith('## '):
            # If we have content in the current chapter, add it to the list
            if current_chapter.strip():
                chaps.append(current_chapter.strip())
            # Start a new chapter
            current_chapter = line + "\n"
        else:
            # Add the line to the current chapter
            current_chapter += line + "\n"
    
    # Add the last chapter if it has content
    if current_chapter.strip():
        chaps.append(current_chapter.strip())

    print(f"{colored('Number of chapters', 'blue')}: {len(chaps)}")
    for i, chap in enumerate(chaps):
        print(f"{colored(f'Chapter {i+1}', 'yellow')}: {chap[:20]}")

    # Create a directory to store split chapters
    input_dir = os.path.dirname(file_path)
    input_filename = os.path.basename(file_path)
    base_name = os.path.splitext(input_filename)[0]
    
    # Create split_chapters directory if it doesn't exist
    split_dir = os.path.join(input_dir, "split_chapters")
    if not os.path.exists(split_dir):
        os.makedirs(split_dir)
        print(f"{colored('Created directory', 'green')}: {split_dir}")
    
    # Create backup directory with date if needed
    import datetime
    import json
    import shutil
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    backup_dir = os.path.join(input_dir, f"backup_{today}")
    backup_metadata = []
    
    # Save each chapter to a separate file
    for i, chapter in enumerate(chaps):
        # Create filename for the chapter
        chapter_filename = f"{base_name}_chapter_{i+1}.md"
        chapter_path = os.path.join(split_dir, chapter_filename)
        
        # Check if file exists and create backup if needed
        if os.path.exists(chapter_path):
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
                print(f"{colored('Created backup directory', 'green')}: {backup_dir}")
            
            # Create backup of existing file
            backup_file = os.path.join(backup_dir, chapter_filename)
            shutil.copy2(chapter_path, backup_file)
            
            # Add to backup metadata
            backup_metadata.append({
                "original_file": chapter_path,
                "backup_file": backup_file,
                "timestamp": datetime.datetime.now().isoformat()
            })
        
        # Write chapter to file
        with open(chapter_path, "w") as f:
            f.write(chapter)
        
        print(f"{colored('Saved chapter', 'green')} {i+1} to {chapter_path}")
    
    # Save backup metadata if any backups were created
    if backup_metadata:
        metadata_path = os.path.join(backup_dir, f"{base_name}_backup_metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(backup_metadata, f, indent=2)
        print(f"{colored('Saved backup metadata', 'green')}: {metadata_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    # parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    split_book(args.input)


if __name__ == "__main__":
    main()
