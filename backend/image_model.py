from PIL import Image
import imagehash
import exifread

def analyze_image(image_path):
    img = Image.open(image_path)

    img_hash = str(imagehash.phash(img))

    metadata_info = {}
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)

        if "EXIF DateTimeOriginal" in tags:
            metadata_info["original_date"] = str(tags["EXIF DateTimeOriginal"])

    return {
        "image_hash": img_hash,
        "metadata": metadata_info
    }