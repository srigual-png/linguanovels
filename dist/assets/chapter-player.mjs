/** Optional, same-level playback of all three parts once the quizzes are submitted.
 * Uses the existing quiz progress schema and current audio URLs from each part page.
 * No extra MP3s, storage keys, accounts, or changes to permanent lesson URLs.
 */
export function initChapterPlayer({restoreProgress, storage}) {
  const cards = document.querySelector('.chapter-parts');
  const progress = document.querySelector('[data-progress-units]');
  if (!cards || !progress) return;

  let units;
  try { units = JSON.parse(progress.dataset.progressUnits); } catch { return; }
  if (!Array.isArray(units) || units.length !== 3) return;

  const panel = document.createElement('section');
  panel.className = 'reader-panel';
  panel.setAttribute('aria-label', 'Complete chapter listening');
  const heading = document.createElement('h2');
  heading.textContent = 'Listen to the full chapter';
  const description = document.createElement('p');
  description.className = 'small';
  description.textContent = 'Enjoy parts 1, 2 and 3 in order, without stopping for questions.';
  const status = document.createElement('p');
  status.className = 'small';
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  panel.append(heading, description, status);
  cards.after(panel);

  // Submit each quiz once; a perfect score is not needed.
  if (!units.every(unit => restoreProgress(unit, storage) !== null)) {
    status.textContent = 'Complete the quizzes for all three parts to unlock uninterrupted listening. Any score counts.';
    return;
  }

  const links = Array.from(cards.querySelectorAll('.part-card a[href]'));
  if (links.length !== 3) {
    status.textContent = 'The full-chapter player is temporarily unavailable.';
    return;
  }

  status.textContent = 'Preparing the three audio parts…';

  // Read the authoritative MP3 source from each existing, permanent part page.
  // This remains valid when audio file versions change (e.g. _V228.mp3).
  Promise.all(links.map(async link => {
    const url = new URL(link.getAttribute('href'), location.origin);
    if (url.origin !== location.origin) throw new Error('Unexpected lesson link');
    const response = await fetch(url.pathname, {credentials: 'same-origin'});
    if (!response.ok) throw new Error('Could not load a listening part');
    const html = await response.text();
    const documentForPart = new DOMParser().parseFromString(html, 'text/html');
    const source = documentForPart.querySelector('audio#audio source')?.getAttribute('src');
    if (!source || !/^\/assets\/audio\/[a-zA-Z0-9_-]+\.mp3$/.test(source)) {
      throw new Error('Audio file not found');
    }
    return source;
  })).then(sources => {
    const player = document.createElement('audio');
    player.controls = true;
    player.preload = 'none';
    player.setAttribute('aria-label', 'Play complete chapter');
    player.style.width = '100%';

    const controls = document.createElement('div');
    controls.className = 'form-actions';

    const restart = document.createElement('button');
    restart.type = 'button';
    restart.className = 'button secondary';
    restart.textContent = 'Play from part 1';

    const speedLabel = document.createElement('label');
    speedLabel.textContent = 'Playback speed ';
    const speed = document.createElement('select');
    speed.setAttribute('aria-label', 'Playback speed for full chapter');
    for (const value of ['0.75', '0.85', '1', '1.1', '1.25']) {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value + '×';
      if (value === '1') option.selected = true;
      speed.append(option);
    }
    speedLabel.append(speed);
    controls.append(restart, speedLabel);
    panel.append(player, controls);

    let current = 0;
    function loadPart(index) {
      current = index;
      player.src = sources[current];
      player.load();
      player.playbackRate = Number(speed.value);
      status.textContent = 'Part ' + (current + 1) + ' of 3';
    }

    function playCurrent() {
      player.play().catch(() => {
        status.textContent = 'Part ' + (current + 1) + ' is ready. Tap Play to continue.';
      });
    }

    speed.addEventListener('change', () => { player.playbackRate = Number(speed.value); });
    restart.addEventListener('click', () => { loadPart(0); playCurrent(); });
    player.addEventListener('ended', () => {
      if (current < sources.length - 1) {
        loadPart(current + 1);
        playCurrent(); // Same player: advances automatically when permitted by the browser.
      } else {
        status.textContent = 'Chapter complete! You can replay it whenever you like.';
      }
    });
    player.addEventListener('error', () => {
      status.textContent = 'Audio could not load. Check your connection and try again.';
    });
    loadPart(0);
  }).catch(() => {
    status.textContent = 'The full-chapter audio could not be prepared. Check your connection and reload this page.';
  });
}
