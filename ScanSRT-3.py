#Correctly edits second line of CC text
#Also updates .srt file with % characters

import re
import shutil

def parse_srt_timecode(timecode):
    """Convert SRT timecode to seconds."""
    hours, minutes, seconds, milliseconds = map(float, re.split('[:,]', timecode))
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000

def load_bad_words(file_path):
    """Load bad words from a file and create regex patterns."""
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file.readlines()]
    # Create regex patterns for each word to match any word containing the letters
    patterns = [re.compile(f"\\b\\w*{''.join([f'[{char}]' for char in word])}\\w*\\b", re.IGNORECASE) for word in words]
    return words, patterns

def process_subtitle_file(input_file, output_file, words, patterns):
    # Make a backup of the original .srt file
    backup_file = input_file + '.mbak'
    shutil.copyfile(input_file, backup_file)

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    modified_lines = []
    with open(output_file, 'w', encoding='utf-8') as edl_file:
        for i in range(len(lines)):
            modified_line = lines[i]
            for word, pattern in zip(words, patterns):
                match = pattern.search(lines[i]) or (i + 1 < len(lines) and pattern.search(lines[i + 1]))
                if match:
                    # Ensure the previous line contains timecodes
                    if '-->' in lines[i-1]:
                        # Extract timecodes
                        timecodes = lines[i-1].strip().split(' --> ')
                        start_time = parse_srt_timecode(timecodes[0])
                        end_time = parse_srt_timecode(timecodes[1])
                        
                        # Extract the full word from the match
                        full_word = match.group(0)
                        
                        # Write to output file with the required format
                        edl_file.write(f"{start_time:09.3f}\t{end_time:09.3f}\t1\t#Muted:'{full_word}'\n")
                        
                        # Replace the word in the subtitle line with '%'
                        if pattern.search(lines[i]):
                            modified_line = re.sub(re.escape(full_word), '%' * len(full_word), modified_line)
                        if i + 1 < len(lines) and pattern.search(lines[i + 1]):
                            lines[i + 1] = re.sub(re.escape(full_word), '%' * len(full_word), lines[i + 1])
            
            # Collect the modified line
            modified_lines.append(modified_line)

    # Write the modified lines back to the .srt file
    with open(input_file, 'w', encoding='utf-8') as srt_file:
        srt_file.writelines(modified_lines)

# Define input and output files
input_file = 'S01E01.srt'
output_file = 'S01E01.edl'
bad_words_file = 'BadWords.txt'

# Load bad words and create regex patterns
words, patterns = load_bad_words(bad_words_file)

# Process the subtitle file
process_subtitle_file(input_file, output_file, words, patterns)
