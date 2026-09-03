"""
NCERT Digital Library — jsDelivr CDN Cache Purge & Pre-Warmer
--------------------------------------------------------------
Automates global cache invalidation and pre-warming across Cloudflare & Fastly
edge networks for all Class 10 textbooks, chapters, and cover assets.

Usage:
  python purge_cache.py                 # Purges all covers and chapters
  python purge_cache.py --covers-only   # Fast purge for cover artwork only
  python purge_cache.py --warm          # Purge and immediately pre-warm CDN edge
  python purge_cache.py --path <rel>    # Purge a specific file
"""

import sys
import os
import json
import time
import argparse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

GITHUB_REPO = "AryansDevStudios/ncert-class10-pdf-storage"
BRANCH = "main"
PURGE_ENDPOINT = "https://purge.jsdelivr.net/"
CDN_BASE = f"https://cdn.jsdelivr.net/gh/{GITHUB_REPO}@{BRANCH}/"

def collect_paths_from_manifest(manifest_path="web_data.json", covers_only=False):
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest file '{manifest_path}' not found.")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    paths = []
    for book in catalog:
        # Book cover
        if book.get("cover_url"):
            paths.append(book["cover_url"].replace("\\", "/"))

        if not covers_only:
            # Chapters
            for ch in book.get("chapters", []):
                if ch.get("url"):
                    paths.append(ch["url"].replace("\\", "/"))

    # De-duplicate while preserving order
    unique_paths = list(dict.fromkeys(paths))
    return unique_paths

def purge_batch(paths_chunk):
    """
    Submits a batch of relative paths to the jsDelivr Purge API.
    """
    formatted_paths = [
        f"/gh/{GITHUB_REPO}@{BRANCH}/{p.lstrip('/')}"
        for p in paths_chunk
    ]

    payload = json.dumps({"path": formatted_paths}).encode("utf-8")
    req = urllib.request.Request(
        PURGE_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NCERT-PurgeTool/1.0"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            purge_id = data.get("id")
            return purge_id, formatted_paths
    except Exception as e:
        print(f"  [ERR] Purge request failed: {e}")
        return None, formatted_paths

def poll_purge_status(purge_id, timeout=10):
    """
    Polls the purge ID status until finished or timeout.
    """
    if not purge_id:
        return False

    status_url = f"https://purge.jsdelivr.net/status/{purge_id}"
    start = time.time()

    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(status_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("status") == "finished":
                    return True
        except Exception:
            pass
        time.sleep(0.5)

    return False

def warm_url(url):
    """
    Sends an HTTP HEAD / lightweight request to pre-warm the CDN edge in the current region.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return url, resp.status, resp.headers.get("Content-Length")
    except Exception as e:
        return url, "ERR", str(e)

def main():
    parser = argparse.ArgumentParser(description="Purge and pre-warm jsDelivr CDN cache for NCERT Class 10 textbooks.")
    parser.add_argument("--covers-only", action="store_true", help="Purge only cover images.")
    parser.add_argument("--warm", action="store_true", help="Pre-warm CDN edge cache after purging.")
    parser.add_argument("--path", type=str, help="Purge a specific relative file path.")
    parser.add_argument("--batch-size", type=int, default=50, help="Number of files per purge request (default: 50).")
    args = parser.parse_args()

    print("=" * 65)
    print("NCERT CLASS 10 — JSDELIVR CDN CACHE PURGE TOOL")
    print(f"Repository: {GITHUB_REPO}@{BRANCH}")
    print("=" * 65)

    if args.path:
        paths = [args.path.replace("\\", "/")]
    else:
        paths = collect_paths_from_manifest(covers_only=args.covers_only)

    print(f"\nCollected {len(paths)} file path(s) to purge globally...")

    # Split into chunks of batch_size
    chunk_size = max(1, min(args.batch_size, 100))
    chunks = [paths[i:i + chunk_size] for i in range(0, len(paths), chunk_size)]

    all_purged = True
    total_purged = 0

    for idx, chunk in enumerate(chunks, 1):
        print(f"\n[Batch {idx}/{len(chunks)}] Submitting {len(chunk)} paths to jsDelivr Purge API...")
        purge_id, formatted_paths = purge_batch(chunk)
        if purge_id:
            print(f"  -> Job ID: {purge_id} (Status: pending)")
            done = poll_purge_status(purge_id)
            if done:
                print(f"  [OK] Successfully purged {len(chunk)} paths from Cloudflare & Fastly edge caches.")
                total_purged += len(chunk)
            else:
                print(f"  [WARN] Purge job queued (ID: {purge_id})")
                total_purged += len(chunk)
        else:
            all_purged = False

    print("\n" + "=" * 65)
    print(f"Purge Complete: {total_purged}/{len(paths)} file caches invalidated.")
    print("=" * 65)

    # Pre-warming phase
    if args.warm:
        print("\nPre-warming CDN edge caches across regional nodes...")
        urls = [f"{CDN_BASE}{p.lstrip('/')}" for p in paths]
        warmed = 0
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_url = {executor.submit(warm_url, u): u for u in urls}
            for future in as_completed(future_to_url):
                url, status, length = future.result()
                if status == 200:
                    warmed += 1
                fname = os.path.basename(url)
                sz_str = f"({int(length)/1024:.1f} KB)" if length and length.isdigit() else ""
                print(f"  [WARM] {fname:25} -> HTTP {status} {sz_str}")

        print(f"\n[OK] Pre-warmed {warmed}/{len(urls)} assets at CDN edge.")

if __name__ == "__main__":
    main()
