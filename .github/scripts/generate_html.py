import json
from datetime import datetime

PHOTOS_JSON = "photos.json"
HTML_FILE = "index.html"

def format_date(date_str):
    """将 20251205 格式转换为 2025/12/05"""
    if len(date_str) == 8:
        return f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:8]}"
    return date_str

def get_image_url(url_base, size):
    """根据尺寸生成图片URL"""
    if size == "uhd":
        return f"{url_base}_UHD.jpg"
    else:  # 1080p
        return f"{url_base}_1920x1080.jpg"

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
  <style>
    .page-header h1 {
      font-weight: 300;
    }
    .subtitle {
      font-size: 0.875rem;
      color: #6c757d;
      margin-bottom: 2rem;
    }
    .copyright-text {
      font-size: 0.875rem;
      color: #6c757d;
      font-style: italic;
    }
    footer {
      background-color: #f8f9fa;
      border-top: 1px solid #dee2e6;
      margin-top: 3rem;
      padding: 2rem 0;
      font-size: 0.875rem;
      color: #6c757d;
    }
    footer a {
      color: #0d6efd;
      text-decoration: none;
    }
    footer a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
<div class="container py-4">
  <div class="page-header mb-4">
    <h1>必应每日一图</h1>
  </div>
  <div class="subtitle">最近三十天</div>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
"""
    
    for photo in photos:
        date_formatted = format_date(photo.get("startDate", ""))
        title = photo.get("title", "")
        copyright_text = photo.get("copyright", "")
        copyright_link = photo.get("copyrightLink", "#")
        url_base = photo.get("urlBase", "")
        
        html += f"""
    <div class="col">
      <div class="card h-100">
        <img src="{photo['url']}" class="card-img-top" alt="{title}">
        <div class="card-body">
          <h5 class="card-title">{title}</h5>
          <p class="card-text">{copyright_text}</p>
          <div class="btn-group w-100" role="group">
            <a href="{copyright_link}" target="_blank" class="btn btn-sm btn-primary">在必应中搜索详情</a>
            <div class="btn-group" role="group">
              <button type="button" class="btn btn-sm btn-secondary dropdown-toggle" data-bs-toggle="dropdown">
                下载图片
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="{get_image_url(url_base, '1080p')}" download>1080p</a></li>
                <li><a class="dropdown-item" href="{get_image_url(url_base, 'uhd')}" download>UHD (4K)</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="card-footer text-muted">
          {date_formatted}
        </div>
      </div>
    </div>
"""
    
    html += """
  </div>
</div>

<footer>
  <div class="container text-center">
    <p>Copyright © <a href="https://github.com/XuanboWangCN" target="_blank">XuanboWang</a> 2025. All rights reserved.<br>
    Powered by <a href="https://xuanbo.top" target="_blank">Xuanbo.top</a></p>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
