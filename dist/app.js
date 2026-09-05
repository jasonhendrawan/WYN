/**
 * JHCWCH Exact Original Client-Side Application
 * Full HD Direct Google Drive Lightbox + Fast Edge Thumbnails
 */

document.addEventListener('DOMContentLoaded', () => {
  const data = window.WYN_DATA || { past_dates: [], bucket_list: [], favorites: [] };
  const trips = (data.past_dates || []).filter(t => !t.title.toLowerCase().includes('pap sayang aku'));
  
  // Date Helpers for Chronological Sorting & Date Picker
  function parseDateToTimestamp(dateStr) {
    if (!dateStr) return 0;
    const d = new Date(dateStr);
    if (!isNaN(d.getTime())) return d.getTime();

    const parts = dateStr.match(/^(\d{1,2})[\/\-\s](\d{1,2}|[a-zA-Z]+)[\/\-\s](\d{4})/);
    if (parts) {
      const day = parseInt(parts[1], 10);
      let month = parts[2];
      const year = parseInt(parts[3], 10);
      const months = {
        jan: 0, feb: 1, mar: 2, apr: 3, mei: 4, may: 4, jun: 5, jul: 6,
        ags: 7, aug: 7, sep: 8, okt: 9, oct: 9, nov: 10, des: 11, dec: 11
      };
      if (isNaN(month)) {
        const mKey = month.toLowerCase().slice(0, 3);
        month = months[mKey] !== undefined ? months[mKey] : 0;
      } else {
        month = parseInt(month, 10) - 1;
      }
      return new Date(year, month, day).getTime();
    }
    return 0;
  }

  function formatDateToIso(dateStr) {
    const ts = parseDateToTimestamp(dateStr);
    if (!ts) {
      return new Date().toISOString().split('T')[0];
    }
    const d = new Date(ts);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
  }

  function formatDisplayDate(dateStr) {
    if (!dateStr) return '';
    const ts = parseDateToTimestamp(dateStr);
    if (!ts) return dateStr;
    const d = new Date(ts);
    const day = d.getDate();
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const month = monthNames[d.getMonth()];
    const year = d.getFullYear();
    return `${day} ${month} ${year}`;
  }

  function formatExifDateDisplay(dateStr) {
    if (!dateStr) return '';
    const clean = dateStr.replace(/^(\d{4}):(\d{2}):(\d{2})/, '$1-$2-$3');
    return formatDisplayDate(clean);
  }

  function sortTripsChronologically() {
    trips.sort((a, b) => parseDateToTimestamp(a.date) - parseDateToTimestamp(b.date));
  }

  // Apply saved date overrides & uniform '6 Aug 2026' date formatting
  const savedDateOverrides = JSON.parse(localStorage.getItem('trip_date_overrides') || '{}');
  trips.forEach(trip => {
    if (savedDateOverrides[trip.title]) {
      trip.date = savedDateOverrides[trip.title];
    }
    trip.date = formatDisplayDate(trip.date);
  });
  sortTripsChronologically();

  let bucketList = JSON.parse(localStorage.getItem('wyn_bucket_list')) || (data.bucket_list || []);
  let favorites = JSON.parse(localStorage.getItem('wyn_favorites')) || (data.favorites || []);
  let theme = localStorage.getItem('wyn_theme') || 'dark';

  // Helper for URL resolution
  function resolveUrl(url) {
    if (!url) return '';
    if (url.startsWith('http://') || url.startsWith('https://')) return url;
    return url.replace(/^\/+/, '');
  }

  // Extract Google Drive ID
  function extractGDriveId(url) {
    if (!url) return '';
    const match = url.match(/(?:\/d\/|[?&]id=|\/gdrive_cache\/|^gdrive_cache\/|^)([a-zA-Z0-9_-]{20,})/);
    if (match) {
      return match[1].replace(/_thumb$/, '').replace(/\.(jpg|jpeg|png|mp4)$/, '');
    }
    return '';
  }

  // Full HD Local & Direct URLs (uses correctly rotated & transposed local images)
  function getFullHDUrl(url) {
    return resolveUrl(url);
  }

  function getCoverHDUrl(url) {
    return resolveUrl(url);
  }

  // Apply Theme
  document.documentElement.setAttribute('data-theme', theme);
  updateThemeIcon(theme);

  // 1. Calculate Days Together
  function updateDaysTogether() {
    const startDate = new Date('2026-08-02T00:00:00');
    const today = new Date();
    const diffTime = Math.abs(today - startDate);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24)) + 1;
    const daysEl = document.getElementById('daysCount');
    if (daysEl) daysEl.textContent = diffDays;
  }
  updateDaysTogether();

  // 2. Update Stats
  function updateStats() {
    const statTimeline = document.getElementById('statTimelineCount');
    const statHighlights = document.getElementById('statHighlightsCount');
    const statMap = document.getElementById('statMapCount');
    const statPlans = document.getElementById('statPlansCount');

    const favSet = new Set(favorites);
    let favCount = 0;
    trips.forEach(t => {
      (t.images || []).forEach(img => {
        const u = typeof img === 'string' ? img : img.url;
        if (favSet.has(u) || favSet.has(resolveUrl(u))) favCount++;
      });
    });

    if (statTimeline) statTimeline.textContent = trips.length;
    if (statHighlights) statHighlights.textContent = favCount;
    if (statMap) statMap.textContent = trips.length;
    if (statPlans) statPlans.textContent = bucketList.length;
  }
  updateStats();

  // 3. Countdown Banner
  function renderCountdown() {
    const banner = document.getElementById('countdownBanner');
    const titleEl = document.getElementById('countdownTitle');
    const daysEl = document.getElementById('countdownDays');
    const dateEl = document.getElementById('countdownDate');

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let futurePlans = [];
    bucketList.forEach(plan => {
      if (plan.completed || !plan.date) return;
      const pDate = new Date(plan.date);
      if (pDate >= today) {
        const diffDays = Math.ceil((pDate - today) / (1000 * 60 * 60 * 24));
        futurePlans.push({ title: plan.idea, days: diffDays, date: plan.date });
      }
    });

    if (futurePlans.length > 0 && banner) {
      futurePlans.sort((a, b) => a.days - b.days);
      const closest = futurePlans[0];
      titleEl.textContent = closest.title;
      daysEl.textContent = closest.days;
      dateEl.textContent = `(${closest.date})`;
      banner.style.display = 'flex';
    } else if (banner) {
      banner.style.display = 'none';
    }
  }
  renderCountdown();

  // 4. Render Horizontal Alternating Timeline
  const timelineRow = document.getElementById('timelineRow');
  // Drag to slide physics & click handling
  const scrollContainer = document.querySelector('.timeline-scroll-container');
  let isDown = false;
  let startX = 0;
  let scrollStartLeft = 0;
  let dragMoved = false;

  if (scrollContainer) {
    scrollContainer.addEventListener('mousedown', (e) => {
      isDown = true;
      dragMoved = false;
      scrollContainer.classList.add('is-dragging');
      startX = e.pageX - scrollContainer.offsetLeft;
      scrollStartLeft = scrollContainer.scrollLeft;
    });

    window.addEventListener('mouseup', () => {
      if (!isDown) return;
      isDown = false;
      scrollContainer.classList.remove('is-dragging');
    });

    scrollContainer.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - scrollContainer.offsetLeft;
      const walk = (x - startX) * 1.5; // Drag sensitivity
      if (Math.abs(walk) > 6) dragMoved = true;
      scrollContainer.scrollLeft = scrollStartLeft - walk;
    });

    // Mouse wheel horizontal scroll
    scrollContainer.addEventListener('wheel', (e) => {
      if (e.deltaY !== 0) {
        e.preventDefault();
        scrollContainer.scrollLeft += e.deltaY * 0.85;
      }
    }, { passive: false });
  }

  function renderTimeline() {
    if (!timelineRow) return;
    timelineRow.innerHTML = '';

    trips.forEach((trip, index) => {
      const isEven = index % 2 === 0;
      const col = document.createElement('div');
      col.className = 'timeline-column';

      const isVideo = trip.image_path && trip.image_path.toLowerCase().endsWith('.mp4');
      const mediaCoverHD = getCoverHDUrl(trip.image_path);
      const mediaCount = trip.images ? trip.images.length : 0;

      const cardHtml = `
        <div class="glass-trip-card" data-trip-id="${trip.id}">
          <div class="trip-card-cover">
            ${isVideo ?
              `<video src="${resolveUrl(trip.image_path)}" autoplay loop muted playsinline></video>` :
              `<img src="${mediaCoverHD}" alt="${trip.title}" loading="lazy" onerror="this.src='${resolveUrl(trip.image_path)}'" />`
            }
            <div class="trip-media-count-badge">
              <i data-lucide="image" style="width: 12px; height: 12px;"></i>
              <span>${mediaCount}</span>
            </div>
          </div>
          <div class="trip-card-info">
            <span class="trip-badge-date">${trip.date}</span>
            <div class="trip-card-title">${trip.title}</div>
          </div>
        </div>
      `;

      if (isEven) {
        col.innerHTML = `
          <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
            ${cardHtml}
            <div class="vertical-guide top"></div>
          </div>
          <div class="timeline-axis-row">
            <div class="timeline-line-segment"></div>
            <div class="timeline-center-dot"></div>
            <div class="timeline-line-segment"></div>
          </div>
          <div class="timeline-spacer"></div>
        `;
      } else {
        col.innerHTML = `
          <div class="timeline-spacer"></div>
          <div class="timeline-axis-row">
            <div class="timeline-line-segment"></div>
            <div class="timeline-center-dot"></div>
            <div class="timeline-line-segment"></div>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
            <div class="vertical-guide bottom"></div>
            ${cardHtml}
          </div>
        `;
      }

      col.querySelector('.glass-trip-card').addEventListener('click', (e) => {
        if (dragMoved) {
          e.preventDefault();
          return;
        }
        openGalleryModal(trip);
      });

      timelineRow.appendChild(col);
    });
  }
  renderTimeline();

  // 5. Revamped Romantic Highlights Memory Wall
  const highlightsGrid = document.getElementById('highlightsGrid');
  const highlightsTotalText = document.getElementById('highlightsTotalText');
  let activeHighlightFilter = 'all';

  // Filter Buttons
  const hlFilterBtns = document.querySelectorAll('.hl-filter-btn');
  hlFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      hlFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeHighlightFilter = btn.dataset.filter;
      renderHighlights();
    });
  });

  function renderHighlights() {
    if (!highlightsGrid) return;
    highlightsGrid.innerHTML = '';

    const favSet = new Set(favorites);
    let favList = [];

    trips.forEach(trip => {
      (trip.images || []).forEach(img => {
        const u = typeof img === 'string' ? img : img.url;
        const thumb = typeof img === 'object' && img.thumb_url ? img.thumb_url : u;
        const cleanU = resolveUrl(u);

        if (favSet.has(u) || favSet.has(cleanU)) {
          const isVid = (typeof img === 'object' && img.type === 'video') || u.toLowerCase().endsWith('.mp4');
          favList.push({
            url: u,
            thumbUrl: thumb,
            tripTitle: trip.title,
            tripDate: trip.date,
            dateTaken: typeof img === 'object' ? img.date_taken : '',
            type: isVid ? 'video' : 'photo',
            isVideo: isVid
          });
        }
      });
    });

    if (highlightsTotalText) {
      highlightsTotalText.textContent = `${favList.length} Favorite ${favList.length === 1 ? 'Memory' : 'Memories'}`;
    }

    // Filter by type
    let filteredList = favList;
    if (activeHighlightFilter === 'photo') {
      filteredList = favList.filter(item => !item.isVideo);
    } else if (activeHighlightFilter === 'video') {
      filteredList = favList.filter(item => item.isVideo);
    }

    if (filteredList.length === 0) {
      highlightsGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1.5rem; background: var(--glass-bg); border: 1px solid var(--border); border-radius: 24px;">
          <div style="width: 64px; height: 64px; border-radius: 50%; background: rgba(236, 72, 153, 0.12); display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem;">
            <i data-lucide="heart" style="width: 32px; height: 32px; color: #ec4899;"></i>
          </div>
          <h3 style="font-family: var(--font-heading); color: var(--text-main); font-size: 1.35rem; margin-bottom: 0.5rem;">No Moments Here Yet</h3>
          <p style="color: var(--text-muted); font-size: 0.9rem; max-width: 420px; margin: 0 auto 1.5rem; line-height: 1.5;">
            ${favList.length === 0 ? 'Click the ❤️ heart icon on any photo in the timeline gallery to collect your favorite memories here!' : 'No items match this filter category.'}
          </p>
          ${favList.length === 0 ? `
            <button id="goToTimelineFromHlBtn" style="background: linear-gradient(135deg, #ec4899, #a855f7); color: #fff; border: none; border-radius: 999px; padding: 0.55rem 1.4rem; font-weight: 700; font-size: 0.88rem; cursor: pointer; box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);">
              Explore Timeline ✨
            </button>
          ` : ''}
        </div>
      `;

      const goBtn = document.getElementById('goToTimelineFromHlBtn');
      if (goBtn) {
        goBtn.addEventListener('click', () => {
          const timelineTab = document.querySelector('.stat-card[data-tab="timeline"]');
          if (timelineTab) timelineTab.click();
        });
      }

      if (window.lucide) window.lucide.createIcons();
      return;
    }

    filteredList.forEach(item => {
      const card = document.createElement('div');
      card.className = 'polaroid-highlight-card';
      const cleanThumb = resolveUrl(item.thumbUrl || item.url);

      card.innerHTML = `
        <div class="polaroid-media-box">
          <img src="${cleanThumb}" alt="${item.tripTitle}" loading="lazy" onerror="this.src='${getFullHDUrl(item.url)}'" />
          ${item.isVideo ? `
            <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.25);">
              <div style="background: rgba(15, 12, 30, 0.75); backdrop-filter: blur(6px); border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; border: 1.5px solid #fff; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <i data-lucide="play" style="width: 20px; height: 20px; fill: #fff; color: #fff; margin-left: 2px;"></i>
              </div>
            </div>
          ` : ''}
          <button class="heart-unfav-btn" title="Remove from favorites">
            <i data-lucide="heart" style="width: 14px; height: 14px; fill: #ec4899; color: #ec4899;"></i>
          </button>
        </div>
        <div class="polaroid-info-bar">
          <div class="polaroid-title">${item.tripTitle}</div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px;">
            <span class="trip-badge-date" style="font-size: 0.72rem;">${formatDisplayDate(item.tripDate)}</span>
            ${item.dateTaken ? `<span style="font-size: 0.7rem; color: var(--text-muted);">${formatExifDateDisplay(item.dateTaken)}</span>` : ''}
          </div>
        </div>
      `;

      // Click card to open fullscreen lightbox
      card.addEventListener('click', (e) => {
        if (!e.target.closest('.heart-unfav-btn')) {
          openLightbox(item.url, item.isVideo ? 'video' : 'image');
        }
      });

      // Click heart to unfavorite instantly with smooth fade animation
      card.querySelector('.heart-unfav-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        toggleFavorite(item.url);
        updateStats();
        card.style.transition = 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)';
        card.style.opacity = '0';
        card.style.transform = 'scale(0.85) translateY(10px)';
        setTimeout(() => {
          renderHighlights();
        }, 220);
      });

      highlightsGrid.appendChild(card);
    });

    if (window.lucide) window.lucide.createIcons();
  }

  // 6. Interactive Leaflet Map & Google Timeline Visualizer
  function renderMap() {
    const iframe = document.getElementById('mapIframe');
    if (!iframe) return;

    let points = [];
    // Ensure points are strictly chronological
    const sortedTrips = [...trips].sort((a, b) => parseDateToTimestamp(a.date) - parseDateToTimestamp(b.date));

    sortedTrips.forEach(trip => {
      if (trip.location && Array.isArray(trip.location) && trip.location.length === 2) {
        points.push({
          id: trip.id,
          title: trip.title,
          date: trip.date,
          lat: trip.location[0],
          lng: trip.location[1],
          image: trip.image_path || '',
          count: trip.images ? trip.images.length : 0,
          stops: trip.timeline_stops || [],
          path: trip.timeline_path || []
        });
      }
    });

    const isLight = theme === 'light';
    const tileUrl = isLight ?
      'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png' :
      'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';

    const iframeHtml = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
          body, html { margin:0; padding:0; width:100%; height:100%; background:${isLight ? '#f8f5ff' : '#0a0614'}; overflow:hidden; font-family:system-ui, -apple-system, sans-serif; }
          #map { width:100%; height:100%; }
          
          /* High Performance Static Modern Pins */
          .custom-pin-container {
            position: relative;
            width: 38px;
            height: 48px;
            cursor: pointer;
            transition: transform 0.15s ease;
            will-change: transform;
          }
          
          .custom-pin-container:hover, .custom-pin-container.active-pin {
            transform: scale(1.2) translateY(-4px);
            z-index: 1000 !important;
          }
          
          .pin-pulse {
            position: absolute;
            bottom: 0px;
            left: 50%;
            transform: translateX(-50%);
            width: 12px;
            height: 5px;
            background: rgba(168, 85, 247, 0.4);
            border-radius: 50%;
          }

          .pin-teardrop {
            width: 34px;
            height: 34px;
            border-radius: 50% 50% 50% 0;
            background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
            transform: rotate(-45deg);
            box-shadow: 0 4px 12px rgba(236, 72, 153, 0.4), 0 2px 4px rgba(0,0,0,0.3);
            border: 2px solid #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 2px;
            left: 2px;
          }
          
          .pin-inner-number {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #ffffff;
            color: #7c3aed;
            font-size: 11px;
            font-weight: 900;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 4px rgba(255, 255, 255, 0.8);
            transform: rotate(45deg);
            font-family: inherit;
            line-height: 1;
          }

          /* Intermediate day stop numbered badge */
          .stop-dot-number {
            width: 18px;
            height: 18px;
            background: linear-gradient(135deg, #ec4899, #a855f7);
            border: 1.5px solid #ffffff;
            border-radius: 50%;
            box-shadow: 0 2px 6px rgba(236, 72, 153, 0.6);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 9px;
            font-weight: 800;
            transition: transform 0.15s ease;
            line-height: 1;
          }
          .stop-dot-number:hover {
            transform: scale(1.25);
          }

          /* Traveling Car Icon (Lightweight Static Shadow) */
          .traveling-avatar {
            width: 28px;
            height: 28px;
            background: #ec4899;
            border: 2px solid #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 14px rgba(236, 72, 153, 0.75);
            color: #fff;
            font-size: 13px;
          }
          
          .leaflet-popup-content-wrapper {
            background: ${isLight ? 'rgba(255,255,255,0.96)' : 'rgba(18, 9, 36, 0.94)'};
            color: ${isLight ? '#1e1b4b' : '#f1f5f9'};
            border-radius: 16px;
            border: 1px solid rgba(168, 85, 247, 0.35);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            padding: 2px;
            max-width: min(260px, 80vw);
          }
          .leaflet-popup-content {
            margin: 8px;
            line-height: 1.3;
          }
          .leaflet-popup-tip { background: ${isLight ? '#fff' : 'rgba(18, 9, 36, 0.94)'}; }

          /* Floating Glass Journey Control Bar */
          .journey-panel {
            position: absolute;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: ${isLight ? 'rgba(255, 255, 255, 0.95)' : 'rgba(15, 10, 28, 0.94)'};
            border: 1px solid ${isLight ? 'rgba(168, 85, 247, 0.25)' : 'rgba(168, 85, 247, 0.35)'};
            border-radius: 999px;
            padding: 3px 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.45);
            max-width: calc(100vw - 16px);
            width: max-content;
            box-sizing: border-box;
          }

          .j-btn {
            background: ${isLight ? 'rgba(168, 85, 247, 0.12)' : 'rgba(255, 255, 255, 0.08)'};
            border: 1px solid rgba(168, 85, 247, 0.3);
            color: ${isLight ? '#6b21a8' : '#ffffff'};
            border-radius: 999px;
            padding: 3px 8px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 3px;
            transition: all 0.15s ease;
            white-space: nowrap;
            height: 28px;
            box-sizing: border-box;
            line-height: 1;
          }

          .j-btn:hover {
            background: linear-gradient(135deg, #ec4899, #a855f7);
            border-color: transparent;
            color: #fff;
          }

          .j-btn.active {
            background: linear-gradient(135deg, #ec4899, #a855f7);
            border-color: transparent;
            color: #fff;
          }

          .j-status-text {
            font-size: 11px;
            font-weight: 600;
            color: ${isLight ? '#4c1d95' : '#e9d5ff'};
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 135px;
            padding: 0 3px;
          }

          @media (max-width: 480px) {
            .journey-panel {
              padding: 2px 6px;
              gap: 4px;
              bottom: 8px;
              max-width: calc(100vw - 12px);
            }
            .j-btn {
              padding: 2px 6px;
              font-size: 10px;
              height: 25px;
            }
            .j-status-text {
              font-size: 10px;
              max-width: 100px;
            }
          }
        </style>
      </head>
      <body>
        <div id="map"></div>

        <!-- Floating Glassmorphic Journey Visualizer Controls -->
        <div class="journey-panel">
          <!-- Back to All Trips Button (visible during Day mode) -->
          <button id="backAllBtn" class="j-btn" style="display: none; background: rgba(168,85,247,0.25);" title="Return to All Adventures Overview">
            ⬅️ All Trips
          </button>

          <!-- Play Button -->
          <button id="playJourneyBtn" class="j-btn" title="Play animated adventure route">
            <span id="playIcon">▶</span> <span id="playLabel">Play</span>
          </button>
          
          <button id="speedBtn" class="j-btn" title="Toggle animation speed">1x</button>

          <span id="journeyStatus" class="j-status-text">📍 ${points.length} Adventures</span>
        </div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
          var map = L.map('map', { center: [-6.2088, 106.8456], zoom: 11, zoomControl: false, preferCanvas: true });
          L.control.zoom({ position: 'topright' }).addTo(map);
          L.tileLayer('${tileUrl}', { attribution: '&copy; OpenStreetMap &copy; CARTO', maxZoom: 19 }).addTo(map);
          
          var locations = ${JSON.stringify(points)};
          var currentMode = 'all'; // 'all' | 'day'
          var selectedDayIndex = 0;

          var markers = [];
          var dayStopMarkers = [];
          var pathPolylines = [];
          var movingMarker = null;
          var showRoutes = true;

          function createNumberedPin(num) {
            return L.divIcon({
              className: 'leaflet-custom-marker',
              html: '<div class="custom-pin-container">' +
                      '<div class="pin-pulse"></div>' +
                      '<div class="pin-teardrop">' +
                        '<div class="pin-inner-number">' + num + '</div>' +
                      '</div>' +
                    '</div>',
              iconSize: [38, 48],
              iconAnchor: [19, 44],
              popupAnchor: [0, -42]
            });
          }

          function createStopIcon(sidx) {
            return L.divIcon({
              className: 'stop-numbered-marker',
              html: '<div class="stop-dot-number">' + (sidx + 1) + '</div>',
              iconSize: [20, 20],
              iconAnchor: [10, 10],
              popupAnchor: [0, -10]
            });
          }

          var travelerIcon = L.divIcon({
            className: 'traveler-marker',
            html: '<div class="traveling-avatar">🚘</div>',
            iconSize: [28, 28],
            iconAnchor: [14, 14]
          });

          function clearLayers() {
            markers.forEach(function(m) { map.removeLayer(m); });
            dayStopMarkers.forEach(function(m) { map.removeLayer(m); });
            pathPolylines.forEach(function(p) { map.removeLayer(p); });
            markers = [];
            dayStopMarkers = [];
            pathPolylines = [];
            if (movingMarker) { map.removeLayer(movingMarker); movingMarker = null; }
          }

          var backAllBtn = document.getElementById('backAllBtn');
          var playBtn = document.getElementById('playJourneyBtn');
          var playIcon = document.getElementById('playIcon');
          var playLabel = document.getElementById('playLabel');
          var speedBtn = document.getElementById('speedBtn');
          var toggleRoutesBtn = document.getElementById('toggleRoutesBtn');
          var statusText = document.getElementById('journeyStatus');

          function resetPlayButton() {
            isPlaying = false;
            if (playTimer) clearTimeout(playTimer);
            playIcon.textContent = '▶';
            playLabel.textContent = 'Play';
            playBtn.classList.remove('active');
          }

          // 1. Render Mode: ALL TRIPS OVERVIEW (Default - Clean Pins Only, No Connecting Lines)
          function renderAllTripsView() {
            if (isPlaying) stopJourney();
            currentMode = 'all';
            clearLayers();
            resetPlayButton();
            backAllBtn.style.display = 'none';

            var bounds = [];

            locations.forEach(function(loc, index) {
              if (loc.lat && loc.lng) {
                var latlng = [loc.lat, loc.lng];
                bounds.push(latlng);

                var cleanImg = loc.image ? (loc.image.startsWith('http') ? loc.image : loc.image.replace(/^\\/+/, '')) : '';
                var isVid = cleanImg.toLowerCase().endsWith('.mp4') || cleanImg.toLowerCase().endsWith('.webm');
                var mediaHtml = '';
                if (cleanImg) {
                  if (isVid) {
                    mediaHtml = '<video src="' + cleanImg + '" autoplay loop muted playsinline style="width:100%; height:105px; object-fit:cover; border-radius:10px; margin-bottom:8px; box-shadow:0 4px 12px rgba(0,0,0,0.3);"></video>';
                  } else {
                    mediaHtml = '<img src="' + cleanImg + '" style="width:100%; height:105px; object-fit:cover; border-radius:10px; margin-bottom:8px; box-shadow:0 4px 12px rgba(0,0,0,0.3);" onerror="this.style.display=\\'none\\'" />';
                  }
                }
                var stopsCount = (loc.stops && loc.stops.length > 0) ? loc.stops.length : 1;

                var popupContent = '<div style="text-align:center; padding:4px; min-width:190px;">' +
                  mediaHtml +
                  '<strong style="font-size:13px; font-weight:700; display:block; margin-bottom:4px; color:${isLight ? '#1e1b4b' : '#ffffff'};">' + (index + 1) + '. ' + loc.title + '</strong>' +
                  '<span style="font-size:11px; color:#c084fc; font-weight:600; background:rgba(168,85,247,0.18); border:1px solid rgba(168,85,247,0.3); padding:2px 10px; border-radius:999px; display:inline-block; margin-bottom:6px;">' + loc.date + '</span>' +
                  '<div style="font-size:11px; color:${isLight ? '#64748b' : '#94a3b8'}; font-weight:500;">' + (loc.count ? loc.count + ' memories captured 📸' : 'Visited Spot 📍') + '</div>' +
                  '<button onclick="window.playDayFromPopup(' + index + ')" style="margin-top:8px; background:linear-gradient(135deg,#ec4899,#a855f7); color:#fff; border:none; border-radius:999px; padding:5px 12px; font-size:11px; font-weight:700; cursor:pointer; box-shadow:0 4px 12px rgba(236,72,153,0.4);">▶ Play Day Route (' + stopsCount + ' stops)</button>' +
                '</div>';

                var marker = L.marker(latlng, { icon: createNumberedPin(index + 1) }).addTo(map).bindPopup(popupContent, { maxWidth: 260 });
                marker._locData = loc;
                marker._index = index;
                markers.push(marker);
              }
            });

            if (bounds.length > 0) map.fitBounds(bounds, { padding: [60, 60], maxZoom: 14 });
            statusText.textContent = '📍 ' + locations.length + ' Adventures';
          }

          // 2. Render Mode: DETAILED DAY ROUTE (Isolated single date with Named Stops & Real Road Lines)
          function renderDayRouteView(dayIdx, autoPlay = false) {
            if (isPlaying) stopJourney();
            currentMode = 'day';
            selectedDayIndex = dayIdx;
            clearLayers();
            resetPlayButton();
            backAllBtn.style.display = 'inline-flex';

            var loc = locations[dayIdx];
            if (!loc) return;

            var bounds = [];

            // Main Destination Pin
            if (loc.lat && loc.lng) {
              bounds.push([loc.lat, loc.lng]);
              var cleanImg = loc.image ? (loc.image.startsWith('http') ? loc.image : loc.image.replace(/^\\/+/, '')) : '';
              var isVid = cleanImg.toLowerCase().endsWith('.mp4') || cleanImg.toLowerCase().endsWith('.webm');
              var mediaHtml = '';
              if (cleanImg) {
                if (isVid) {
                  mediaHtml = '<video src="' + cleanImg + '" autoplay loop muted playsinline style="width:100%; height:105px; object-fit:cover; border-radius:10px; margin-bottom:8px; box-shadow:0 4px 12px rgba(0,0,0,0.3);"></video>';
                } else {
                  mediaHtml = '<img src="' + cleanImg + '" style="width:100%; height:105px; object-fit:cover; border-radius:10px; margin-bottom:8px; box-shadow:0 4px 12px rgba(0,0,0,0.3);" onerror="this.style.display=\\'none\\'" />';
                }
              }

              var popupContent = '<div style="text-align:center; padding:4px; min-width:190px;">' +
                mediaHtml +
                '<strong style="font-size:13px; font-weight:700; display:block; margin-bottom:4px; color:${isLight ? '#1e1b4b' : '#ffffff'};">' + (dayIdx + 1) + '. ' + loc.title + '</strong>' +
                '<span style="font-size:11px; color:#c084fc; font-weight:600; background:rgba(168,85,247,0.18); border:1px solid rgba(168,85,247,0.3); padding:2px 10px; border-radius:999px; display:inline-block; margin-bottom:6px;">' + loc.date + '</span>' +
                '<div style="font-size:11px; color:${isLight ? '#64748b' : '#94a3b8'}; font-weight:500;">' + (loc.count ? loc.count + ' memories captured 📸' : 'Main Destination 📍') + '</div>' +
              '</div>';

              var marker = L.marker([loc.lat, loc.lng], { icon: createNumberedPin(dayIdx + 1) }).addTo(map).bindPopup(popupContent, { maxWidth: 260 });
              marker._locData = loc;
              markers.push(marker);
            }

            // Intermediate Visited Stops for that Day
            if (loc.stops && loc.stops.length > 0) {
              loc.stops.forEach(function(st, sidx) {
                if (st.coords) {
                  bounds.push(st.coords);
                  var stopName = st.name || ('Stop #' + (sidx + 1));
                  var sMarker = L.marker(st.coords, { icon: createStopIcon(sidx) }).addTo(map).bindPopup(
                    '<div style="font-size:12px; text-align:center; padding:4px; min-width:140px;">' +
                      '<strong style="color:${isLight ? '#1e1b4b' : '#fff'}; display:block; font-size:12px; margin-bottom:3px;">' + (sidx + 1) + '. ' + stopName + '</strong>' +
                      '<span style="color:#c084fc; font-weight:600; font-size:11px; background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.25); padding:1px 8px; border-radius:999px; display:inline-block;">' + (st.time || loc.date) + '</span>' +
                    '</div>'
                  );
                  sMarker._stopData = st;
                  sMarker._stopIdx = sidx;
                  dayStopMarkers.push(sMarker);
                }
              });
            }

            // Draw this Day's Exact Real Road GPS Path
            if (showRoutes && loc.path && loc.path.length > 1) {
              loc.path.forEach(function(pt) { bounds.push(pt); });
              var dayPolyline = L.polyline(loc.path, {
                color: '#ec4899',
                weight: 4.5,
                opacity: 0.95,
                className: 'journey-polyline'
              }).addTo(map);
              pathPolylines.push(dayPolyline);
            }

            if (bounds.length > 0) map.fitBounds(bounds, { padding: [60, 60], maxZoom: 15 });
            statusText.textContent = '📅 ' + (dayIdx + 1) + '. ' + loc.title + ' (' + (loc.stops ? loc.stops.length : 1) + ' stops)';

            if (autoPlay) {
              setTimeout(function() {
                startJourney();
              }, 400);
            }
          }

          // Initial Render (Always All Trips by default)
          renderAllTripsView();

          backAllBtn.addEventListener('click', function() {
            renderAllTripsView();
          });

          window.playDayFromPopup = function(idx) {
            renderDayRouteView(idx, true);
          };

          // Playback Engine
          var isPlaying = false;
          var playIndex = 0;
          var speedMultiplier = 1;
          var playTimer = null;

          function stepJourney() {
            var targetList = currentMode === 'all' ? markers : (dayStopMarkers.length > 0 ? dayStopMarkers : markers);
            
            if (!isPlaying || playIndex >= targetList.length) {
              stopJourney();
              if (playIndex >= targetList.length) {
                if (currentMode === 'day') {
                  statusText.textContent = '✨ Day Route Complete! Returning to All Trips...';
                  playLabel.textContent = 'Replay';
                  playIcon.textContent = '🔁';
                  setTimeout(function() {
                    if (!isPlaying && currentMode === 'day') {
                      renderAllTripsView();
                    }
                  }, 2200);
                } else {
                  statusText.textContent = '✨ All Adventures Completed!';
                  playLabel.textContent = 'Replay';
                  playIcon.textContent = '🔁';
                }
              }
              return;
            }

            var marker = targetList[playIndex];
            var latLng = marker.getLatLng();
            
            if (currentMode === 'all') {
              var loc = marker._locData;
              statusText.textContent = '📍 (' + (playIndex + 1) + '/' + targetList.length + ') ' + loc.title + ' • ' + loc.date;
            } else {
              var loc = locations[selectedDayIndex];
              var stopObj = marker._stopData;
              var stopName = (stopObj && stopObj.name) ? stopObj.name : ('Stop ' + (playIndex + 1));
              statusText.textContent = '📍 ' + (playIndex + 1) + '. ' + stopName + ' (' + ((stopObj && stopObj.time) ? stopObj.time : loc.date) + ')';
            }

            // Move traveling avatar
            if (!movingMarker) {
              movingMarker = L.marker([latLng.lat, latLng.lng], { icon: travelerIcon, zIndexOffset: 2000 }).addTo(map);
            } else {
              movingMarker.setLatLng([latLng.lat, latLng.lng]);
            }

            // Fly camera smoothly to location
            var flyDuration = 1.5 / speedMultiplier;
            map.flyTo([latLng.lat, latLng.lng], Math.max(map.getZoom(), currentMode === 'all' ? 13 : 15), {
              animate: true,
              duration: flyDuration
            });

            setTimeout(function() {
              if (isPlaying) {
                marker.openPopup();
                playIndex++;
                playTimer = setTimeout(stepJourney, (2000 / speedMultiplier));
              }
            }, (flyDuration * 1000));
          }

          function startJourney() {
            var targetList = currentMode === 'all' ? markers : (dayStopMarkers.length > 0 ? dayStopMarkers : markers);
            if (targetList.length === 0) return;
            if (playIndex >= targetList.length) playIndex = 0;
            isPlaying = true;
            playIcon.textContent = '⏸';
            playLabel.textContent = 'Pause';
            playBtn.classList.add('active');
            stepJourney();
          }

          function stopJourney() {
            isPlaying = false;
            if (playTimer) clearTimeout(playTimer);
            if (playIndex >= (currentMode === 'all' ? markers.length : (dayStopMarkers.length || markers.length))) {
              playIcon.textContent = '🔁';
              playLabel.textContent = 'Replay';
            } else {
              playIcon.textContent = '▶';
              playLabel.textContent = 'Play';
            }
            playBtn.classList.remove('active');
          }

          playBtn.addEventListener('click', function() {
            if (isPlaying) {
              stopJourney();
            } else {
              startJourney();
            }
          });

          // Speed toggle
          var speeds = [1, 2, 4];
          var speedIdx = 0;
          speedBtn.addEventListener('click', function() {
            speedIdx = (speedIdx + 1) % speeds.length;
            speedMultiplier = speeds[speedIdx];
            speedBtn.textContent = speedMultiplier + 'x';
          });
        </script>
      </body>
      </html>
    `;
    iframe.srcdoc = iframeHtml;
  }

  // 7. Google Keep Style Pure Interactive Checklist
  const keepActiveList = document.getElementById('keepActiveList');
  const keepAddInput = document.getElementById('keepAddInput');
  const keepCompletedToggle = document.getElementById('keepCompletedToggle');
  const keepCompletedList = document.getElementById('keepCompletedList');
  const keepCompletedCountLabel = document.getElementById('keepCompletedCountLabel');
  const keepChevronIcon = document.getElementById('keepChevronIcon');
  let completedExpanded = false;

  function renderKeepChecklist(focusIdx = null) {
    if (!keepActiveList || !keepCompletedList) return;
    keepActiveList.innerHTML = '';
    keepCompletedList.innerHTML = '';

    const completedItems = bucketList.filter(b => b.completed);
    const uncompletedItems = bucketList.filter(b => !b.completed);
    const progressSummary = document.getElementById('plansProgressSummary');

    if (progressSummary) {
      progressSummary.textContent = `${completedItems.length} of ${bucketList.length} completed ✨`;
    }

    // Render Active (Uncompleted) Items
    uncompletedItems.forEach((plan) => {
      const globalIdx = bucketList.indexOf(plan);
      const row = createKeepRow(plan, globalIdx, false);
      keepActiveList.appendChild(row);
    });

    // Render Completed Section
    if (completedItems.length > 0 && keepCompletedToggle) {
      keepCompletedToggle.style.display = 'flex';
      if (keepCompletedCountLabel) {
        keepCompletedCountLabel.textContent = `${completedItems.length} Completed ${completedItems.length === 1 ? 'item' : 'items'}`;
      }
      keepCompletedList.style.display = completedExpanded ? 'flex' : 'none';
      if (keepChevronIcon) {
        keepChevronIcon.style.transform = completedExpanded ? 'rotate(0deg)' : 'rotate(-90deg)';
      }

      completedItems.forEach((plan) => {
        const globalIdx = bucketList.indexOf(plan);
        const row = createKeepRow(plan, globalIdx, true);
        keepCompletedList.appendChild(row);
      });
    } else if (keepCompletedToggle) {
      keepCompletedToggle.style.display = 'none';
      keepCompletedList.style.display = 'none';
    }

    if (focusIdx !== null) {
      const inputs = document.querySelectorAll('.keep-input-text');
      if (inputs[focusIdx]) {
        inputs[focusIdx].focus();
        inputs[focusIdx].setSelectionRange(inputs[focusIdx].value.length, inputs[focusIdx].value.length);
      }
    }

    if (window.lucide) window.lucide.createIcons();
  }

  function createKeepRow(plan, globalIdx, isCompleted) {
    const row = document.createElement('div');
    row.className = 'keep-item-row';

    row.innerHTML = `
      <input type="checkbox" class="keep-checkbox" ${isCompleted ? 'checked' : ''} aria-label="Toggle task" />
      <input type="text" class="keep-input-text ${isCompleted ? 'completed' : ''}" value="${plan.idea.replace(/"/g, '&quot;')}" placeholder="List item" />
      <button class="keep-delete-btn" title="Delete item">
        <i data-lucide="x" style="width: 14px; height: 14px;"></i>
      </button>
    `;

    const checkbox = row.querySelector('.keep-checkbox');
    const input = row.querySelector('.keep-input-text');
    const deleteBtn = row.querySelector('.keep-delete-btn');

    // Checkbox toggle
    checkbox.addEventListener('change', () => {
      plan.completed = checkbox.checked;
      localStorage.setItem('wyn_bucket_list', JSON.stringify(bucketList));
      updateStats();
      renderCountdown();
      renderKeepChecklist();
    });

    // Realtime typing
    input.addEventListener('input', () => {
      plan.idea = input.value;
      localStorage.setItem('wyn_bucket_list', JSON.stringify(bucketList));
      renderCountdown();
    });

    // Keyboard navigation (Enter / Backspace / Arrows)
    input.addEventListener('keydown', (e) => {
      const allInputs = Array.from(document.querySelectorAll('.keep-input-text'));
      const currentIdx = allInputs.indexOf(input);

      if (e.key === 'Enter') {
        e.preventDefault();
        const newItem = { idea: '', category: 'General', date: '', notes: '', completed: false, trip_id: '' };
        bucketList.splice(globalIdx + 1, 0, newItem);
        localStorage.setItem('wyn_bucket_list', JSON.stringify(bucketList));
        updateStats();
        renderKeepChecklist(currentIdx + 1);
      } else if (e.key === 'Backspace' && input.value === '') {
        e.preventDefault();
        bucketList.splice(globalIdx, 1);
        localStorage.setItem('wyn_bucket_list', JSON.stringify(bucketList));
        updateStats();
        renderCountdown();
        renderKeepChecklist(Math.max(0, currentIdx - 1));
      } else if (e.key === 'ArrowDown' && currentIdx < allInputs.length - 1) {
        e.preventDefault();
        allInputs[currentIdx + 1].focus();
      } else if (e.key === 'ArrowUp' && currentIdx > 0) {
        e.preventDefault();
        allInputs[currentIdx - 1].focus();
      }
    });

    // Delete button
    deleteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      bucketList.splice(globalIdx, 1);
      localStorage.setItem('wyn_bucket_list', JSON.stringify(bucketList));
      updateStats();
      renderCountdown();
      renderKeepChecklist();
    });

    return row;
  }

  // "+ List item" input handler
  if (keepAddInput) {
    keepAddInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const val = keepAddInput.value.trim();
        if (val) {
          bucketList.push({ idea: val, category: 'General', date: '', notes: '', completed: false, trip_id: '' });
          localStorage.setItem('wyn_bucket_list', JSON.stringify(bucketList));
          keepAddInput.value = '';
          updateStats();
          renderCountdown();
          renderKeepChecklist();
          // Keep focus in add input for fast typing
          keepAddInput.focus();
        }
      }
    });
  }

  // Completed items toggle
  if (keepCompletedToggle) {
    keepCompletedToggle.addEventListener('click', () => {
      completedExpanded = !completedExpanded;
      if (keepCompletedList) {
        keepCompletedList.style.display = completedExpanded ? 'flex' : 'none';
      }
      if (keepChevronIcon) {
        keepChevronIcon.style.transform = completedExpanded ? 'rotate(0deg)' : 'rotate(-90deg)';
      }
    });
  }

  // 8. Tab Switching (4 Tabs)
  const statCards = document.querySelectorAll('.stat-card');
  const sections = document.querySelectorAll('.view-section');

  statCards.forEach(card => {
    card.addEventListener('click', () => {
      const tab = card.dataset.tab;
      statCards.forEach(c => c.className = 'stat-card');
      card.classList.add(`active-${tab}`);

      sections.forEach(s => s.classList.remove('active'));
      const activeSection = document.getElementById(`${tab}View`);
      if (activeSection) activeSection.classList.add('active');

      if (tab === 'timeline') renderTimeline();
      if (tab === 'highlights') renderHighlights();
      if (tab === 'map') renderMap();
      if (tab === 'plans') renderKeepChecklist();

      if (window.lucide) window.lucide.createIcons();
    });
  });

  // 9. Gallery Modal (Thumbnail Image + Play Badge for Videos)
  const galleryModal = document.getElementById('galleryModal');
  const closeGalleryModal = document.getElementById('closeGalleryModal');
  const galleryModalDate = document.getElementById('galleryModalDate');
  const editGalleryDateBtn = document.getElementById('editGalleryDateBtn');
  const galleryDateEditContainer = document.getElementById('galleryDateEditContainer');
  const galleryDateEditInput = document.getElementById('galleryDateEditInput');
  const saveGalleryDateBtn = document.getElementById('saveGalleryDateBtn');
  const cancelGalleryDateBtn = document.getElementById('cancelGalleryDateBtn');
  const galleryModalTitle = document.getElementById('galleryModalTitle');
  const galleryModalDesc = document.getElementById('galleryModalDesc');
  const galleryModalGrid = document.getElementById('galleryModalGrid');

  let currentEditingTrip = null;

  if (editGalleryDateBtn && galleryDateEditContainer) {
    editGalleryDateBtn.addEventListener('click', () => {
      if (!currentEditingTrip) return;
      galleryDateEditInput.value = formatDateToIso(currentEditingTrip.date);
      galleryDateEditContainer.style.display = 'inline-flex';
      editGalleryDateBtn.style.display = 'none';
      if (typeof galleryDateEditInput.showPicker === 'function') {
        try { galleryDateEditInput.showPicker(); } catch (err) {}
      } else {
        galleryDateEditInput.focus();
      }
    });

    cancelGalleryDateBtn.addEventListener('click', () => {
      galleryDateEditContainer.style.display = 'none';
      editGalleryDateBtn.style.display = 'inline-flex';
    });

    const handleSaveDate = () => {
      if (!currentEditingTrip) return;
      const isoVal = galleryDateEditInput.value;
      if (isoVal) {
        const displayDate = formatDisplayDate(isoVal);
        currentEditingTrip.date = displayDate;
        galleryModalDate.textContent = displayDate;

        // Persist date overrides to localStorage
        const dateOverrides = JSON.parse(localStorage.getItem('trip_date_overrides') || '{}');
        dateOverrides[currentEditingTrip.title] = displayDate;
        localStorage.setItem('trip_date_overrides', JSON.stringify(dateOverrides));

        // Re-sort chronologically and rearrange timeline cards
        sortTripsChronologically();
        renderTimeline();
        renderHighlights();
        updateStats();
      }
      galleryDateEditContainer.style.display = 'none';
      editGalleryDateBtn.style.display = 'inline-flex';
    };

    saveGalleryDateBtn.addEventListener('click', handleSaveDate);
    galleryDateEditInput.addEventListener('change', handleSaveDate);
    galleryDateEditInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleSaveDate();
      if (e.key === 'Escape') {
        galleryDateEditContainer.style.display = 'none';
        editGalleryDateBtn.style.display = 'inline-flex';
      }
    });
  }

  function openGalleryModal(trip) {
    if (!galleryModal) return;
    currentEditingTrip = trip;
    galleryModalDate.textContent = formatDisplayDate(trip.date);
    galleryModalTitle.textContent = trip.title;
    galleryModalDesc.textContent = trip.description || '';

    // Reset date edit state
    if (galleryDateEditContainer) galleryDateEditContainer.style.display = 'none';
    if (editGalleryDateBtn) editGalleryDateBtn.style.display = 'inline-flex';

    galleryModalGrid.innerHTML = '';
    const images = trip.images || [];

    images.forEach(img => {
      const url = typeof img === 'string' ? img : img.url;
      const thumb = typeof img === 'object' && img.thumb_url ? img.thumb_url : url;
      const isVideo = (typeof img === 'object' && img.type === 'video') || url.toLowerCase().endsWith('.mp4');
      const cleanUrl = resolveUrl(url);
      const cleanThumb = resolveUrl(thumb);
      const dateTaken = typeof img === 'object' ? (img.date_taken || '') : '';
      const isFav = favorites.includes(url) || favorites.includes(cleanUrl);

      const item = document.createElement('div');
      item.className = 'gallery-grid-item';

      item.innerHTML = `
        <img src="${cleanThumb}" alt="Photo" loading="lazy" onerror="this.src='${getFullHDUrl(url)}'" />
        ${isVideo ? `
          <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.25);">
            <div style="background: rgba(15, 12, 30, 0.75); backdrop-filter: blur(6px); border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; border: 1.5px solid #fff; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
              <i data-lucide="play" style="width: 20px; height: 20px; fill: #fff; color: #fff; margin-left: 2px;"></i>
            </div>
          </div>
        ` : ''}
        <button class="heart-fav-btn ${isFav ? 'active' : ''}">
          <i data-lucide="heart" style="width: 13px; height: 13px; fill: ${isFav ? '#ec4899' : 'transparent'}; color: ${isFav ? '#ec4899' : '#fff'};"></i>
        </button>
        ${dateTaken ? `<div class="exif-date-badge"><i data-lucide="calendar" style="width: 10px; height: 10px;"></i> ${formatExifDateDisplay(dateTaken)}</div>` : ''}
      `;

      item.addEventListener('click', (e) => {
        if (!e.target.closest('.heart-fav-btn')) {
          openLightbox(url, isVideo ? 'video' : 'image');
        }
      });

      const heartBtn = item.querySelector('.heart-fav-btn');
      heartBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        heartBtn.classList.remove('heart-burst');
        void heartBtn.offsetWidth; // restart anim
        heartBtn.classList.add('heart-burst');
        
        const wasFav = favorites.includes(url) || favorites.includes(cleanUrl);
        const nowFav = !wasFav;
        toggleFavorite(url);
        heartBtn.classList.toggle('active', nowFav);
        const heartIcon = heartBtn.querySelector('i') || heartBtn.querySelector('svg');
        if (heartIcon) {
          heartIcon.style.fill = nowFav ? '#ec4899' : 'transparent';
          heartIcon.style.color = nowFav ? '#ec4899' : '#fff';
        }
        updateStats();
      });

      galleryModalGrid.appendChild(item);
    });

    galleryModal.classList.add('open');
    if (window.lucide) window.lucide.createIcons();
  }

  if (closeGalleryModal) {
    closeGalleryModal.addEventListener('click', () => galleryModal.classList.remove('open'));
  }

  // 10. Fullscreen Full HD Lightbox with Interactive Zoom, Pan & Rotate
  const lightboxModal = document.getElementById('lightboxModal');
  const closeLightboxModal = document.getElementById('closeLightboxModal');
  const lightboxMediaBox = document.getElementById('lightboxMediaBox');
  const lightboxViewport = document.getElementById('lightboxViewport');
  const lightboxZoomInBtn = document.getElementById('lightboxZoomInBtn');
  const lightboxZoomOutBtn = document.getElementById('lightboxZoomOutBtn');
  const lightboxResetBtn = document.getElementById('lightboxResetBtn');
  const lightboxRotateBtn = document.getElementById('lightboxRotateBtn');
  const lightboxZoomBadge = document.getElementById('lightboxZoomBadge');

  let currentZoom = 1.0;
  let panX = 0;
  let panY = 0;
  let currentRotation = 0;
  let isPanning = false;
  let panStartX = 0;
  let panStartY = 0;
  let initialPinchDist = 0;
  let initialPinchZoom = 1.0;

  function updateTransform() {
    if (!lightboxMediaBox) return;
    lightboxMediaBox.style.transform = `translate(${panX}px, ${panY}px) scale(${currentZoom}) rotate(${currentRotation}deg)`;
    if (lightboxZoomBadge) {
      lightboxZoomBadge.textContent = `${Math.round(currentZoom * 100)}%`;
    }
  }

  function resetZoom() {
    currentZoom = 1.0;
    panX = 0;
    panY = 0;
    currentRotation = 0;
    updateTransform();
  }

  function setZoom(newZoom, centerX, centerY) {
    const clampedZoom = Math.min(Math.max(newZoom, 1.0), 5.0);
    if (clampedZoom === currentZoom) return;

    if (centerX !== undefined && centerY !== undefined && lightboxViewport) {
      const rect = lightboxViewport.getBoundingClientRect();
      const ox = centerX - rect.left - rect.width / 2;
      const oy = centerY - rect.top - rect.height / 2;
      const factor = clampedZoom / currentZoom;
      panX = ox - (ox - panX) * factor;
      panY = oy - (oy - panY) * factor;
    }

    if (clampedZoom === 1.0) {
      panX = 0;
      panY = 0;
    }

    currentZoom = clampedZoom;
    updateTransform();
  }

  if (lightboxZoomInBtn) {
    lightboxZoomInBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      setZoom(currentZoom + 0.35);
    });
  }

  if (lightboxZoomOutBtn) {
    lightboxZoomOutBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      setZoom(currentZoom - 0.35);
    });
  }

  if (lightboxResetBtn) {
    lightboxResetBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      resetZoom();
    });
  }

  if (lightboxRotateBtn) {
    lightboxRotateBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      currentRotation = (currentRotation + 90) % 360;
      updateTransform();
    });
  }

  // Mouse Wheel Zoom
  if (lightboxViewport) {
    lightboxViewport.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomDelta = e.deltaY < 0 ? 0.25 : -0.25;
      setZoom(currentZoom + zoomDelta, e.clientX, e.clientY);
    }, { passive: false });

    // Mouse Drag / Pan
    lightboxViewport.addEventListener('mousedown', (e) => {
      if (e.target.closest('.lightbox-top-bar')) return;
      isPanning = true;
      lightboxViewport.classList.add('is-panning');
      panStartX = e.clientX - panX;
      panStartY = e.clientY - panY;
    });

    window.addEventListener('mousemove', (e) => {
      if (!isPanning) return;
      panX = e.clientX - panStartX;
      panY = e.clientY - panStartY;
      updateTransform();
    });

    window.addEventListener('mouseup', () => {
      if (isPanning) {
        isPanning = false;
        if (lightboxViewport) lightboxViewport.classList.remove('is-panning');
      }
    });

    // Double click to toggle zoom (1x <-> 2.2x)
    lightboxViewport.addEventListener('dblclick', (e) => {
      if (e.target.closest('.lightbox-top-bar')) return;
      if (currentZoom > 1.1) {
        resetZoom();
      } else {
        setZoom(2.2, e.clientX, e.clientY);
      }
    });

    // Touch Pinch-to-Zoom & Touch Pan for Mobile
    lightboxViewport.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        isPanning = true;
        panStartX = e.touches[0].clientX - panX;
        panStartY = e.touches[0].clientY - panY;
      } else if (e.touches.length === 2) {
        isPanning = false;
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        initialPinchDist = Math.hypot(dx, dy);
        initialPinchZoom = currentZoom;
      }
    }, { passive: true });

    lightboxViewport.addEventListener('touchmove', (e) => {
      if (e.touches.length === 1 && isPanning && currentZoom > 1.0) {
        e.preventDefault();
        panX = e.touches[0].clientX - panStartX;
        panY = e.touches[0].clientY - panStartY;
        updateTransform();
      } else if (e.touches.length === 2 && initialPinchDist > 0) {
        e.preventDefault();
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        const dist = Math.hypot(dx, dy);
        const factor = dist / initialPinchDist;
        const midX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        const midY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        setZoom(initialPinchZoom * factor, midX, midY);
      }
    }, { passive: false });

    lightboxViewport.addEventListener('touchend', (e) => {
      if (e.touches.length < 2) initialPinchDist = 0;
      if (e.touches.length === 0) isPanning = false;
    });
  }

  function openLightbox(url, type) {
    if (!lightboxModal) return;
    resetZoom();
    const cleanUrl = resolveUrl(url);
    const gdriveId = extractGDriveId(url);

    if (type === 'video') {
      if (gdriveId) {
        lightboxMediaBox.innerHTML = `
          <div style="width: 80vw; max-width: 900px; height: 75vh; display: flex; align-items: center; justify-content: center;">
            <iframe src="https://drive.google.com/file/d/${gdriveId}/preview" 
              style="width: 100%; height: 100%; border: none; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.8);" 
              allow="autoplay; fullscreen" 
              allowfullscreen>
            </iframe>
          </div>
        `;
      } else {
        lightboxMediaBox.innerHTML = `
          <video src="${cleanUrl}" controls autoplay playsinline style="max-height: 75vh; max-width: 100%; border-radius: 8px; box-shadow: 0 10px 40px rgba(0,0,0,0.8);">
            Your browser does not support HTML5 video.
          </video>
        `;
      }
    } else {
      lightboxMediaBox.innerHTML = `
        <img src="${cleanUrl}" alt="Media" class="lightbox-zoom-img" onerror="this.src='${cleanUrl}'" />
      `;
    }

    lightboxModal.classList.add('open');
    if (window.lucide) window.lucide.createIcons();
  }

  if (closeLightboxModal) {
    closeLightboxModal.addEventListener('click', () => {
      lightboxModal.classList.remove('open');
      lightboxMediaBox.innerHTML = '';
    });
  }

  // Close modals on backdrop or ESC
  window.addEventListener('click', (e) => {
    if (e.target === galleryModal) galleryModal.classList.remove('open');
    if (e.target === lightboxModal) {
      lightboxModal.classList.remove('open');
      lightboxMediaBox.innerHTML = '';
    }
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (lightboxModal) {
        lightboxModal.classList.remove('open');
        lightboxMediaBox.innerHTML = '';
      }
      if (galleryModal) galleryModal.classList.remove('open');
    }
  });

  // 11. Add / Edit Plan Modal
  const planModal = document.getElementById('planModal');
  const openAddPlanBtn = document.getElementById('openAddPlanBtn');
  const closePlanModal = document.getElementById('closePlanModal');
  const cancelPlanBtn = document.getElementById('cancelPlanBtn');
  const savePlanBtn = document.getElementById('savePlanBtn');
  const deletePlanBtn = document.getElementById('deletePlanBtn');
  const planModalHeading = document.getElementById('planModalHeading');
  const planIdeaInput = document.getElementById('planIdeaInput');
  const planCategoryInput = document.getElementById('planCategoryInput');
  const planDateInput = document.getElementById('planDateInput');
  const planNotesInput = document.getElementById('planNotesInput');
  const planCompletedInput = document.getElementById('planCompletedInput');

  let editingOriginalIdea = '';

  function openAddPlanModal() {
    editingOriginalIdea = '';
    planModalHeading.textContent = 'Add New Plan';
    planIdeaInput.value = '';
    planCategoryInput.value = 'General';
    planDateInput.value = '';
    planNotesInput.value = '';
    planCompletedInput.checked = false;
    deletePlanBtn.style.display = 'none';
    planModal.classList.add('open');
  }

  function openEditPlanModal(plan) {
    editingOriginalIdea = plan.idea;
    planModalHeading.textContent = 'Edit Plan';
    planIdeaInput.value = plan.idea || '';
    planCategoryInput.value = plan.category || 'General';
    planDateInput.value = plan.date || '';
    planNotesInput.value = plan.notes || '';
    planCompletedInput.checked = Boolean(plan.completed);
    deletePlanBtn.style.display = 'block';
    planModal.classList.add('open');
  }

  if (openAddPlanBtn) openAddPlanBtn.addEventListener('click', openAddPlanModal);
  if (closePlanModal) closePlanModal.addEventListener('click', () => planModal.classList.remove('open'));
  if (cancelPlanBtn) cancelPlanBtn.addEventListener('click', () => planModal.classList.remove('open'));

  if (savePlanBtn) {
    savePlanBtn.addEventListener('click', () => {
      const idea = planIdeaInput.value.trim();
      if (!idea) return alert('Plan title cannot be empty!');

      const newItem = {
        idea: idea,
        category: planCategoryInput.value.trim() || 'General',
        date: planDateInput.value,
        notes: planNotesInput.value.trim(),
        completed: planCompletedInput.checked,
        trip_id: ''
      };

      if (editingOriginalIdea) {
        const idx = bucketList.findIndex(b => b.idea === editingOriginalIdea);
        if (idx !== -1) bucketList[idx] = newItem;
      } else {
        bucketList.push(newItem);
      }

      localStorage.setItem('wyn_bucket_list', JSON.stringify(bucketList));
      planModal.classList.remove('open');
      renderPlansChecklist();
      updateStats();
      renderCountdown();
    });
  }

  if (deletePlanBtn) {
    deletePlanBtn.addEventListener('click', () => {
      if (editingOriginalIdea) {
        bucketList = bucketList.filter(b => b.idea !== editingOriginalIdea);
        localStorage.setItem('wyn_bucket_list', JSON.stringify(bucketList));
        planModal.classList.remove('open');
        renderPlansChecklist();
        updateStats();
        renderCountdown();
      }
    });
  }

  // 12. Helper: Toggle Favorites
  function toggleFavorite(url) {
    const cleanU = resolveUrl(url);
    if (favorites.includes(url) || favorites.includes(cleanU)) {
      favorites = favorites.filter(u => u !== url && u !== cleanU);
    } else {
      favorites.push(cleanU);
    }
    localStorage.setItem('wyn_favorites', JSON.stringify(favorites));
  }

  // 13. Theme Switcher
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('wyn_theme', theme);
      updateThemeIcon(theme);
      renderMap();
    });
  }

  function updateThemeIcon(t) {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    icon.setAttribute('data-lucide', t === 'dark' ? 'sun' : 'moon');
    if (window.lucide) window.lucide.createIcons();
  }

  if (window.lucide) window.lucide.createIcons();
});
