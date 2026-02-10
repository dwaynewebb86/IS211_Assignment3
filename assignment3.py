# import modules
import argparse
import re
import csv
import datetime
from urllib.request import urlopen

# download data function
def downloadData(url):
    with urlopen(url) as response:
        return response.read()

# process data function
def processData(data):
    lines = data.decode('utf-8').splitlines()
    reader = csv.reader(lines)
    
    total_hits = 0
    image_hits = 0
    browser_counts = {'Firefox': 0, 'Chrome': 0, 'IE': 0, 'Safari': 0}
    hour_counts = {} 
    
    for row in reader:
        if len(row) < 3:
            continue
        
        path = row[0]          
        datetime_str = row[1] 
        user_agent = row[2]    
        
        total_hits += 1
        
        # check image
        if re.search(r'\.(jpg|gif|png)$', path, re.IGNORECASE):
            image_hits += 1
        
        # count browsers
        if 'Firefox' in user_agent:
            browser_counts['Firefox'] += 1
        elif 'Chrome' in user_agent and 'Edge' not in user_agent:
            browser_counts['Chrome'] += 1
        elif 'MSIE' in user_agent or 'Trident' in user_agent:
            browser_counts['IE'] += 1
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            browser_counts['Safari'] += 1
        
        # EXTRA CREDIT: Extract hour and count
        try:
            dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            hour = dt.hour  
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        except ValueError:
            pass  
    
   # calculate and print results
    image_percentage = (image_hits / total_hits) * 100 if total_hits > 0 else 0
    print(f"Image requests account for {image_percentage:.1f}% of all requests")
    
    most_popular = max(browser_counts, key=browser_counts.get)
    print(f"The most popular browser is {most_popular}")
    
    # extra credit
    print("\nHits by hour:")
    sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
    for hour, count in sorted_hours:
        print(f"Hour {hour:02d} has {count} hits")
    

# main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    
    data = downloadData(args.url)
    processData(data)

if __name__ == "__main__":
    main()