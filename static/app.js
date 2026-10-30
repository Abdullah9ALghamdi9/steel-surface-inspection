const $ = id => document.getElementById(id);
const fileInput = $('image-input');
const dropArea = $('drop-area');
let previewURL = null;
let currentRequest = null;
let requestNumber = 0;

const pct = n => `${(n * 100).toFixed(1)}%`;
const setText = (id, text) => { $(id).textContent = text; };
const allowedMime = new Set(['image/png', 'image/jpeg', 'image/bmp', 'image/webp']);
const allowedExt = /\.(png|jpe?g|bmp|webp)$/i;

function showError(message) {
  setText('error', message);
  $('error').hidden = false;
  $('loading-state').hidden = true;
}

function showFile(file) {
  if (previewURL) URL.revokeObjectURL(previewURL);
  previewURL = URL.createObjectURL(file);
  $('preview').src = previewURL;
  $('preview').hidden = false;
  $('upload-prompt').hidden = true;
  setText('filename', file.name);
  $('filename').hidden = false;
}

function renderResult(data) {
  const prediction = data.prediction;
  setText('defect-title', prediction.defect_english);
  setText('defect-description', prediction.description);
  setText('recommendation', data.recommendation);

  const probabilities = $('probabilities');
  probabilities.replaceChildren();
  for (const item of [...prediction.probabilities].sort((a, b) => b.probability - a.probability)) {
    const row = document.createElement('div');
    row.className = `prob-row ${item.code === prediction.defect_code ? 'is-top' : ''}`;
    const head = document.createElement('div');
    head.className = 'prob-head';
    const name = document.createElement('span');
    name.textContent = item.name_en;
    const score = document.createElement('span');
    score.textContent = pct(item.probability);
    head.append(name, score);
    const track = document.createElement('div');
    track.className = 'prob-track';
    const fill = document.createElement('span');
    fill.style.width = pct(item.probability);
    track.append(fill);
    row.append(head, track);
    probabilities.append(row);
  }
  $('result').hidden = false;
}

async function analyze(file) {
  if (!file) return;
  if (currentRequest) currentRequest.abort();
  const myNumber = ++requestNumber;
  $('error').hidden = true;
  $('result').hidden = true;
  $('empty-state').hidden = true;
  $('loading-state').hidden = false;
  showFile(file);

  if (file.size > 10 * 1024 * 1024) {
    showError('Image is too large. Maximum size: 10 MB.');
    return;
  }
  if (!allowedMime.has(file.type) && !allowedExt.test(file.name)) {
    showError('Unsupported format. Choose PNG, JPG, BMP, or WEBP.');
    return;
  }

  const controller = new AbortController();
  currentRequest = controller;
  const payload = new FormData();
  payload.append('file', file, file.name);
  try {
    const response = await fetch('/api/inspect', {
      method: 'POST',
      body: payload,
      signal: controller.signal
    });
    const data = await response.json();
    if (myNumber !== requestNumber) return;
    if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Unable to analyze this image.');
    $('loading-state').hidden = true;
    renderResult(data);
  } catch (error) {
    if (error.name !== 'AbortError' && myNumber === requestNumber) {
      showError(error.message || 'Could not connect to the server.');
    }
  } finally {
    if (myNumber === requestNumber) currentRequest = null;
  }
}

fileInput.addEventListener('change', () => analyze(fileInput.files?.[0]));
for (const eventType of ['dragenter', 'dragover']) {
  dropArea.addEventListener(eventType, event => {
    event.preventDefault();
    dropArea.classList.add('dragging');
  });
}
for (const eventType of ['dragleave', 'drop']) {
  dropArea.addEventListener(eventType, event => {
    event.preventDefault();
    dropArea.classList.remove('dragging');
  });
}
dropArea.addEventListener('drop', event => {
  const file = event.dataTransfer?.files?.[0];
  if (file) analyze(file);
});
