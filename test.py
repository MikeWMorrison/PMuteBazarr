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
sample_subtitle_file = os.path.join(test_dir, "sample_episode.srt")
with open(sample_subtitle_file, "w", encoding="utf-8") as f:
    f.write(sample_subtitle_content)

# Call the process_subtitle function with sample data
process_subtitle(
    directory=test_dir,
    episode="sample_episode",
    episode_name="Sample Episode",
    subtitles=sample_subtitle_file,
    subtitles_language="eng"
)

# Print the processed subtitle content
print("Processed subtitle content:")
with open(sample_subtitle_file, "r", encoding="utf-8") as f:
    print(f.read())

# Print the .edl2 file content
edl2_file = os.path.join(test_dir, "sample_episode.edl2")
print("\nEDL2 file content:")
with open(edl2_file, "r", encoding="utf-8") as f:
    print(f.read())

# Clean up
os.remove(sample_subtitle_file)
os.remove(edl2_file)
os.rmdir(test_dir)
