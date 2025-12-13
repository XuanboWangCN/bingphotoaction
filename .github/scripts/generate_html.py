import json
from datetime import datetime

PHOTOS_JSON = "photos.json"
HTML_FILE = "index.html"
PHOTOS_PER_PAGE = 25

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

    # 计算总页数
    total_pages = (len(photos) + PHOTOS_PER_PAGE - 1) // PHOTOS_PER_PAGE

    # 生成所有页面的HTML
    html_template = """<!DOCTYPE html>
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
    .pagination {
      margin-top: 2rem;
      justify-content: center;
    }
    .page-info {
      text-align: center;
      margin-top: 1rem;
      font-size: 0.875rem;
      color: #6c757d;
    }
    
    /* 卡片优化 */
    .card {
      display: flex;
      flex-direction: column;
    }
    .card-body {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    .card-text {
      flex: 1;
      margin-bottom: 1rem;
    }
    
    /* 按钮组优化 */
    .btn-action-group {
      display: flex;
      gap: 0.5rem;
      width: 100%;
    }
    .btn-bing-wrapper {
      flex: 2;
      display: flex;
    }
    .btn-download-wrapper {
      flex: 1;
      display: flex;
    }
    .btn-download-wrapper .btn,
    .btn-bing-wrapper .btn {
      width: 100%;
      font-size: 0.75rem;
      padding: 0.4rem 0.5rem;
    }
    .btn-group-vertical .btn-group,
    .btn-bing-wrapper .btn-group {
      width: 100%;
    }
    .btn-bing-wrapper .dropdown-toggle::after {
      margin-left: 0.25rem;
    }
  </style>
</head>
<body>
<div class="container py-4">
  <div class="page-header mb-4">
    <h1>必应每日一图</h1>
  </div>
  <div class="subtitle">全部图片 (共 {total_photos} 张)</div>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
{photos_content}
  </div>

  <!-- 分页导航 -->
  <nav>
    <ul class="pagination">
      <li class="page-item {prev_disabled}">
        <a class="page-link" href="?page={prev_page}" {prev_disabled_attr}>上一页</a>
      </li>
      {page_numbers}
      <li class="page-item {next_disabled}">
        <a class="page-link" href="?page={next_page}" {next_disabled_attr}>下一页</a>
      </li>
    </ul>
  </nav>

  <div class="page-info">
    第 {current_page} / {total_pages} 页 (每页显示 {photos_per_page} 张)
  </div>
</div>

<footer>
  <div class="container text-center">
    <p>Copyright © <a href="https://github.com/XuanboWangCN" target="_blank">XuanboWang</a> 2025. All rights reserved.<br>
    Powered by <a href="https://xuanbo.top" target="_blank">Xuanbo.top</a></p>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
  // 解析URL查询参数获取当前页码
  function getCurrentPage() {{
    const params = new URLSearchParams(window.location.search);
    let page = parseInt(params.get('page')) || 1;
    const maxPage = {total_pages};
    if (page < 1) page = 1;
    if (page > maxPage) page = maxPage;
    return page;
  }}

  // 页面加载时显示对应页面的内容
  function showPage(page) {{
    // 隐藏所有页面内容
    const allPages = document.querySelectorAll('.photo-page');
    allPages.forEach(p => p.style.display = 'none');
    
    // 显示当前页面内容
    const currentPageDiv = document.getElementById('page-' + page);
    if (currentPageDiv) {{
      currentPageDiv.style.display = 'block';
    }}
  }}

  // 初始化
  window.addEventListener('load', function() {{
    const page = getCurrentPage();
    showPage(page);
  }});
</script>
</body>
</html>
"""

    # 为每一页生成内容
    photos_html_by_page = {}
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * PHOTOS_PER_PAGE
        end_idx = start_idx + PHOTOS_PER_PAGE
        page_photos = photos[start_idx:end_idx]
        
        page_html = f'    <div class="photo-page" id="page-{page_num}">\n'
        page_html += '      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">\n'
        
        for photo in page_photos:
            date_formatted = format_date(photo.get("startDate", ""))
            title = photo.get("title", "")
            copyright_text = photo.get("copyright", "")
            copyright_link = photo.get("copyrightLink", "#")
            url_base = photo.get("urlBase", "")
            
            page_html += f"""        <div class="col">
          <div class="card h-100">
            <img src="{photo['url']}" class="card-img-top" alt="{title}">
            <div class="card-body">
              <h5 class="card-title">{title}</h5>
              <p class="card-text">{copyright_text}</p>
              <div class="btn-action-group">
                <div class="btn-bing-wrapper">
                  <a href="{copyright_link}" target="_blank" class="btn btn-sm btn-primary">在必应中搜索详情</a>
                </div>
                <div class="btn-download-wrapper">
                  <div class="btn-group w-100" role="group">
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
            </div>
            <div class="card-footer text-muted">
              {date_formatted}
            </div>
          </div>
        </div>
"""
        
        page_html += '      </div>\n'
        page_html += '    </div>\n'
        photos_html_by_page[page_num] = page_html

    # 组合所有页面内容
    all_photos_html = ''.join(photos_html_by_page.values())

    # 生成页码导航
    page_numbers_html = ''
    for page_num in range(1, total_pages + 1):
        if page_num == 1:
            page_numbers_html += f'      <li class="page-item active"><a class="page-link" href="?page={page_num}">{page_num}</a></li>\n'
        else:
            page_numbers_html += f'      <li class="page-item"><a class="page-link" href="?page={page_num}">{page_num}</a></li>\n'

    # 替换模板中的占位符
    final_html = html_template.format(
        total_photos=len(photos),
        photos_content=all_photos_html,
        prev_disabled='disabled' if 1 == 1 else '',
        prev_page=0,
        prev_disabled_attr='tabindex="-1" aria-disabled="true"' if 1 == 1 else '',
        page_numbers=page_numbers_html,
        next_disabled='disabled' if total_pages == 1 else '',
        next_page=2 if total_pages > 1 else total_pages,
        next_disabled_attr='tabindex="-1" aria-disabled="true"' if total_pages == 1 else '',
        current_page=1,
        total_pages=total_pages,
        photos_per_page=PHOTOS_PER_PAGE
    )
    
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    main()
