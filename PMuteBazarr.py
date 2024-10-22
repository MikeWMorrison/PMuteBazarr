import sys
import os
import logging

def process_subtitle(directory, subtitle_file):
    # Determine the log file path based on the environment
    if os.path.exists('/config/scripts'):
        # Production environment
        log_file = '/config/scripts/subtitle_processing.log'
    else:
        # Test environment
        log_file = os.path.join(os.getcwd(), 'subtitle_processing.log')

    # Configure logging
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Log all passed arguments
    logging.info(f"Arguments: \n\tdirectory={directory}, \n\tsubtitle_file={subtitle_file}")

    try:
        # Check if the subtitle file exists
        full_subtitle_path = os.path.join(directory, subtitle_file)
        if not os.path.exists(full_subtitle_path):
            raise FileNotFoundError(f"Subtitle file not found: {full_subtitle_path}")

        # Read the .srt file
        with open(full_subtitle_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Process the content (example: remove HI tags)
        processed_content = content.replace('[HI]', '').replace('[Forced]', '')

        # Save the processed content
        with open(full_subtitle_path, 'w', encoding='utf-8') as file:
            file.write(processed_content)

        # Copy to .edl2
        edl2_path = os.path.splitext(full_subtitle_path)[0] + '.edl2'
        with open(edl2_path, 'w', encoding='utf-8') as file:
            file.write(processed_content)

        logging.info(f"Processed subtitles for {subtitle_file} - Success")
        print(f"Processed subtitles for {subtitle_file} - Success")

    except Exception as e:
        logging.error(f"Failed to process subtitles for {subtitle_file} - {str(e)}")
        print(f"Failed to process subtitles for {subtitle_file} - {str(e)}")
        if not os.path.exists('/config/scripts'):
            raise  # Re-raise the exception for the test environment

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 PMuteBazarr.py <directory> <subtitle_file>")
        sys.exit(1)
    
    process_subtitle(sys.argv[1], sys.argv[2])
