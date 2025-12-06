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
    # 检查photo.json是否存在且有内容
    if not os.path.exists(PHOTO_JSON):
        print(f"Error: {PHOTO_JSON} not found")
        return
    
    with open(PHOTO_JSON, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            print(f"Error: {PHOTO_JSON} is empty")
            return
        try:
            photo = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse {PHOTO_JSON}: {e}")
            return
    
    photos = load_photos()
    # 按startDate去重
    photos = [p for p in photos if p.get("startDate") != photo.get("startDate")]
    photos.insert(0, photo)
    photos = photos[:MAX_DAYS]
    save_photos(photos)
    print(f"Updated photos.json with {len(photos)} photos")

if __name__ == "__main__":
    main()
