import sys
import os
import argparse
import requests
import time
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin, urlparse
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

if __name__ == "__main__":
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
    print(args.url)
    print(args.r)
    print(args.l)
    print(args.p)
    headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"}
    response = requests.get(args.url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs = soup.find_all("img")
        for img in imgs:
            if "src" in img.attrs:
                img_url = img["src"]

                if (any(img_url.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)):
                    ruta = urljoin(args.url, img_url)
                    filename = os.path.join(args.p, os.path.basename(urlparse(ruta).path))
                    try:
                        img_response = requests.get(ruta, headers=headers, stream=True)
                        img_response.raise_for_status()
                        with open(filename, "wb") as f:
                            for chunk in img_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"Descargada: {filename}")
                    except Exception as e:
                        print(f"Error descargando {ruta}: {e}")
                    time.sleep(5)
    else:
        print("Failed to retrieve the web page")
    print(response.status_code)