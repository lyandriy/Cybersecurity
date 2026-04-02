import argparse
import os
from PIL import Image
from PIL.ExifTags import TAGS
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    for file in args.files:
        if not os.path.exists(file):
            print(f"Archivo no encontrado: {file}")
            continue
        if os.path.splitext(file)[1].lower() not in ALLOWED_EXTENSIONS:
            print(f"Extensión no permitida: {file}")
            continue
    for file in args.files:
        img = Image.open(file)
        print(f"Nombre del archivo: {file}")
        print(f"Formato: {img.format}")
        print(f"Tamaño: {img.width} x {img.height}")
        if img.info:
            for key, value in img.info.items():
                print(f"{key}: {value}")
        else:
            print("Sin datos info")
        exif_data = img._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                print(f"{TAGS.get(tag_id, tag_id)}: {value}")
        else:
            print("Sin datos EXIF")