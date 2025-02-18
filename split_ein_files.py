import json
import math

CHUNK_SIZE = 500  # URLs per file

def split_ein_file(input_file, prefix):
    # Read original file
    with open(input_file, 'r') as f:
        data = json.load(f)
        ein_numbers = data['ein_numbers']
    
    # Calculate number of chunks needed
    total_eins = len(ein_numbers)
    num_chunks = math.ceil(total_eins / CHUNK_SIZE)
    
    # Split and save chunks
    for i in range(num_chunks):
        start_idx = i * CHUNK_SIZE
        end_idx = start_idx + CHUNK_SIZE
        chunk = ein_numbers[start_idx:end_idx]
        
        output_file = f"{prefix}_chunk_{i+1}.json"
        with open(output_file, 'w') as f:
            json.dump({'ein_numbers': chunk}, f)
        print(f"Created {output_file} with {len(chunk)} EINs")

# Split each input file
for file_num in ['1', '2', '3']:
    input_file = f'eo{file_num}.json'
    split_ein_file(input_file, f'eo{file_num}') 