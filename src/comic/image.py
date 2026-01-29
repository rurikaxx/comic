import os
from pathlib import Path

from PIL import Image


def get_quality() -> int:
    return int(os.environ.get("COMIC_IMAGE_QUALITY", "70"))


def compress_images(directory: Path) -> None:
    """Re-save all images in directory with configured quality."""
    quality = get_quality()

    for path in sorted(directory.iterdir()):
        if path.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        try:
            with Image.open(path) as img:
                img.save(path, quality=quality, optimize=True)
        except Exception as e:
            print(f"  警告：壓縮 {path.name} 失敗: {e}")
