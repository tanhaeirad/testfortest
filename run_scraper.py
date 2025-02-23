import subprocess
import time
from datetime import datetime
import os
import sys

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    with open("scraping_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def run_spider_for_chunk(input_file, output_file):
    log_message(f"Starting scraping for {input_file}")
    
    try:
        # Run the spider
        result = subprocess.run([
            "scrapy", "crawl", "charity",
            "-a", f"input_file={input_file}",
            "-o", output_file
        ], check=True)
        
        log_message(f"Completed scraping {input_file}")
        
        # Take a break between chunks        
        time.sleep(1)
        
    except subprocess.CalledProcessError as e:
        log_message(f"Error processing {input_file}: {str(e)}")
    except Exception as e:
        log_message(f"Unexpected error with {input_file}: {str(e)}")

def main():
    # Get command line argument, default to processing all chunks if no argument
    try:
        mode = int(sys.argv[1])
        if mode not in [0, 1]:
            log_message("Error: Argument must be 0 (even chunks) or 1 (odd chunks)")
            return
    except IndexError:
        log_message("No mode specified, processing all chunks")
        mode = None
    except ValueError:
        log_message("Error: Argument must be 0 (even chunks) or 1 (odd chunks)")
        return

    # Process each original file's chunks
    for file_num in ['1', '2', '3']:
        for chunk_num in range(1, 2000):  # Assuming max 2000 chunks per file
            # Skip if not matching even/odd mode
            if mode is not None and chunk_num % 2 != mode:
                continue
                
            input_file = f'input_files/eo{file_num}_chunk_{chunk_num}.json'
            output_file = f'results/results_eo{file_num}_chunk_{chunk_num}.csv'
            
            if os.path.exists(output_file):
                log_message(f"Skipping {input_file} because {output_file} exists")
                continue
            
            try:
                with open(input_file):
                    run_spider_for_chunk(input_file, output_file)
            except FileNotFoundError:
                # No more chunks for this file
                break

if __name__ == "__main__":
    log_message("Starting scraping process")
    main()
    log_message("Completed all scraping") 