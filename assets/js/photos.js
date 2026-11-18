/*
 * Photography collection — add photographs and their credits here.
 *
 * 1. Copy images into assets/photos/ (subfolders are supported).
 * 2. Add one object per photograph below, in the desired display order.
 * 3. Supply English and Chinese captions; English is the fallback language.
 *
 * Example (replace the filename and text with your own before uncommenting):
 * {
 *   src: 'assets/photos/my-photograph.jpg',
 *   width: 2400,
 *   height: 1600,
 *   alt: { en: 'A description of what is visible.', zh: '照片内容的描述。' },
 *   title: { en: 'Photograph title', zh: '作品标题' },
 *   description: { en: 'A short caption.', zh: '一段简短的照片说明。' },
 *   credit: { en: 'Photo: Photographer', zh: '摄影：摄影师' },
 *   location: { en: 'Location', zh: '拍摄地点' },
 *   date: '2026-11-15', // YYYY-MM-DD; used instead of year when supplied.
 *   year: '2026'
 * }
 *
 * src is required and must point inside assets/photos/. Supported formats:
 * JPEG, PNG, WebP, AVIF, and GIF. width / height are recommended to reserve
 * image space while loading. All caption fields are optional. Images are
 * served directly by the website; this file is not an upload form.
 */
window.PORTFOLIO_PHOTOS = [
  {
    src: 'assets/photos/xihong-70km-2026-11-15.jpg',
    width: 533,
    height: 800,
    alt: {
      en: 'Zhouhong Gu in an orange running jacket, raising a finish-line banner after the 70 km trail race.',
      zh: '顾洲洪身穿橙色跑步外套，在 70 公里越野跑终点举起完赛横幅。'
    },
    title: {
      en: 'The Ultra-Trail Xihong 168 autumn - 70km',
      zh: '西宏 70 公里越野跑'
    },
    description: {
      en: 'On November 15, 2026, I completed the 70 km race. A finish-line moment to remember, with the banner held high.',
      zh: '2026 年 11 月 15 日，我完成了西宏 70 公里越野跑。在终点举起横幅，把这一刻留作纪念。'
    },
    credit: { en: 'Photo: 清补凉', zh: '摄影：清补凉' },
    date: '2026-11-15'
  }
];
