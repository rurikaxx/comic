from __future__ import annotations

import aiohttp

API_URL = "https://nhentai.net/api/gallery/{gallery_id}"
IMAGE_BASE_URL = "https://i1.nhentai.net/galleries/{media_id}/{page}.{ext}"

TYPE_MAP = {
    "j": "jpg",
    "p": "png",
    "w": "webp",
}


class GalleryInfo:
    def __init__(self, gallery_id: str, title: str, media_id: str, pages: list[dict]):
        self.gallery_id = gallery_id
        self.title = title
        self.media_id = media_id
        self.pages = pages

    def image_urls(self) -> list[tuple[str, str]]:
        """Return list of (url, filename) tuples."""
        result = []
        for i, page in enumerate(self.pages, start=1):
            ext = TYPE_MAP.get(page["t"], "jpg")
            url = IMAGE_BASE_URL.format(media_id=self.media_id, page=i, ext=ext)
            filename = f"{i}.{ext}"
            result.append((url, filename))
        return result


def _pick_title(titles: dict) -> str:
    for key in ("japanese", "chinese", "english"):
        if titles.get(key):
            return titles[key]
    return "unknown"


async def fetch_gallery(gallery_id: str) -> GalleryInfo:
    url = API_URL.format(gallery_id=gallery_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                raise SystemExit(f"錯誤：漫畫編號 {gallery_id} 不存在")
            if resp.status == 403:
                raise SystemExit(f"錯誤：存取被拒絕 (403)，可能需要透過 CloudFlare 驗證")
            resp.raise_for_status()
            data = await resp.json()

    title = _pick_title(data["title"])
    media_id = data["media_id"]
    pages = data["images"]["pages"]

    return GalleryInfo(
        gallery_id=gallery_id,
        title=title,
        media_id=media_id,
        pages=pages,
    )
