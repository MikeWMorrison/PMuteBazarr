import sys
import os
import logging
import re
import shutil
import argparse

def parse_srt_timecode(timecode):
    """Convert SRT timecode to seconds."""
    hours, minutes, seconds, milliseconds = map(float, re.split('[:,]', timecode))
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000

def load_bad_words():
    """Load bad words from the filter.txt file and create regex patterns."""
    words = []
    patterns = []
    
    # Determine the path to filter.txt
    if os.path.exists('/config/scripts'):
        # Production environment
        file_path = '/config/scripts/filter.txt'
    else:
        # Test environment
        file_path = os.path.join(os.getcwd(), 'filter.txt')
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            if word:  # Skip empty lines
                words.append(word)
                # Create regex pattern
                pattern = r'\b'
                for char in word:
                    if char == '*':
                        pattern += r'\w*'
                    else:
                        pattern += f'[{re.escape(char)}]'
                pattern += r'\b'
                patterns.append(re.compile(pattern, re.IGNORECASE))
    
    return words, patterns

def process_subtitle(directory, subtitle_file):
    # Determine the log file path based on the environment
    if os.path.exists('/config/scripts'):
        # Production environment
        log_file = '/config/scripts/subtitle_processing.log'
        filter_file = '/config/scripts/filter.txt'
    else:
        # Test environment
        log_file = os.path.join(os.getcwd(), 'subtitle_processing.log')
        filter_file = os.path.join(os.getcwd(), 'filter.txt')

    # Configure logging
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Log all passed arguments
    logging.info(f"Arguments: directory={directory}, subtitle_file={subtitle_file}")

    try:
        # Check if the subtitle file exists
        full_subtitle_path = os.path.join(directory, subtitle_file)
        if not os.path.exists(full_subtitle_path):
            raise FileNotFoundError(f"Subtitle file not found: {full_subtitle_path}")

        # Load bad words and patterns
        words, patterns = load_bad_words()

        # Make a backup of the original .srt file
        backup_file = full_subtitle_path + '.bak'
        shutil.copyfile(full_subtitle_path, backup_file)

        # Process the subtitle file
        with open(full_subtitle_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        modified_lines = []
        edl_lines = []
        for i in range(len(lines)):
            modified_line = lines[i]
            for word, pattern in zip(words, patterns):
                match = pattern.search(lines[i]) or (i + 1 < len(lines) and pattern.search(lines[i + 1]))
                if match:
                    if '-->' in lines[i-1]:
                        timecodes = lines[i-1].strip().split(' --> ')
                        start_time = parse_srt_timecode(timecodes[0])
                        end_time = parse_srt_timecode(timecodes[1])
                        full_word = match.group(0)
                        edl_lines.append(f"{start_time:05.3f}\t{end_time:05.3f}\t1\t#Muted:'{full_word}'\n")
                        if pattern.search(lines[i]):
                            modified_line = re.sub(re.escape(full_word), '%' * len(full_word), modified_line)
                        if i + 1 < len(lines) and pattern.search(lines[i + 1]):
                            lines[i + 1] = re.sub(re.escape(full_word), '%' * len(full_word), lines[i + 1])
            modified_lines.append(modified_line)

        # Write the modified lines back to the .srt file
        with open(full_subtitle_path, 'w', encoding='utf-8') as srt_file:
            srt_file.writelines(modified_lines)

        # Create the .edl file
        edl_path = os.path.splitext(full_subtitle_path)[0] + '.edl'
        with open(edl_path, 'w', encoding='utf-8') as edl_file:
            edl_file.writelines(edl_lines)

        logging.info(f"Processed subtitles and created .edl file for {subtitle_file} - Success")
        print(f"Processed subtitles and created .edl file for {subtitle_file} - Success")

    except Exception as e:
        logging.error(f"Failed to process subtitles for {subtitle_file} - {str(e)}")
        print(f"Failed to process subtitles for {subtitle_file} - {str(e)}")
        if not os.path.exists('/config/scripts'):
            raise  # Re-raise the exception for the test environment

def run_test():
    print("Running test...")
    
    # Use the existing TestFile.srt
    test_file = "TestFile.srt"
    test_dir = os.path.dirname(os.path.abspath(test_file))

    try:
        # Call the process_subtitle function with the test file
        process_subtitle(test_dir, os.path.basename(test_file))

        # Print the processed subtitle content
        print("Processed subtitle content:")
        with open(test_file, "r", encoding="utf-8") as f:
            print(f.read())

        # Check if the .edl file exists and print its content
        edl_file = os.path.splitext(test_file)[0] + '.edl'
        if os.path.exists(edl_file):
            print(f"\nEDL file created/updated: {edl_file}")
            print("EDL file content:")
            with open(edl_file, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print("\nEDL file was not created.")

        # Print the log file content
        log_file = os.path.join(os.getcwd(), 'subtitle_processing.log')
        if os.path.exists(log_file):
            print("\nLog file content:")
            with open(log_file, "r") as f:
                print(f.read())
        else:
            print("\nLog file was not created.")

    except Exception as e:
        print(f"An error occurred: {e}")

    print("Test completed. All files have been kept for review.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process subtitles and create EDL files.")
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('directory', nargs='?', help='Directory containing the subtitle file')
    parser.add_argument('subtitle_file', nargs='?', help='Name of the subtitle file')
    
    args = parser.parse_args()

    if args.test:
        run_test()
    elif args.directory and args.subtitle_file:
        process_subtitle(args.directory, args.subtitle_file)
    else:
        print("Usage: python3 PMuteBazarr.py [--test] <directory> <subtitle_file>")
        sys.exit(1)
