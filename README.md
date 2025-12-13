# Bing Photo Action 🖼️

> 一个完全自动化的解决方案，每日自动采集必应每日一图，永久保存至数据库，并实时生成动态分页网站。
## 👁 预览
### bphoto.xuanbo.top 的屏幕截图
<img src="https://raw.githubusercontent.com/XuanboWangCN/bingphotoaction/refs/heads/main/screenshots.png" 
     alt="bphoto.xuanbo.top的屏幕截图" 
     style="width:50%; height:auto;" 
     title="bphoto.xuanbo.top的屏幕截图">
### 🌍 在线预览

- **Cloudflare Pages**：[https://bingphotoaction.pages.dev/](https://bingphotoaction.pages.dev/)
- **My website**：[https://bphoto.xuanbo.top/](https://bphoto.xuanbo.top/)

## 📋 项目概述

本项目是一套完整的自动化系统，通过GitHub Actions的定时任务机制，每日北京时间12:00自动采集必应搜索首页的精选图片，将其元数据永久保存至JSON数据库，并实时生成具有分页功能的响应式网站。

## ✨ 核心功能

### 🤖 自动化采集
- ⏰ **定时任务**：每日北京时间12:00自动执行（UTC 4:00）
- 🔄 **智能去重**：基于日期自动识别并去除重复数据
- 💾 **永久存储**：所有照片信息永久保存，无限期历史记录

### 📊 数据管理
- 📁 **JSON数据库**：`photos.json`集中存储所有照片元数据
- 🎯 **完整信息**：包含标题、描述、发布日期、版权信息及多种分辨率下载链接
- 🔗 **多分辨率支持**：同时提供1080p和4K (UHD)两种分辨率选项

### 🌐 网站展示
- 📄 **分页系统**：每页显示25张照片，支持无限分页浏览
- 📱 **响应式设计**：
  - 4列布局（≥1200px超大屏幕）
  - 3列布局（992-1199px桌面屏幕）
  - 2列布局（768-991px平板设备）
  - 1列布局（<768px移动设备）
- 🎨 **界面设计**：基于Bootstrap 5.3.3框架，采用现代简洁的卡片设计风格
- ⚡ **动态导航**：支持页码按钮、上一页/下一页导航，当前页面实时高亮显示（最多9个按钮窗口）
- 🔽 **便捷操作**：集成图片下载和必应搜索快捷按钮
- ⚙️ **客户端渲染**：采用Vanilla JavaScript动态渲染，无需服务端处理分页逻辑
- 🚀 **智能加载**：分页JSON按需加载，加载失败自动回退至完整数据库

### 🔍 用户体验优化
- 🖱️ **流畅交互**：点击页码实时切换内容，无需刷新页面
- 🔗 **位置记忆**：通过URL查询参数(`?page=N`)保存浏览位置
- 📝 **元数据展示**：完整显示图片标题、版权信息和发布日期
- 💾 **一键下载**：直接链接到官方1080p和4K版本资源
- 🖼️ **图片懒加载**：采用IntersectionObserver API，仅在图片进入视口时加载高分辨率图像
- ⚡ **性能优化**：通过分页JSON拆分减少单次加载数据量，显著提升大数据集下的加载速度

## 🛠️ 技术栈

### 后端
- **Python 3.11+** — 脚本执行引擎
- **GitHub Actions** — 自动化工作流平台
- **Cron Job** — 定时任务调度机制

### 前端
- **Bootstrap 5.3.3** — UI框架
- **Flexbox** — 响应式布局引擎
- **Vanilla JavaScript** — 客户端交互逻辑
- **HTML5** — 语义化页面结构

### 托管与数据
- **JSON** — 数据持久化格式
- **Cloudflare Pages** — 静态网站托管平台

## 🚀 工作原理

### 第一阶段：自动化采集
```
定时触发 → API数据获取 → 数据验证 → 重复识别 → JSON持久化
```

### 第二阶段：网站生成
```
数据库读取 → 分页处理(25张/页) → HTML静态生成 → 站点索引构建
```

### 第三阶段：用户访问
```
请求处理 → URL参数解析 → 页面动态渲染 → 状态实时高亮
```

## 📁 项目结构

```
bingphotoaction/
├── .github/
│   ├── scripts/
│   │   ├── generate_html.py      # HTML生成脚本（生成分页JSON）
│   │   └── update_photos.py       # 照片数据更新脚本
│   └── workflows/
│       └── fetch-bing-photo.yml   # GitHub Action工作流
├── htmlphotosinfojson/
│   ├── page-1.json               # 第1页照片数据
│   ├── page-2.json               # 第2页照片数据
│   └── ...                        # 更多分页数据
├── index.html                     # 生成的网站（客户端渲染）
├── photos.json                    # 完整照片数据库（备份及回退）
└── README.md                      # 项目说明
```

## 🔄 GitHub Actions 工作流

### 触发机制
- ⏰ **定时触发**：每日UTC 16:00（北京时间00:00）自动执行
- 🔘 **手动触发**：支持通过`workflow_dispatch`事件按需手动执行

### 工作步骤
```yaml
1. 代码库检出与环境准备
2. 必应API调用获取照片数据写入 photo.json
3. 执行 update_photos.py 增量合并数据至 photos.json
4. 执行 generate_html.py 生成分页网站HTML及JSON数据
   - 按25张/页拆分生成分页JSON文件（page-1.json, page-2.json ...）
   - 输出至 htmlphotosinfojson/ 目录
   - 生成最小化HTML文件，包含客户端渲染脚本
5. 提交 photos.json、index.html、htmlphotosinfojson/ 至远程仓库
```

## 📊 数据结构示例

### photos.json 结构
```json
[
  {
    "title": "冰封的倒影",
    "copyright": "默塞德河, 优胜美地国家公园...",
    "copyrightLink": "https://www.bing.com/search?q=...",
    "startDate": "20251212",
    "endDate": "20251213",
    "url": "https://www.bing.com/th?id=OHR...",
    "urlBase": "https://www.bing.com/th?id=OHR...",
    "raw": { ... }
  }
]
```

### htmlphotosinfojson/page-{n}.json 结构
> 客户端优先请求分页JSON，结构与photos.json相同，但只包含该页的25条数据（最后一页可能少于25条）

```json
[
  { "title": "...", "copyright": "...", "startDate": "...", "url": "...", ... },
  { "title": "...", "copyright": "...", "startDate": "...", "url": "...", ... },
  ...（共25条或更少）
]
```

#### 加载策略
1. **首选**：尝试加载 `htmlphotosinfojson/page-{n}.json`（仅需25条数据）
2. **回退**：若404则加载完整 `photos.json`，在客户端切割该页数据
3. **优势**：大幅减少带宽占用，特别是在数据集很大时提升加载速度

## 🎨 功能详解

### 卡片展示模块
- 🖼️ 高分辨率图片预览显示
- 📌 图片标题与版权信息展示
- 🔗 必应搜索结果跳转链接
- ⬇️ 多分辨率下载选项

### 分页导航模块
```
[上一页] [1] [2] [3] ... [下一页]
当前位置：第 1 / 10 页 (单页容量：25张)
```

### 交互按钮模块
- **图片下载**：下拉菜单选择1080p或4K分辨率
- **搜索查看**：跳转至必应搜索结果页面

## 🔧 本地部署指南

### 系统要求
- Python 3.11 或更高版本

### 部署步骤
```bash
# 步骤1：克隆或Fork项目至本地
git clone https://github.com/yourusername/bingphotoaction.git
cd bingphotoaction

# 步骤2：手动执行脚本进行功能测试
python .github/scripts/update_photos.py
python .github/scripts/generate_html.py

# 步骤3：推送至GitHub以启用自动工作流
git push origin main
```

### GitHub Actions 配置
1. 进入仓库的 Settings → Actions → General 页面
2. 确保 "Allow all actions" 选项已启用
3. 工作流将自动在每日北京时间00:00执行

## 📄 开源协议

本项目采用 **知识共享署名协议 4.0 国际版本（CC-BY 4.0）** 发布。

### 协议条款
**您可以自由地：**
- **共享** — 在任何媒介以任何形式复制、发行本作品
- **修改** — 创建本作品的衍生作品

**惟须遵守下列条件：**
- **署名** — 您必须给出适当的署名，提供指向本许可证的链接，同时标明本作品是否已被修改

详细条款请参阅：[CC-BY 4.0 完整许可证](https://creativecommons.org/licenses/by/4.0/deed.zh_Hans)

## 🔗 相关资源

| 资源名称 | 链接 | 说明 |
|--------|------|------|
| 项目主站 | [bingphotoaction.pages.dev](https://bingphotoaction.pages.dev/) | 完整功能展示 |
| 备用镜像 | [bphoto.xuanbo.top](https://bphoto.xuanbo.top/) 
| API接口 | [bingphotoapi.xuanbo.top/info](https://bingphotoapi.xuanbo.top/info) | 必应照片信息API |
| 源代码仓库 | [GitHub仓库](https://github.com/XuanboWangCN/bingphotoaction) | 源代码托管 |

---

⭐ **如果本项目对您有所帮助，诚邀您点击右上角的Star按钮予以支持！**

❓ **如有任何问题，欢迎[提交Issue](https://github.com/XuanboWangCN/bingphotoaction/issues)反馈或通过邮件联系。**

最后更新：2025年12月14日







