import asyncio
import re
from pathlib import Path

try:
    import readline
except ImportError:
    readline = None

import click

from comic.api import fetch_gallery
from comic.downloader import download_images
from comic.image import compress_images



def _sanitize_title(title: str) -> str:
    """Remove spaces and filesystem-unsafe characters from title."""
    title = re.sub(r"\s+", "", title)
    title = re.sub(r'[<>:"/\\|?*]', "", title)
    return title


async def _run(gallery_id: str) -> None:
    print(f"正在取得漫畫資訊 #{gallery_id} ...")
    info = await fetch_gallery(gallery_id)

    dir_name = _sanitize_title(info.title)
    output_dir = Path.cwd() / dir_name
    print(f"標題：{info.title}")
    print(f"頁數：{len(info.pages)}")
    print(f"儲存至：{output_dir}")

    image_list = info.image_urls()
    print("開始下載圖片 ...")
    failed = await download_images(image_list, output_dir)

    if failed:
        print(f"警告：{len(failed)} 張圖片下載失敗: {', '.join(failed)}")

    print("壓縮圖片中 ...")
    compress_images(output_dir)

    total = len(image_list)
    success = total - len(failed)
    print(f"完成！成功下載 {success}/{total} 張圖片")

    if readline is not None:
        def _prefill_hook():
            readline.insert_text(dir_name)
            readline.redisplay()
        readline.set_pre_input_hook(_prefill_hook)
        try:
            new_name = input("輸入目錄名稱：").strip()
        finally:
            readline.set_pre_input_hook()
    else:
        new_name = click.prompt("輸入目錄名稱", default=dir_name).strip()

    if new_name != dir_name:
        new_dir = output_dir.parent / new_name
        output_dir.rename(new_dir)
        print(f"已重新命名為：{new_dir}")


@click.command()
@click.argument("gallery_id")
def main(gallery_id: str) -> None:
    """Download a comic from nhentai.net by gallery ID."""
    asyncio.run(_run(gallery_id))
