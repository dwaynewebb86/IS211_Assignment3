import argparse
import os
import sys
from urllib.parse import urlparse
from urllib.request import urlopen


def _filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    return name or "downloaded_file"


def download_file(url: str, dest_path: str) -> None:
    try:
        with urlopen(url) as response, open(dest_path, "wb") as out_f:
            chunk_size = 1024 * 1024
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                out_f.write(chunk)
    except Exception as exc:
        raise RuntimeError(f"Failed to download {url}: {exc}") from exc


def main(url: str) -> None:
    filename = _filename_from_url(url)
    dest_path = os.path.join(os.getcwd(), filename)
    print(f"Downloading {url} -> {dest_path}")
    download_file(url, dest_path)
    print("Download complete.")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
