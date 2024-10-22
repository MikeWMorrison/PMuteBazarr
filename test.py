import os
from PMuteBazarr import process_subtitle

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
