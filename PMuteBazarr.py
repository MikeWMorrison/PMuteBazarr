import sys
import os
import logging

def process_subtitle(directory, episode, episode_name, subtitles, subtitles_language, *args):
    # Determine the log file path based on how the script is run
    if __name__ == '__main__':
        # When run directly (production), use the original path
        log_file = '/config/scripts/subtitle_processing.log'
    else:
        # When imported (testing), use the current directory
        log_file = os.path.join(os.getcwd(), 'subtitle_processing.log')

    # Configure logging
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Log all passed arguments
        logging.info(f"Arguments: directory={directory}, episode={episode}, episode_name={episode_name}, subtitles={subtitles}, subtitles_language={subtitles_language}, args={args}")

        # Read the .srt file
        with open(subtitles, 'r', encoding='utf-8') as file:
            content = file.read()

        # Process the content (example: remove HI tags)
        processed_content = content.replace('[HI]', '').replace('[Forced]', '')

        # Save the processed content
        with open(subtitles, 'w', encoding='utf-8') as file:
            file.write(processed_content)

        # Copy to .edl2
        edl2_path = os.path.splitext(subtitles)[0] + '.edl2'
        with open(edl2_path, 'w', encoding='utf-8') as file:
            file.write(processed_content)

        logging.info(f"Processed subtitles for {episode_name} - Success")

    except Exception as e:
        logging.error(f"Failed to process subtitles for {episode_name} - {str(e)}")
        print(f"Failed to process subtitles for {episode_name} - {str(e)}")

if __name__ == "__main__":
    process_subtitle(*sys.argv[1:])
