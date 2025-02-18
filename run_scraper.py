import subprocess
import time
from datetime import datetime

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
    except subprocess.CalledProcessError as e:
        log_message(f"Error processing {input_file}: {str(e)}")
    except Exception as e:
        log_message(f"Unexpected error with {input_file}: {str(e)}")

def main():
    # Process each original file's chunks
    for file_num in ['1', '2', '3']:
        for chunk_num in range(1, 21):  # Assuming max 20 chunks per file
            input_file = f'eo{file_num}_chunk_{chunk_num}.json'
            output_file = f'results/results_eo{file_num}_chunk_{chunk_num}.csv'
            
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