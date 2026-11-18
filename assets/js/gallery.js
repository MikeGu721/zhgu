(() => {
  'use strict';

  const grid = document.getElementById('photo-grid');
  const empty = document.getElementById('gallery-empty');
  const count = document.getElementById('photo-count');
  if (!grid) return;

  const isChinese = document.documentElement.lang.toLowerCase().startsWith('zh');
  const language = isChinese ? 'zh' : 'en';
  const labels = isChinese
    ? { untitled: '无题', photograph: '照片', open: '查看照片', close: '关闭照片', previous: '上一张', next: '下一张', gallery: '摄影作品' }
    : { untitled: 'Untitled', photograph: 'Photograph', open: 'View photograph', close: 'Close photograph', previous: 'Previous photograph', next: 'Next photograph', gallery: 'Photography' };
  const prefix = document.body.dataset.assetPrefix === '../' ? '../' : './';
  const localized = (value, fallback = '') => {
    if (typeof value === 'string') return value;
    if (!value || typeof value !== 'object') return fallback;
    return typeof value[language] === 'string' ? value[language]
      : typeof value.en === 'string' ? value.en : fallback;
  };
  const imagePath = (source) => {
    if (typeof source !== 'string' || !/^assets\/photos\/.+\.(avif|gif|jpe?g|png|webp)$/i.test(source)) return null;
    if (/[\\\u0000-\u001f\u007f?#%]/.test(source)) return null;
    const segments = source.split('/');
    if (segments.some((segment) => !segment || segment === '.' || segment === '..')) return null;
    return prefix + segments.map(encodeURIComponent).join('/');
  };
  const input = Array.isArray(window.PORTFOLIO_PHOTOS) ? window.PORTFOLIO_PHOTOS : [];
  const photographs = input.filter((photo) => photo && typeof photo === 'object')
    .map((photo) => ({ ...photo, imageSource: imagePath(photo.src) }))
    .filter((photo) => photo.imageSource);

  grid.hidden = photographs.length === 0;
  if (empty) empty.hidden = photographs.length > 0;
  if (count) {
    count.hidden = photographs.length === 0;
    count.textContent = isChinese
      ? `${photographs.length} 张照片`
      : `${photographs.length} photograph${photographs.length === 1 ? '' : 's'}`;
  }
  if (!photographs.length) return;

  const create = (tag, className, text) => {
    const element = document.createElement(tag);
    element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  };
  const button = (className, text) => {
    const element = create('button', className, text);
    element.type = 'button';
    return element;
  };
  const titleFor = (photo) => localized(photo.title, labels.untitled);
  const dateFor = (photo) => typeof photo.date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(photo.date)
    ? photo.date : typeof photo.year === 'string' || typeof photo.year === 'number' ? String(photo.year) : '';
  const metadataFor = (photo) => [localized(photo.location), dateFor(photo)]
    .filter(Boolean).join(' · ');
  const altFor = (photo, index) => localized(photo.alt, localized(photo.title, `${labels.photograph} ${index + 1}`));

  const dialog = create('dialog', 'photo-dialog');
  dialog.id = 'photo-dialog';
  dialog.setAttribute('aria-label', labels.gallery);
  const shell = create('div', 'photo-dialog-shell');
  const closeButton = button('photo-dialog-close', '×');
  closeButton.setAttribute('aria-label', labels.close);
  closeButton.autofocus = true;
  const figure = create('figure', 'photo-dialog-figure');
  const enlargedImage = create('img', 'photo-dialog-image');
  const caption = create('figcaption', 'photo-dialog-caption');
  const title = create('h3', 'photo-dialog-title');
  const metadata = create('p', 'photo-dialog-meta');
  const description = create('p', 'photo-dialog-description');
  const credit = create('p', 'photo-dialog-credit');
  caption.append(title, metadata, description, credit);
  figure.append(enlargedImage, caption);
  const controls = create('div', 'photo-dialog-controls');
  const previousButton = button('photo-dialog-prev', '←');
  previousButton.setAttribute('aria-label', labels.previous);
  const counter = create('p', 'photo-dialog-counter');
  counter.setAttribute('role', 'status');
  counter.setAttribute('aria-live', 'polite');
  counter.setAttribute('aria-atomic', 'true');
  const nextButton = button('photo-dialog-next', '→');
  nextButton.setAttribute('aria-label', labels.next);
  previousButton.hidden = nextButton.hidden = photographs.length === 1;
  controls.append(previousButton, counter, nextButton);
  shell.append(closeButton, figure, controls);
  dialog.append(shell);
  document.body.append(dialog);

  let activeIndex = 0;
  let trigger = null;
  let previousOverflow = '';
  const display = (index) => {
    activeIndex = (index + photographs.length) % photographs.length;
    const photo = photographs[activeIndex];
    enlargedImage.src = photo.imageSource;
    enlargedImage.alt = altFor(photo, activeIndex);
    title.textContent = titleFor(photo);
    metadata.textContent = metadataFor(photo);
    metadata.hidden = !metadata.textContent;
    description.textContent = localized(photo.description);
    description.hidden = !description.textContent;
    credit.textContent = localized(photo.credit);
    credit.hidden = !credit.textContent;
    counter.textContent = `${activeIndex + 1} / ${photographs.length}`;
  };
  const open = (index, sourceButton) => {
    trigger = sourceButton;
    display(index);
    if (typeof dialog.showModal !== 'function') {
      // Legacy browsers can still open the original image directly.
      window.location.assign(photographs[index].imageSource);
      return;
    }
    previousOverflow = document.body.style.overflow;
    dialog.showModal();
    document.body.style.overflow = 'hidden';
  };
  closeButton.addEventListener('click', () => dialog.close());
  previousButton.addEventListener('click', () => display(activeIndex - 1));
  nextButton.addEventListener('click', () => display(activeIndex + 1));
  dialog.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      display(activeIndex + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
  // Require the pointer to start and finish on the backdrop, so dragging
  // from a photograph onto the backdrop never closes it accidentally.
  let pointerStartedOutside = false;
  dialog.addEventListener('pointerdown', (event) => {
    pointerStartedOutside = event.target === dialog;
  });
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog && pointerStartedOutside) dialog.close();
    pointerStartedOutside = false;
  });
  dialog.addEventListener('close', () => {
    document.body.style.overflow = previousOverflow;
    if (trigger && trigger.isConnected) trigger.focus({ preventScroll: true });
  });

  const cards = photographs.map((photo, index) => {
    const card = button('photo-card');
    card.setAttribute('aria-label', `${labels.open}: ${titleFor(photo)}`);
    const image = create('img', 'photo-card-image');
    image.src = photo.imageSource;
    image.alt = altFor(photo, index);
    image.loading = 'lazy';
    image.decoding = 'async';
    if (Number.isInteger(photo.width) && photo.width > 0) image.width = photo.width;
    if (Number.isInteger(photo.height) && photo.height > 0) image.height = photo.height;
    const cardCaption = create('span', 'photo-card-caption');
    cardCaption.append(create('span', 'photo-card-title', titleFor(photo)));
    const details = metadataFor(photo);
    if (details) cardCaption.append(create('span', 'photo-card-meta', details));
    const descriptionText = localized(photo.description);
    if (descriptionText) cardCaption.append(create('span', 'photo-card-description', descriptionText));
    const creditText = localized(photo.credit);
    if (creditText) cardCaption.append(create('span', 'photo-card-credit', creditText));
    card.append(image, cardCaption);
    card.addEventListener('click', () => open(index, card));
    return card;
  });
  grid.replaceChildren(...cards);
})();
