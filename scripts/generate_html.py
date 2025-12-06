import json

PHOTOS_JSON = "photos.json"
HTML_FILE = "index.html"

def main():
    with open(PHOTOS_JSON, "r", encoding="utf-8") as f:
        photos = json.load(f)

    html = """<!DOCTYPE html>
<html lang="zh-cn">
<head>
  <meta charset="UTF-8">
  <title>必应每日一图</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container py-4">
  <h1 class="mb-4">必应每日一图（最近30天）</h1>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
"""
    for photo in photos:
        html += f"""
    <div class="col">
      <div class="card h-100">
        <img src="{photo['url']}" class="card-img-top" alt="{photo['title']}">
        <div class="card-body">
          <h5 class="card-title">{photo['title']}</h5>
          <p class="card-text">{photo['copyright']}</p>
          <a href="{photo['copyrightLink']}" target="_blank" class="btn btn-sm btn-primary">了解更多</a>
        </div>
        <div class="card-footer text-muted">
          日期：{photo['startDate']}
        </div>
      </div>
    </div>
"""
    html += """
  </div>
</div>
</body>
</html>
"""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
