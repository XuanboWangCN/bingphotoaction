import json
import os
from datetime import datetime

PHOTOS_JSON = "photos.json"
HTML_FILE = "index.html"
PHOTOS_PER_PAGE = 12
PAGE_JSON_DIR = "htmlphotosinfojson"
PAGE_JSON_TEMPLATE = os.path.join(PAGE_JSON_DIR, "page-{n}.json")

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
    # 确保目录存在
    if not os.path.exists(PAGE_JSON_DIR):
        os.makedirs(PAGE_JSON_DIR)
    
    with open(PHOTOS_JSON, "r", encoding="utf-8") as f:
        photos = json.load(f)

    # 计算总页数
    total_pages = (len(photos) + PHOTOS_PER_PAGE - 1) // PHOTOS_PER_PAGE

    # 为每一页生成单独的 page-{n}.json，便于客户端按需请求
    photos_html_by_page = {}
    # 确保输出目录存在
    os.makedirs(PAGE_JSON_DIR, exist_ok=True)

    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * PHOTOS_PER_PAGE
        end_idx = start_idx + PHOTOS_PER_PAGE
        page_photos = photos[start_idx:end_idx]

        # 写入单页 JSON 文件到指定目录
        page_json_path = PAGE_JSON_TEMPLATE.format(n=page_num)
        with open(page_json_path, 'w', encoding='utf-8') as pj:
            json.dump(page_photos, pj, ensure_ascii=False, indent=2)

        # 仍保留 HTML 分块（仅用于在不支持 JS 的环境或回退使用）
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
    # 添加分页响应式样式
    html += '    /* 分页响应式样式 */\n'
    html += '    .pagination-container {\n'
    html += '    /*  overflow-x: auto;*/\n'
    html += '      -webkit-overflow-scrolling: touch;\n'
    html += '      padding-bottom: 5px;\n'
    html += '    }\n'
    html += '    .pagination {\n'
    html += '      flex-wrap: nowrap;\n'
    html += '      margin-bottom: 0;\n'
    html += '    }\n'
    html += '    .pagination .page-link {\n'
    html += '      min-width: 40px;\n'
    html += '      text-align: center;\n'
    html += '      padding: 0.375rem 0.5rem;\n'
    html += '      font-size: 0.875rem;\n'
    html += '    }\n'
    html += '    @media (max-width: 767.98px) {\n'
    html += '      .pagination {\n'
    html += '        flex-wrap: wrap;\n'
    html += '        justify-content: center;\n'
    html += '      }\n'
    html += '      .pagination .page-item {\n'
    html += '        margin-bottom: 2px;\n'
    html += '      }\n'
    html += '      .pagination .page-link {\n'
    html += '        padding: 0.25rem 0.375rem;\n'
    html += '        font-size: 0.8125rem;\n'
    html += '        min-width: 36px;\n'
    html += '      }\n'
    html += '    }\n'
    html += '    /* 跳转页面组件 */\n'
    html += '    .page-jump-container {\n'
    html += '      max-width: 300px;\n'
    html += '      margin: 1.5rem auto;\n'
    html += '    }\n'
    html += '    @media (max-width: 767.98px) {\n'
    html += '      .page-jump-container {\n'
    html += '        max-width: 250px;\n'
    html += '      }\n'
    html += '    }\n'
    html += '  </style>\n'
    html += '</head>\n'
    html += '<body>\n'
    html += '  <div class="container py-4">\n'
    html += '    <div class="page-header mb-4">\n'
    html += '      <h1>必应每日一图相册</h1>\n'
    html += '    </div>\n'
    html += '    <div class="subtitle" id="summary">正在加载照片信息…</div>\n'
    html += '    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">\n'
    html += '      <div id="gallery" class="photo-page"></div>\n'
    html += '    </div>\n'
    html += '\n'
    html += '    <!-- 分页导航 -->\n'
    html += '    <nav class="mt-5" aria-label="Page navigation">\n'
    html += '      <div class="pagination-container">\n'
    html += '        <ul class="pagination justify-content-center" id="pagination"></ul>\n'
    html += '      </div>\n'
    html += '    </nav>\n'
    html += '\n'
    html += '    <!-- 跳转到页面组件 -->\n'
    html += '    <div class="page-jump-container">\n'
    html += '      <div class="input-group input-group-sm">\n'
    html += '        <span class="input-group-text">转至</span>\n'
    html += '        <input type="number" id="jumpPageInput" class="form-control" placeholder="页码" min="1" max="' + str(total_pages) + '">\n'
    html += '        <button class="btn btn-primary" type="button" id="jumpPageBtn">跳转</button>\n'
    html += '      </div>\n'
    html += '    </div>\n'
    html += '\n'
    html += '    <div class="text-center mt-3 text-muted">\n'
    html += '      第 <span id="current-page">1</span> / <span id="total-pages">1</span> 页 <br>每页最多显示 <span id="per-page">' + str(PHOTOS_PER_PAGE) + '</span> 张\n'
    html += '    </div>\n'
    html += '  </div>\n'
    html += '\n'
    html += '<footer>\n'
    html += '  <div class="container text-center">\n'
    html += '    <p>Copyright © <a href="https://github.com/XuanboWangCN" target="_blank">XuanboWang</a> 2025. All rights reserved.<br>\n'
    html += '    Powered by <a href="https://xuanbo.top" target="_blank">Xuanbo.top</a><br>在 Github 中查看源代码：<a href="https://github.com/XuanboWangCN/bingphotoaction/" target="_blank">github.com/XuanboWangCN/bingphotoaction</a></p>\n'
    html += '  </div>\n'
    html += '</footer>\n'
    html += '\n'
    html += '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>\n'
    # 客户端会优先请求 page-{n}.json，若不存在则回退到整体 photos.json
    script_block = '''<script>
    (function(){
        const PER_PAGE = __PER_PAGE__;
        const TOTAL_PHOTOS = __TOTAL_PHOTOS__;
        const TOTAL_PAGES = __TOTAL_PAGES__;
        const PAGE_JSON_DIR = '__PAGE_JSON_DIR__';
        let photos = [];
        let observer = null;

        function $(sel){ return document.querySelector(sel); }
        function $$(sel){ return document.querySelectorAll(sel); }
        function getQueryPage(){const p = parseInt(new URLSearchParams(location.search).get('page')) || 1; return Math.max(1,p);}
        function updateURL(page){const url=new URL(location.href);url.searchParams.set('page',page);history.replaceState(null,'',url);}
        function formatDate(d){if(!d) return ''; const s=String(d); if(/^\d{8}$/.test(s)) return `${s.slice(0,4)}/${s.slice(4,6)}/${s.slice(6,8)}`; if(/^\d{12}$/.test(s)) return `${s.slice(0,4)}/${s.slice(4,6)}/${s.slice(6,8)}`; return s;}

        function createCard(item){
            const col=document.createElement('div'); col.className='col';
            const card=document.createElement('div'); card.className='card h-100';
            const img=document.createElement('img'); img.className='card-img-top lazy'; img.alt=item.title||''; img.setAttribute('data-src', item.url||''); img.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22200%22%3E%3Crect width=%22100%25%22 height=%22100%25%22 fill=%22%23eee%22/%3E%3C/svg%3E'; img.loading='lazy';
            const body=document.createElement('div'); body.className='card-body d-flex flex-column';
            const bodyInner=document.createElement('div'); bodyInner.className='flex-grow-1';
            const title=document.createElement('h5'); title.className='card-title'; title.textContent=item.title||'';
            const desc=document.createElement('p'); desc.className='card-text'; desc.textContent=item.copyright||'';
            bodyInner.appendChild(title); bodyInner.appendChild(desc);
            const btnGroup=document.createElement('div'); btnGroup.className='btn-group w-100 mt-2'; btnGroup.role='group';
            const dlGroup=document.createElement('div'); dlGroup.className='btn-group flex-grow-1'; dlGroup.role='group';
            const dlBtn=document.createElement('button'); dlBtn.type='button'; dlBtn.className='btn btn-sm btn-secondary dropdown-toggle'; dlBtn.setAttribute('data-bs-toggle','dropdown'); dlBtn.textContent='下载图片';
            const dlMenu=document.createElement('ul'); dlMenu.className='dropdown-menu';
            const li1080=document.createElement('li'); li1080.innerHTML=`<a class="dropdown-item" href="${item.url}" download>1080p</a>`;
            const li4k=document.createElement('li'); li4k.innerHTML=`<a class="dropdown-item" href="${(item.urlBase||'')}_UHD.jpg" download>UHD (4K)</a>`;
            dlMenu.appendChild(li1080); dlMenu.appendChild(li4k); dlGroup.appendChild(dlBtn); dlGroup.appendChild(dlMenu);
            const viewBtn=document.createElement('a'); viewBtn.className='btn btn-sm btn-primary'; viewBtn.target='_blank'; viewBtn.textContent='在必应中查看'; viewBtn.href=item.copyrightLink||'#';
            btnGroup.appendChild(dlGroup); btnGroup.appendChild(viewBtn);
            body.appendChild(bodyInner); body.appendChild(btnGroup);
            const footer=document.createElement('div'); footer.className='card-footer text-muted'; footer.textContent = formatDate(item.startDate || (item.raw && item.raw.startdate) || item.fullstartdate || '');
            card.appendChild(img); card.appendChild(body); card.appendChild(footer); col.appendChild(card); return col;
        }

        function clearGallery(){const g=$('#gallery'); if(g) g.innerHTML='';}

        function renderFromArray(arr, page){
            clearGallery(); const frag=document.createDocumentFragment(); arr.forEach(it=>frag.appendChild(createCard(it))); $('#gallery').appendChild(frag);
            document.getElementById('current-page').textContent = page; 
            document.getElementById('total-pages').textContent = TOTAL_PAGES; 
            document.getElementById('per-page').textContent = PER_PAGE; 
            updatePagination(page, TOTAL_PAGES); 
            updateURL(page);
            updateJumpPageInput(page);
            if(observer) observer.disconnect(); 
            observer = new IntersectionObserver((entries)=>{ 
                entries.forEach(en=>{ 
                    if(en.isIntersecting){ 
                        const img=en.target; 
                        const src=img.getAttribute('data-src'); 
                        if(src){ 
                            img.src=src; 
                            img.removeAttribute('data-src'); 
                        } 
                        observer.unobserve(img); 
                    } 
                }); 
            }, {rootMargin: '200px'});
            $$('img.lazy').forEach(img=>observer.observe(img));
        }

        function updateJumpPageInput(page) {
            const input = $('#jumpPageInput');
            if (input) {
                input.value = page;
                input.max = TOTAL_PAGES;
            }
        }

        function updatePagination(current, total){
            const container=document.getElementById('pagination'); container.innerHTML=''; const maxButtons=9;
            function makeItem(label,page,disabled,active){ 
                const li=document.createElement('li'); 
                li.className='page-item'+(disabled?' disabled':'')+(active?' active':''); 
                const a=document.createElement('a'); 
                a.className='page-link'; 
                a.href='?page='+page; 
                a.textContent=label; 
                a.addEventListener('click', function(e){ 
                    e.preventDefault(); 
                    if(!disabled) loadPage(page); 
                }); 
                li.appendChild(a); 
                return li; 
            }
            container.appendChild(makeItem('上一页', Math.max(1,current-1), current<=1, false));
            if(total <= maxButtons){ 
                for(let i=1;i<=total;i++) 
                    container.appendChild(makeItem(i,i,false,i===current)); 
            } else { 
                const windowSize = maxButtons - 2; 
                let start = Math.max(2, current - Math.floor(windowSize/2)); 
                let end = start + windowSize -1; 
                if(end >= total){ 
                    end = total-1; 
                    start = end - windowSize +1; 
                } 
                container.appendChild(makeItem(1,1,false,current===1)); 
                if(start>2) container.appendChild(makeItem('...', start-1, true, false)); 
                for(let i=start;i<=end;i++) 
                    container.appendChild(makeItem(i,i,false,i===current)); 
                if(end < total-1) container.appendChild(makeItem('...', end+1, true, false)); 
                container.appendChild(makeItem(total,total,false,current===total)); 
            }
            container.appendChild(makeItem('下一页', Math.min(total, current+1), current>=total, false));
        }

        function loadPage(page){
            page = Math.max(1, Math.min(parseInt(page), TOTAL_PAGES));
            const pageJson = `${PAGE_JSON_DIR}/page-${page}.json`;
            fetch(pageJson, {cache:'no-cache'}).then(r=>{ 
                if(r.ok) return r.json(); 
                throw new Error('no page json'); 
            }).then(arr=>{ 
                renderFromArray(arr, page); 
            }).catch(()=>{ // 回退到整体 photos.json
                fetch('photos.json', {cache:'no-cache'}).then(r=>r.json()).then(all=>{ 
                    const total = Math.ceil(all.length / PER_PAGE) || 1; 
                    const p = Math.max(1, Math.min(page, total)); 
                    const start=(p-1)*PER_PAGE; 
                    renderFromArray(all.slice(start, start+PER_PAGE), p); 
                }).catch(err=>{ 
                    document.getElementById('summary').textContent='加载照片数据失败'; 
                    console.error(err); 
                });
            });
        }

        function initJumpPage() {
            const jumpBtn = $('#jumpPageBtn');
            const jumpInput = $('#jumpPageInput');
            
            if (jumpBtn && jumpInput) {
                // 按钮点击事件
                jumpBtn.addEventListener('click', function() {
                    const page = parseInt(jumpInput.value);
                    if (page >= 1 && page <= TOTAL_PAGES) {
                        loadPage(page);
                    } else {
                        alert('请输入有效的页码 (1-' + TOTAL_PAGES + ')');
                        jumpInput.focus();
                    }
                });
                
                // 输入框回车事件
                jumpInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        jumpBtn.click();
                    }
                });
            }
        }

        window.addEventListener('load', function(){
            // 控制台美化输出
            console.log('%c必应每日一图相册 - Github项目地址：https://github.com/XuanboWangCN/bingphotoaction  \\n知识共享署名协议 4.0 国际版本（CC-BY 4.0）\\n© 2025 XuanboWang（ https://github.com/XuanboWangCN ）. All rights reserved.', 'background: #222; color: #bada55; font-size: 12px; padding: 5px; border-radius: 3px;');
            
            document.getElementById('summary').textContent = `已保存来自必应的 ${TOTAL_PHOTOS} 张图片`;
            loadPage(getQueryPage());
            initJumpPage();
        });
    })();
</script></body></html>'''
    script_block = script_block.replace('__PER_PAGE__', str(PHOTOS_PER_PAGE)).replace('__TOTAL_PHOTOS__', str(len(photos))).replace('__TOTAL_PAGES__', str(total_pages)).replace('__PAGE_JSON_DIR__', PAGE_JSON_DIR.replace('\\','/'))
    html += script_block

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()

