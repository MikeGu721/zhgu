# Zhouhong Gu · 个人主页

个人介绍、研究论文与摄影作品的中英双语网站。使用 HTML、CSS 和 JavaScript，可直接部署到 GitHub Pages；无需包管理器、构建步骤、数据库或后台服务。

当前尚未添加摄影原片，图库为空，页面保留了作品展示位置。仓库不包含冒充本人作品的演示照片。

## 本地预览

在仓库根目录运行：

```sh
python3 -m http.server 8000
```

在浏览器中访问：

- 英文页面：<http://localhost:8000/>
- 中文页面：<http://localhost:8000/zh/>

按 `Ctrl+C` 停止预览。修改文件后刷新浏览器即可，无需安装依赖。

## 文件位置

| 文件或目录 | 用途 |
| --- | --- |
| `index.html` | 英文主页：介绍、论文、社交链接等 |
| `zh/index.html` | 中文主页：与英文版对应的内容 |
| `assets/css/style.css` | 两种语言共用的样式与响应式布局 |
| `assets/js/photos.js` | 摄影作品清单、标题、描述、地点和年份 |
| `assets/js/gallery.js` | 图库渲染、照片放大与键盘浏览 |
| `assets/photos/` | 实际摄影图片，可按项目建立子目录 |
| `.github/workflows/pages.yml` | GitHub Pages 自动部署工作流 |

修改个人介绍、论文或社交链接时，请同步更新两份 HTML。增添照片只需修改共用的图片清单，无需分别编辑两个页面。

## 增添摄影作品

1. 将准备好的图片放入 `assets/photos/`，例如 `assets/photos/2026/evening-light.webp`。可以建立子目录；推荐使用简短的英文字母、数字和连字符命名文件。
2. 打开 `assets/js/photos.js`，将 `window.PORTFOLIO_PHOTOS = [];` 改为包含作品对象的数组。已有作品时，在数组里继续追加对象，对象之间用逗号分隔。
3. 在本地检查中英文标题、图片描述和放大浏览效果，再将图片与清单一起提交到仓库。

下面仅为填写格式示例，文件名和文字需替换为自己的真实作品：

```js
window.PORTFOLIO_PHOTOS = [
  {
    src: 'assets/photos/2026/evening-light.webp',
    width: 2400,
    height: 1600,
    alt: {
      en: 'Warm evening light falling across a quiet street.',
      zh: '傍晚的暖光洒在安静的街道上。'
    },
    title: {
      en: 'Evening light',
      zh: '晚光'
    },
    location: {
      en: 'Shanghai',
      zh: '上海'
    },
    year: '2026'
  }
];
```

字段说明：

| 字段 | 填写方式 |
| --- | --- |
| `src` | 必填。以 `assets/photos/` 开头的图片路径；中英文共用同一路径，不要为中文版添加 `../`。仅支持本仓库图片，不接受远程图片地址。 |
| `width` / `height` | 图片的实际像素宽高，填正整数。建议填写，便于图片加载前预留空间。 |
| `alt` | 建议填写中英文的照片内容描述，供屏幕阅读器和图片无法显示时使用。描述看得见的内容，不必重复“这是一张照片”。 |
| `title` | 中英文作品标题；未填写时显示“无题”或“Untitled”。 |
| `location` | 可选的中英文拍摄地点；不希望公开时可省略。 |
| `year` | 可选的拍摄年份，可用字符串或数字。 |

`alt`、`title`、`location` 推荐使用 `{ en: 'English', zh: '中文' }`。缺少中文时会回退到英文；也支持两种语言共用一个字符串。各作品按数组顺序展示，调整对象顺序即可排序；删除对象即可从页面移除对应作品。清空数组会恢复留白状态。

支持 `.jpg`、`.jpeg`、`.png`、`.webp`、`.avif` 和 `.gif`。建议优先使用 WebP 或 JPG，将宽度控制在约 1600–2400 像素、单张文件约 500 KB，并兼顾画质与移动端加载速度。发布前请自行移除照片 EXIF 中不想公开的定位等信息，保留原片在自己的存储中。

图片路径不要包含 `..`、反斜杠、`?`、`#` 或 `%`；直接填写实际文件名，无需 URL 编码。GitHub Pages 区分文件名大小写，请确保路径与文件名完全一致。

## 图库操作

- 点击照片可放大查看，桌面和移动端均可使用。
- 使用界面箭头或键盘左右方向键切换照片，首尾循环。
- 按 `Esc`、点击关闭按钮或点击遮罩背景可关闭；关闭后焦点返回原照片。
- 只有一张照片时，不显示前后切换按钮。

## GitHub Pages 部署

工作流位于 `.github/workflows/pages.yml`。首次部署时，在 GitHub 仓库的 **Settings → Pages → Build and deployment** 中将 **Source** 设为 **GitHub Actions**。此操作需要仓库相应权限。

将修改推送到 `main` 后，在仓库 **Actions** 页面查看部署进度与结果；最终访问地址以成功的部署记录或 **Settings → Pages** 显示为准。页面使用相对资源路径，可用于 `/zhgu/` 这样的项目子路径。

更新内容的日常流程为：修改文件 → 本地预览 → 提交并推送 → 等待 Pages 部署成功。网站本身不提供在线上传入口，照片通过仓库文件和 `photos.js` 维护。
