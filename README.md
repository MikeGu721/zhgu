# Zhouhong Gu · 个人主页

个人介绍、论文与预印本、大事年表、摄影与越野跑记录的中英双语网站。英文为默认入口，中文位于 `/zh/`。

网站使用静态 HTML、CSS 和原生 JavaScript。`scripts/build.py` 通过 Python 标准库读取共用数据，生成两份 HTML；无需 npm、第三方 Python 包、数据库或后台服务。GitHub Actions 会在部署前自动生成页面。

当前数据收录 34 项工作和 14 条年表记录。摄影区已加入 2026 年 11 月 15 日西宏 70 公里越野跑的完赛照片，保留原图与摄影署名。页面使用自托管 DM Sans 与系统中文无衬线字体，正文为 17px，辅助文字最小为 14px。

## 本地生成与预览

在仓库根目录运行：

```sh
python3 scripts/build.py
python3 -m http.server 8000
```

在浏览器中访问：

- 英文页面：<http://localhost:8000/>
- 中文页面：<http://localhost:8000/zh/>

按 `Ctrl+C` 停止预览。修改页面模板、论文或年表数据后，重新执行 `python3 scripts/build.py` 并刷新浏览器。只修改 CSS、JavaScript 或图片时，直接刷新即可。

## 文件位置

| 文件或目录 | 用途 |
| --- | --- |
| `scripts/build.py` | 中英页面生成器、个人介绍、导航及社交链接文案 |
| `data/publications.json` | 共用论文目录、首次公开日期、发表版本、arXiv 与来源记录 |
| `data/timeline.json` | 独立维护的年表事件及双语说明 |
| `index.html` | 生成的英文主页，不作为内容修改入口 |
| `zh/index.html` | 生成的中文主页，不作为内容修改入口 |
| `assets/css/style.css` | 共用样式、文字大小与响应式布局 |
| `assets/fonts/` | 自托管字体及其许可证 |
| `assets/js/publications.js` | 论文搜索与类型筛选 |
| `assets/js/photos.js` | 共用照片清单、标题、说明、署名及日期 |
| `assets/js/gallery.js` | 图库渲染、照片放大与键盘浏览 |
| `assets/photos/` | 照片文件，可按项目建立子目录 |
| `.github/workflows/pages.yml` | 页面生成与 GitHub Pages 自动部署 |

修改个人介绍或社交链接时，请在 `scripts/build.py` 中同步维护英文和中文文案，然后生成页面。直接修改生成的 HTML 会在下次生成时被覆盖。

## 维护论文目录

在 `data/publications.json` 的 `works` 数组中新增或修改条目，并更新文件顶部的 `updated` 日期。可以复制已有条目作为格式参考。

| 字段 | 维护说明 |
| --- | --- |
| `id` | 稳定且唯一的标识；年表用此标识链接到论文。 |
| `title` / `authors` | 论文标题和作者数组；保留来源中的姓名。 |
| `date` | 这项工作**首次公开**的日期，用于倒序排列。可为 `YYYY-MM-DD`、`YYYY-MM` 或 `YYYY`。 |
| `date_precision` | 与日期对应的 `day`、`month` 或 `year`。 |
| `date_basis` | 首次公开日期的来源依据，例如 `arxiv`。 |
| `arxiv` | arXiv 的编号、链接、首次提交日期及标题；没有 arXiv 版本时为 `null`。 |
| `publication` | 正式发表或录用版本的会议/期刊、发布日期、日期精度、状态、链接和来源；没有时为 `null`。 |
| `extra_links` | 可选的其他链接，沿用现有条目的格式。 |

同一工作的会议/期刊版与 arXiv 版合并在一个条目中展示。新增条目前应人工核对题目变化、作者及版本关系；网站不会自动识别或去重。同一条目至少需要一个可访问的 `publication` 或 `arxiv` 链接。

论文日期使用首次公开时间。arXiv 采用来源明确记载的首次提交日期（UTC），不使用最新修订日期，也不从 arXiv 编号推算日期。仅有月份或年份时，保留原精度，不补造月日。正式发表日期与首次公开日期可以不同，分别记录在对应字段中。

生成器会按 `date` 倒序排列全部条目。页面提供“全部”“已录用 / 发表”和“arXiv”筛选，以及标题、作者和年份搜索；这些交互不依赖第三方 JavaScript 库。

## 维护大事年表

年表独立保存在 `data/timeline.json`，不会由论文目录自动生成。修改论文后，如需同步年表，应一并更新相关事件。

- 论文事件按**正式发表时间**记录，`date_kind` 使用 `publication`。日期可精确到日、月或年，`precision` 应与之对应；不将未知日期补为某月 1 日。
- 比赛等个人事件使用已确认的实际发生日期。西宏 70 公里越野跑完赛记录为 `2026-11-15`，`date_kind` 为 `race_completed`。
- 每个事件维护中英文 `title`，并可填写双语 `description`、`note` 和证据 `sources`。
- `papers` 中的 `id` 应与论文目录一致，`label` 是年表中的简短链接文字。同一期刊或会议的多篇论文可以合并为一个事件。
- `link` 可指向相关页面区块，例如比赛事件的 `#photography`。

事件位于 `dated` 数组中，生成时按日期倒序排列；较早记录可在页面展开查看。新增记录时以实际来源为准，并将日期政策与文件顶部的 `date_policy` 保持一致。

## 增添照片

1. 将图片放入 `assets/photos/`，例如 `assets/photos/2026/evening-light.webp`。可以建立子目录；推荐使用简短的英文字母、数字和连字符命名文件。
2. 在 `assets/js/photos.js` 的 `window.PORTFOLIO_PHOTOS` 数组中追加一个对象，各对象之间用逗号分隔。
3. 在本地检查中英文说明、署名和放大浏览效果，再将图片与清单一起提交。

下面仅为格式示例，文件名和文案需替换为真实内容：

```js
{
  src: 'assets/photos/2026/evening-light.webp',
  width: 2400,
  height: 1600,
  alt: {
    en: 'Warm evening light falling across a quiet street.',
    zh: '傍晚的暖光洒在安静的街道上。'
  },
  title: { en: 'Evening light', zh: '晚光' },
  description: {
    en: 'A quiet moment on an evening walk.',
    zh: '傍晚散步时，留下的一刻。'
  },
  credit: { en: 'Photo: Photographer', zh: '摄影：摄影师' },
  location: { en: 'Shanghai', zh: '上海' },
  date: '2026-11-15'
}
```

| 字段 | 填写方式 |
| --- | --- |
| `src` | 必填。以 `assets/photos/` 开头的本仓库图片路径；中英文共用同一路径，不要为中文版添加 `../`。不接受远程图片地址。 |
| `width` / `height` | 图片实际像素宽高，填正整数，便于加载前预留空间。 |
| `alt` | 中英文照片内容描述，供屏幕阅读器和图片无法显示时使用。 |
| `title` | 中英文标题；未填写时显示“无题”或“Untitled”。 |
| `description` | 可选的中英文简短说明，显示在照片卡片及放大视图中。 |
| `credit` | 可选的摄影署名；他人拍摄的个人记录应保留实际摄影者署名。 |
| `location` | 可选的中英文拍摄地点。 |
| `date` | 可选的 `YYYY-MM-DD` 日期；提供时优先于 `year` 显示。 |
| `year` | 兼容原有清单的年份字段，可用字符串或数字；不确定月日时可只填此项。 |

文本字段推荐使用 `{ en: 'English', zh: '中文' }`。缺少中文时会回退到英文，也支持两种语言共用一个字符串。照片按数组顺序展示；调整顺序即可排序，删除对象即可移除相应展示。

当前西宏完赛照片为 `assets/photos/xihong-70km-2026-11-15.jpg`，尺寸 533 × 800，原图与水印未改动，署名为“清补凉”。它是他人为本人拍摄的完赛记录，不应标注为本人摄影作品。

支持 `.jpg`、`.jpeg`、`.png`、`.webp`、`.avif` 和 `.gif`。新照片建议兼顾画质与移动端加载速度，使用 WebP 或 JPG；保留摄影署名，并在发布前检查是否含有不想公开的 EXIF 定位等信息。不要为低分辨率原片强行放大像素尺寸。

图片路径不要包含 `..`、反斜杠、`?`、`#` 或 `%`；直接填写实际文件名，无需 URL 编码。GitHub Pages 区分文件名大小写，路径必须与文件名一致。

## 图库操作

- 点击照片可放大查看，桌面和移动端均可使用。
- 使用界面箭头或键盘左右方向键切换照片，首尾循环。
- 按 `Esc`、点击关闭按钮或遮罩背景可关闭；关闭后焦点返回原照片。
- 只有一张照片时，不显示前后切换按钮。

## GitHub Pages 部署

工作流位于 `.github/workflows/pages.yml`，每次推送到 `main` 后自动运行 `python3 scripts/build.py`，再打包并发布静态页面。首次配置时，仓库 **Settings → Pages → Build and deployment → Source** 应设为 **GitHub Actions**。

日常更新流程为：修改源文件或数据 → 生成页面 → 本地检查中英文与窄屏显示 → 提交并推送 → 在仓库 **Actions** 页面确认部署成功。

发布地址：

- 英文：<https://mikegu721.github.io/zhgu/>
- 中文：<https://mikegu721.github.io/zhgu/zh/>

网站本身不提供在线上传入口。照片通过仓库文件和 `photos.js` 维护；论文与年表通过各自 JSON 数据维护。
