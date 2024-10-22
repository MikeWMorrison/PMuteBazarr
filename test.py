import os
from PMuteBazarr import process_subtitle

# Create a sample subtitle file
sample_subtitle_content = """1
00:00:01,000 --> 00:00:04,000
[HI] Hello, world!

2
00:00:05,000 --> 00:00:08,000
[Forced] This is a test subtitle.

3
00:00:09,000 --> 00:00:12,000
Normal subtitle line.
"""

# Create a temporary directory for testing
test_dir = "test_subtitles"
os.makedirs(test_dir, exist_ok=True)

# Create a sample subtitle file
sample_subtitle_file = "sample_episode.srt"
full_subtitle_path = os.path.join(test_dir, sample_subtitle_file)
with open(full_subtitle_path, "w", encoding="utf-8") as f:
    f.write(sample_subtitle_content)

try:
    # Call the process_subtitle function with sample data
    process_subtitle(test_dir, sample_subtitle_file)

    # Print the processed subtitle content
    print("Processed subtitle content:")
    with open(full_subtitle_path, "r", encoding="utf-8") as f:
        print(f.read())

    # Print the .edl2 file content
    edl2_file = os.path.join(test_dir, "sample_episode.edl2")
    print("\nEDL2 file content:")
    with open(edl2_file, "r", encoding="utf-8") as f:
        print(f.read())

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up
    if os.path.exists(full_subtitle_path):
        os.remove(full_subtitle_path)
    if os.path.exists(edl2_file):
        os.remove(edl2_file)
    if os.path.exists(test_dir):
        os.rmdir(test_dir)

print("Test completed. Check subtitle_processing.log for detailed logs.")
