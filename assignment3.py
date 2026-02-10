# import modules
import argparse
import os
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

# filename function
def _filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    return name or "downloaded_file"

# download function
def downloadData(url):
    with urlopen(url) as response:
        return response.read()

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
