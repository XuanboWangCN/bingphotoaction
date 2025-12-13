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
        return url_base + "_UHD.jpg"
    else:  # 1080p
        return url_base + "_1920x1080.jpg"

def main():
    with open(PHOTOS_JSON, "r", encoding="utf-8") as f:
        photos = json.load(f)

    # 计算总页数
    total_pages = (len(photos) + PHOTOS_PER_PAGE - 1) // PHOTOS_PER_PAGE

    # 为每一页生成内容
    photos_html_by_page = {}
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * PHOTOS_PER_PAGE
        end_idx = start_idx + PHOTOS_PER_PAGE
        page_photos = photos[start_idx:end_idx]
        
        page_html = '    <div class="photo-page" id="page-' + str(page_num) + '">\n'
        
        for photo in page_photos:
            date_formatted = format_date(photo.get("startDate", ""))
            title = photo.get("title", "")
            copyright_text = photo.get("copyright", "")
            copyright_link = photo.get("copyrightLink", "#")
            url_base = photo.get("urlBase", "")
            photo_url = photo.get("url", "")
            
            page_html += '      <div class="col">\n'
            page_html += '        <div class="card h-100">\n'
            page_html += '          <img src="' + photo_url + '" class="card-img-top" alt="' + title + '">\n'
            page_html += '          <div class="card-body d-flex flex-column">\n'
            page_html += '            <div class="flex-grow-1">\n'
            page_html += '              <h5 class="card-title">' + title + '</h5>\n'
            page_html += '              <p class="card-text">' + copyright_text + '</p>\n'
            page_html += '            </div>\n'
            page_html += '            <div class="btn-group w-100 mt-2" role="group">\n'
            page_html += '              <div class="btn-group flex-grow-1" role="group">\n'
            page_html += '                <button type="button" class="btn btn-sm btn-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">\n'
            page_html += '                  下载图片\n'
            page_html += '                </button>\n'
            page_html += '                <ul class="dropdown-menu">\n'
            page_html += '                  <li><a class="dropdown-item" href="' + get_image_url(url_base, '1080p') + '" download>1080p</a></li>\n'
            page_html += '                  <li><a class="dropdown-item" href="' + get_image_url(url_base, 'uhd') + '" download>UHD (4K)</a></li>\n'
            page_html += '                </ul>\n'
            page_html += '              </div>\n'
            page_html += '              <a href="' + copyright_link + '" target="_blank" class="btn btn-sm btn-primary">在必应中查看</a>\n'
            page_html += '            </div>\n'
            page_html += '          </div>\n'
            page_html += '          <div class="card-footer text-muted">\n'
            page_html += '            ' + date_formatted + '\n'
            page_html += '          </div>\n'
            page_html += '        </div>\n'
            page_html += '      </div>\n'
        
        page_html += '    </div>\n'
        photos_html_by_page[page_num] = page_html

    # 组合所有页面内容
    all_photos_html = ''.join(photos_html_by_page.values())

    # 生成页码导航
    page_numbers_html = ''
    for page_num in range(1, total_pages + 1):
        if page_num == 1:
            page_numbers_html += '      <li class="page-item active"><a class="page-link" href="?page=' + str(page_num) + '">' + str(page_num) + '</a></li>\n'
        else:
            page_numbers_html += '      <li class="page-item"><a class="page-link" href="?page=' + str(page_num) + '">' + str(page_num) + '</a></li>\n'

    # 构建HTML
    html = '<!DOCTYPE html>\n'
    html += '<html lang="zh-cn">\n'
    html += '<head>\n'
    html += '  <meta charset="UTF-8">\n'
    html += '  <title>必应每日一图相册 by XuanboWang</title>\n'
    html += '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
    html += '  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">\n'
    html += '  <link rel="icon" href="https://bingphotoaction.pages.dev/favicon.png" type="image/x-icon">\n'
    html += '  <meta name="description" content="必应每日一图图册 - 每日精选高质量壁纸库，永久保存必应搜索精选图片，支持1080p和4K分辨率免费下载，随时查看历史图片记录，响应式分页浏览，海量高清图片收藏库。">\n'
    html += '  <meta name="keywords" content="必应图册,每日壁纸,图片库,高清壁纸,4K下载,免费素材,图片收藏,历史图片,历史壁纸,图片记录">\n'
    html += '  <meta name="author" content="XuanboWang">\n'
    html += '  <meta property="og:title" content="必应每日一图图册">\n'
    html += '  <meta property="og:description" content="海量高质量必应精选图片，永久免费图册库，完整历史图片记录，1080p和4K分辨率免费下载">\n'
    html += '  <meta property="og:type" content="website">\n'
    html += '  <meta name="twitter:card" content="summary">\n'
    html += '  <meta name="twitter:title" content="必应每日一图图册">\n'
    html += '  <meta name="twitter:description" content="精选高清图片图册库，查看完整历史记录，每日更新，免费下载高清壁纸">\n'
    html += '  <style>\n'
    html += '    .page-header h1 {\n'
    html += '      font-weight: 300;\n'
    html += '    }\n'
    html += '    .subtitle {\n'
    html += '      font-size: 0.875rem;\n'
    html += '      color: #6c757d;\n'
    html += '      margin-bottom: 2rem;\n'
    html += '    }\n'
    html += '    .copyright-text {\n'
    html += '      font-size: 0.875rem;\n'
    html += '      color: #6c757d;\n'
    html += '      font-style: italic;\n'
    html += '    }\n'
    html += '    footer {\n'
    html += '      background-color: #f8f9fa;\n'
    html += '      border-top: 1px solid #dee2e6;\n'
    html += '      margin-top: 3rem;\n'
    html += '      padding: 2rem 0;\n'
    html += '      font-size: 0.875rem;\n'
    html += '      color: #6c757d;\n'
    html += '    }\n'
    html += '    footer a {\n'
    html += '      color: #0d6efd;\n'
    html += '      text-decoration: none;\n'
    html += '    }\n'
    html += '    footer a:hover {\n'
    html += '      text-decoration: underline;\n'
    html += '    }\n'
    html += '    .page-info {\n'
    html += '      text-align: center;\n'
    html += '      font-size: 0.875rem;\n'
    html += '      color: #6c757d;\n'
    html += '      margin: 2rem 0;\n'
    html += '    }\n'
    html += '    .card {\n'
    html += '      border-radius: 8px;\n'
    html += '      overflow: hidden;\n'
    html += '      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);\n'
    html += '    }\n'
    html += '    .card-img-top {\n'
    html += '      object-fit: cover;\n'
    html += '      height: 200px;\n'
    html += '    }\n'
    html += '    .card-title {\n'
    html += '      font-size: 1rem;\n'
    html += '      margin-bottom: 0.5rem;\n'
    html += '      font-weight: 600;\n'
    html += '      color: #212529;\n'
    html += '    }\n'
    html += '    .card-text {\n'
    html += '      font-size: 0.875rem;\n'
    html += '      color: #6c757d;\n'
    html += '      margin-bottom: 1rem;\n'
    html += '      line-height: 1.4;\n'
    html += '    }\n'
    html += '    .card-footer {\n'
    html += '      background-color: #f8f9fa;\n'
    html += '      border-top: 1px solid #dee2e6;\n'
    html += '      padding: 0.75rem 1rem;\n'
    html += '      font-size: 0.875rem;\n'
    html += '    }\n'
    html += '    .photo-page {\n'
    html += '      display: flex;\n'
    html += '      flex-wrap: wrap;\n'
    html += '      width: 100%;\n'
    html += '      gap: 1rem;\n'
    html += '    }\n'
    html += '    .photo-page .col {\n'
    html += '      flex: 0 0 calc(25% - 0.75rem);\n'
    html += '    }\n'
    html += '    @media (max-width: 1199.98px) {\n'
    html += '      .photo-page .col {\n'
    html += '        flex: 0 0 calc(33.333333% - 0.67rem);\n'
    html += '      }\n'
    html += '    }\n'
    html += '    @media (max-width: 991.98px) {\n'
    html += '      .photo-page .col {\n'
    html += '        flex: 0 0 calc(50% - 0.5rem);\n'
    html += '      }\n'
    html += '    }\n'
    html += '    @media (max-width: 767.98px) {\n'
    html += '      .photo-page .col {\n'
    html += '        flex: 0 0 100%;\n'
    html += '      }\n'
    html += '    }\n'
    html += '  </style>\n'
    html += '</head>\n'
    html += '<body>\n'
    html += '  <div class="container py-4">\n'
    html += '    <div class="page-header mb-4">\n'
    html += '      <h1>必应每日一图相册</h1>\n'
    html += '    </div>\n'
    html += '    <div class="subtitle">已保存来自必应的 ' + str(len(photos)) + ' 张图片</div>\n'
    html += '    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">\n'
    html += all_photos_html
    html += '    </div>\n'
    html += '\n'
    html += '    <!-- 分页导航 -->\n'
    html += '    <nav class="mt-5" aria-label="Page navigation">\n'
    html += '      <ul class="pagination justify-content-center">\n'
    html += '        <li class="page-item ' + ('disabled' if total_pages <= 1 else '') + '">\n'
    html += '          <a class="page-link" href="#" id="prev-page" ' + ('tabindex="-1" aria-disabled="true"' if total_pages <= 1 else '') + '>上一页</a>\n'
    html += '        </li>\n'
    html += page_numbers_html
    html += '        <li class="page-item ' + ('disabled' if total_pages <= 1 else '') + '">\n'
    html += '          <a class="page-link" href="#" id="next-page" ' + ('tabindex="-1" aria-disabled="true"' if total_pages <= 1 else '') + '>下一页</a>\n'
    html += '        </li>\n'
    html += '      </ul>\n'
    html += '    </nav>\n'
    html += '\n'
    html += '    <div class="text-center mt-3 text-muted">\n'
    html += '      第 <span id="current-page">1</span> / ' + str(total_pages) + ' 页 <br>每页最多显示 ' + str(PHOTOS_PER_PAGE) + ' 张\n'
    html += '    </div>\n'
    html += '  </div>\n'
    html += '\n'
    html += '<footer>\n'
    html += '  <div class="container text-center">\n'
    html += '    <p>Copyright © <a href="https://github.com/XuanboWangCN" target="_blank">XuanboWang</a> 2025. All rights reserved.<br>\n'
    html += '    Powered by <a href="https://xuanbo.top" target="_blank">Xuanbo.top</a><br>在 Github 中查看源代码：<a href="https://github.com/XuanboWangCN/bingphotoaction/" target="_blank">XuanboWang</a></p>\n'
    html += '  </div>\n'
    html += '</footer>\n'
    html += '\n'
    html += '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>\n'
    html += '<script>\n'
    html += '  // 解析URL查询参数获取当前页码\n'
    html += '  function getCurrentPage() {\n'
    html += '    const params = new URLSearchParams(window.location.search);\n'
    html += '    let page = parseInt(params.get("page")) || 1;\n'
    html += '    const maxPage = ' + str(total_pages) + ';\n'
    html += '    if (page < 1) page = 1;\n'
    html += '    if (page > maxPage) page = maxPage;\n'
    html += '    return page;\n'
    html += '  }\n'
    html += '\n'
    html += '  // 页面加载时显示对应页面的内容\n'
    html += '  function showPage(page) {\n'
    html += '    // 隐藏所有页面内容\n'
    html += '    const allPages = document.querySelectorAll(".photo-page");\n'
    html += '    allPages.forEach(p => p.style.display = "none");\n'
    html += '    \n'
    html += '    // 显示当前页面内容\n'
    html += '    const currentPageDiv = document.getElementById("page-" + page);\n'
    html += '    if (currentPageDiv) {\n'
    html += '      currentPageDiv.style.display = "flex";\n'
    html += '    }\n'
    html += '    \n'
    html += '    // 更新页码显示\n'
    html += '    document.getElementById("current-page").textContent = page;\n'
    html += '    \n'
    html += '    // 更新上一页/下一页按钮\n'
    html += '    const maxPage = ' + str(total_pages) + ';\n'
    html += '    const prevBtn = document.getElementById("prev-page");\n'
    html += '    const nextBtn = document.getElementById("next-page");\n'
    html += '    \n'
    html += '    if (page <= 1) {\n'
    html += '      prevBtn.href = "#";\n'
    html += '      prevBtn.parentElement.classList.add("disabled");\n'
    html += '    } else {\n'
    html += '      prevBtn.href = "?page=" + (page - 1);\n'
    html += '      prevBtn.parentElement.classList.remove("disabled");\n'
    html += '    }\n'
    html += '    \n'
    html += '    if (page >= maxPage) {\n'
    html += '      nextBtn.href = "#";\n'
    html += '      nextBtn.parentElement.classList.add("disabled");\n'
    html += '    } else {\n'
    html += '      nextBtn.href = "?page=" + (page + 1);\n'
    html += '      nextBtn.parentElement.classList.remove("disabled");\n'
    html += '    }\n'
    html += '    \n'
    html += '    // 更新分页按钮样式\n'
    html += '    const pageItems = document.querySelectorAll(".pagination .page-item");\n'
    html += '    pageItems.forEach(item => {\n'
    html += '      const link = item.querySelector("a");\n'
    html += '      if (link) {\n'
    html += '        const pageText = link.textContent.trim();\n'
    html += '        // 只处理数字页码按钮\n'
    html += '        if (/^\\d+$/.test(pageText)) {\n'
    html += '          if (parseInt(pageText) === page) {\n'
    html += '            item.classList.add("active");\n'
    html += '          } else {\n'
    html += '            item.classList.remove("active");\n'
    html += '          }\n'
    html += '        }\n'
    html += '      }\n'
    html += '    });\n'
    html += '  }\n'
    html += '\n'
    html += '  // 初始化\n'
    html += '  window.addEventListener("load", function() {\n'
    html += '    const page = getCurrentPage();\n'
    html += '    showPage(page);\n'
    html += '  });\n'
    html += '</script>\n'
    html += '</body>\n'
    html += '</html>\n'

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
