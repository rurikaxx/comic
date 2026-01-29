# Comic Downloader Design

## Overview

CLI tool to download comics from nhentai.net by gallery ID.

## Usage

```bash
comic-dl 546951
```

## Architecture

```
comic/
├── pyproject.toml
├── src/
│   └── comic/
│       ├── __init__.py
│       ├── cli.py          # CLI entry point (click)
│       ├── api.py          # nhentai API client
│       ├── downloader.py   # async concurrent image download
│       └── image.py        # image compression (Pillow)
└── storage/
```

## Flow

1. CLI receives gallery ID
2. Call `GET https://nhentai.net/api/gallery/{id}`
3. Parse JSON response:
   - Title: prefer japanese > chinese > english
   - `media_id` for image URL construction
   - `pages` array for each page's image format
4. Create directory: `storage/{title_no_spaces}/`
5. Build image URLs: `https://i1.nhentai.net/galleries/{media_id}/{n}.{ext}`
6. Download all images concurrently with `aiohttp`
7. Compress each image with Pillow using configurable quality

## Image Format Mapping

- `j` -> `.jpg`
- `p` -> `.png`
- `w` -> `.webp`

## Environment Variables

- `COMIC_IMAGE_QUALITY`: image compression quality, default `70` (integer 1-100)

## Error Handling

- API 404: print error, exit
- Single image download failure: warn, continue, report failed pages at end
- Network error: retry up to 3 times per image

## Dependencies

- `aiohttp` - async HTTP
- `Pillow` - image compression
- `click` - CLI framework
