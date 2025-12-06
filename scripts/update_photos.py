import json
import os
from datetime import datetime

PHOTO_JSON = "photo.json"
PHOTOS_JSON = "photos.json"
MAX_DAYS = 30

def load_photos():
    if os.path.exists(PHOTOS_JSON):
        with open(PHOTOS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_photos(photos):
    with open(PHOTOS_JSON, "w", encoding="utf-8") as f:
        json.dump(photos, f, ensure_ascii=False, indent=2)

def main():
    with open(PHOTO_JSON, "r", encoding="utf-8") as f:
        photo = json.load(f)
    photos = load_photos()
    # 按startDate去重
    photos = [p for p in photos if p.get("startDate") != photo.get("startDate")]
    photos.insert(0, photo)
    photos = photos[:MAX_DAYS]
    save_photos(photos)

if __name__ == "__main__":
    main()
