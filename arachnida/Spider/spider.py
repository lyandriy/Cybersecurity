import sys
import os
import argparse
import requests
import time
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin, urlparse
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"}
visited = set()

def pars():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-r", action="store_true")
    parser.add_argument("-l", type=int, default=5)
    parser.add_argument("-p", default="./data/")

    args = parser.parse_args()

    if args.l != 5 and not args.r:
        parser.error("-l solo se puede usar con -r")
    if os.path.exists(args.p) and not os.path.isdir(args.p):
        parser.error(f"argument -p: invalid path: '{args.p}'")
    else:
        os.makedirs(args.p, exist_ok=True)
    return args

def recursion_links(url, depth, args, base_domain):
    if depth == 0 or url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(f"Error accediendo {url}: {e}")
        return

    if response.status_code != 200 or "text/html" not in response.headers.get("Content-Type", ""):
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    img_from_soup(soup, url, args)

    for a_tag in soup.find_all("a"):
        href = a_tag.get("href")
        if href:
            print(depth)
            full_url = urljoin(url, href)
            if urlparse(full_url).scheme in ("http", "https") and \
               urlparse(full_url).netloc == base_domain:
                recursion_links(full_url, depth - 1, args, base_domain)

def download_img(url, args):
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(f"Error: {e}")
        return

    if response.status_code == 200 and "text/html" in response.headers.get("Content-Type", ""):
        soup = BeautifulSoup(response.text, 'html.parser')
        img_from_soup(soup, url, args)

def img_from_soup(soup, base_url, args):
    for img in soup.find_all("img"):
        img_url = img.get("src", "")
        if (any(img_url.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)):
            full_url = urljoin(base_url, img_url)
            filename = os.path.join(args.p, os.path.basename(urlparse(full_url).path))
            try:
                img_response = requests.get(full_url, headers=headers, stream=True)
                img_response.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Descargada: {filename}")
            except Exception as e:
                print(f"Error descargando {full_url}: {e}")

if __name__ == "__main__":
    args = pars()

    if args.r:
        recursion_links(args.url, args.l, args, urlparse(args.url).netloc)
    else:
        download_img(args.url, args)
