from __future__ import annotations

import asyncio
from pathlib import Path

import aiohttp

MAX_CONCURRENT = 5
MAX_RETRIES = 3
RETRY_DELAY = 1.0


async def _download_one(
    session: aiohttp.ClientSession,
    url: str,
    dest: Path,
    semaphore: asyncio.Semaphore,
) -> str | None:
    """Download a single image. Returns filename on failure, None on success."""
    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        if attempt == MAX_RETRIES:
                            return dest.name
                        await asyncio.sleep(RETRY_DELAY * attempt)
                        continue
                    data = await resp.read()
                    dest.write_bytes(data)
                    return None
            except (aiohttp.ClientError, asyncio.TimeoutError):
                if attempt == MAX_RETRIES:
                    return dest.name
                await asyncio.sleep(RETRY_DELAY * attempt)
    return dest.name


async def download_images(
    image_list: list[tuple[str, str]],
    output_dir: Path,
) -> list[str]:
    """Download all images concurrently.

    Args:
        image_list: list of (url, filename) tuples
        output_dir: directory to save images

    Returns:
        list of failed filenames
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            _download_one(session, url, output_dir / filename, semaphore)
            for url, filename in image_list
        ]
        results = await asyncio.gather(*tasks)

    return [r for r in results if r is not None]
