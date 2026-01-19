import csv
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import time

# Color mapping based on serial number ranges
COLOR_RANGES = [
    (2, 197, 'black'),
    (198, 397, 'white'),
    (398, 597, 'blue'),
    (598, 797, 'pink'),
    (798, 997, 'green'),
    (998, 1197, 'brown'),
    (1198, 1397, 'beige'),
    (1399, 1597, 'red'),
    (1598, 1797, 'grey'),
    (1798, 1997, 'yellow')
]

def get_color_suffix(serial_num):
    """Get color suffix based on serial number"""
    for start, end, color in COLOR_RANGES:
        if start <= serial_num <= end:
            return color
    return ''

def get_file_extension(url):
    """Extract file extension from URL"""
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1]
    return ext if ext else '.jpg'

def sanitize_filename(name):
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip()

def download_image(serial_num, url, name, output_dir):
    """Download a single image"""
    try:
        # Get color suffix
        color = get_color_suffix(serial_num)
        
        # Sanitize the name
        clean_name = sanitize_filename(name)
        
        # Get file extension
        ext = get_file_extension(url)
        
        # Create filename: serial_name_color.ext
        if color:
            filename = f"{serial_num}_{clean_name}_{color}{ext}"
        else:
            filename = f"{serial_num}_{clean_name}{ext}"
        
        filepath = os.path.join(output_dir, filename)
        
        # Download image
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Save image
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return (serial_num, True, filename)
    
    except Exception as e:
        return (serial_num, False, str(e))

def main():
    # Configuration
    csv_file = 'tops(Sheet1).csv'
    output_dir = 'downloaded_images'
    max_workers = 10  # Number of concurrent downloads
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read CSV file
    print(f"Reading CSV file: {csv_file}")
    tasks = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        serial_num = 1
        for row in reader:
            if len(row) >= 2:
                url = row[0].strip()
                name = row[1].strip()
                
                if url and name:
                    tasks.append((serial_num, url, name))
                    serial_num += 1
    
    print(f"Found {len(tasks)} images to download")
    print(f"Downloading with {max_workers} concurrent workers...")
    
    # Download images concurrently
    successful = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(download_image, serial, url, name, output_dir): serial
            for serial, url, name in tasks
        }
        
        # Process completed downloads
        for future in as_completed(futures):
            serial_num, success, result = future.result()
            
            if success:
                successful += 1
                print(f"✓ [{successful + failed}/{len(tasks)}] Downloaded: {result}")
            else:
                failed += 1
                print(f"✗ [{successful + failed}/{len(tasks)}] Failed #{serial_num}: {result}")
    
    # Summary
    print("\n" + "="*60)
    print(f"Download Complete!")
    print(f"Total: {len(tasks)} | Successful: {successful} | Failed: {failed}")
    print(f"Images saved to: {os.path.abspath(output_dir)}")
    print("="*60)

if __name__ == "__main__":
    main()



