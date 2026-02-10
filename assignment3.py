# import modules
import argparse
import os
import sys
import re
import csv
from urllib.parse import urlparse
from urllib.request import urlopen

# filename function
def _filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    return name or "downloaded_file"

# download data function
def downloadData(url):
    with urlopen(url) as response:
        return response.read()

# process data function
def processData(data):
     # parse csv
    lines = data.decode('utf-8').splitlines()
    reader = csv.reader(lines)
    
    total_hits = 0
    image_hits = 0
    browser_counts = {'Firefox': 0, 'Chrome': 0, 'IE': 0, 'Safari': 0}
    
    for row in reader:
        if len(row) < 3:
            continue
        
        path = row[0]          # e.g., /images/test.jpg
        datetime_str = row[1]  # e.g., 01/27/2014 03:26:04
        user_agent = row[2]    # e.g., Mozilla/5.0 ... Firefox/34.0
        
        total_hits += 1
        
        # Part III: Check if it's an image
        if re.search(r'\.(jpg|gif|png)$', path, re.IGNORECASE):
            image_hits += 1
        
        # Count browsers function
        if 'Firefox' in user_agent:
            browser_counts['Firefox'] += 1
        elif 'Chrome' in user_agent and 'Edge' not in user_agent:
            browser_counts['Chrome'] += 1
        elif 'MSIE' in user_agent or 'Trident' in user_agent:
            browser_counts['IE'] += 1
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            browser_counts['Safari'] += 1
    
    # calculate and print results
    image_percentage = (image_hits / total_hits) * 100 if total_hits > 0 else 0
    print(f"Total hits: {total_hits}")
    print(f"Image hits: {image_hits}")
    print(f"Percentage of image hits: {image_percentage:.2f}%")
    print("Browser counts:")
    for browser, count in browser_counts.items():
        print(f"  {browser}: {count}")
   

# main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    
    data = downloadData(args.url)
    processData(data)


# main entry point
if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
