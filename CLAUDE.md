# CLAUDE.md

## Project Overview

comic-dl: CLI tool to download comics from nhentai.net by gallery ID. Uses nhentai API to fetch metadata, downloads images concurrently with aiohttp, and compresses them with Pillow.

## Tech Stack

- Python 3.9+
- aiohttp (async HTTP)
- Pillow (image compression)
- click (CLI framework)
- setuptools (build system)

## Project Structure

```
src/comic/
├── cli.py          # CLI entry point, orchestrates the download flow
├── api.py          # nhentai API client, fetches gallery metadata
├── downloader.py   # Async concurrent image downloader
├── image.py        # Image compression with configurable quality
└── __main__.py     # python -m comic support
                    # Comics saved to current working directory as {sanitized_title}/
```

## Commands

```bash
# Install
pip install .

# Install (development, 修改程式碼後不需重新安裝)
pip install -e .

# Run
comic-dl <gallery_id>
python -m comic <gallery_id>
```

## Environment Variables

- `COMIC_IMAGE_QUALITY`: Image compression quality (1-100), default `70`

## Conventions

- Language: Chinese (Traditional) for user-facing messages and commit messages
- All user-facing CLI output is in Chinese
- Title priority for directory naming: japanese > chinese > english, spaces removed
- Images saved to `{cwd}/{sanitized_title}/`
- Async concurrent downloads with semaphore limit of 5
- Failed downloads retry up to 3 times
- 下載完成後提示使用者修改目錄名稱，使用 readline 預填原始名稱（可直接編輯），Windows 無 readline 時 fallback 為 click.prompt
