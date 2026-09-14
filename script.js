document.getElementById('year').textContent = new Date().getFullYear();

function applyActiveNavigation() {
  const navLinks = document.querySelectorAll('.top-nav a');
  const currentPage = window.location.pathname.split('/').pop() || 'visitor-home.html';
  const sectionMap = {
    'visitor-home.html': 'visitor-home.html',
    'about.html': 'about.html',
    'church-history.html': 'about.html',
    'services.html': 'services.html',
    'sunday-worship.html': 'services.html',
    'sermons.html': 'sermons.html',
    'events.html': 'events.html',
    'ministries.html': 'ministries.html',
    'youth-ministry.html': 'ministries.html',
    'women-ministry.html': 'ministries.html',
    'men-ministry.html': 'ministries.html',
    'children-ministry.html': 'ministries.html',
    'choir-ministry.html': 'ministries.html',
    'member-area.html': 'member-area.html',
    'member-dashboard.html': 'member-area.html',
    'admin-login.html': 'admin-login.html',
    'admin-dashboard.html': 'admin-login.html',
  };

  const activeTarget = sectionMap[currentPage] || currentPage;

  navLinks.forEach((link) => {
    const linkPath = link.getAttribute('href');
    const isActive = linkPath === activeTarget;

    link.classList.toggle('active', isActive);
    if (isActive) {
      link.setAttribute('aria-current', 'page');
    } else {
      link.removeAttribute('aria-current');
    }
  });
}

applyActiveNavigation();

const API_BASE = 'http://127.0.0.1:8001';
const ACCESS_TOKEN_KEY = 'churchAccessToken';
const CURRENT_USER_KEY = 'churchCurrentUser';

async function fetchFromApi(path, options = {}) {
  const headers = { ...(options.headers || {}) };

  if (!(options.body instanceof FormData) && !headers['Content-Type'] && options.method && options.method !== 'GET') {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  const responseText = await response.text();
  let data = responseText ? JSON.parse(responseText) : null;

  if (!response.ok) {
    throw new Error(data?.detail || data?.message || `Request failed with status ${response.status}`);
  }

  return data;
}

async function loginToApi(email, password) {
  const body = new URLSearchParams({ username: email, password }).toString();

  const response = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data?.detail || 'Login failed');
  }

  return data;
}

function buildSermonCard(item) {
  const image = item.thumbnail_url || item.image_url || 'pic/serene-church-service-stockcake.jpg';
  return `
    <article
      class="sermon-card"
      data-category="${(item.category || 'general').toLowerCase().replace(/\s+/g, '-') }"
      data-tag="${item.category || 'General'}"
      data-title="${item.title || 'Sermon'}"
      data-preacher="${item.preacher || 'Pastor'}"
      data-date="${item.sermon_date || 'TBD'}"
      data-scripture="${item.bible_scripture || 'God\'s Word'}"
      data-description="${item.description || 'Description coming soon.'}"
      data-image="${image}"
    >
      <div class="sermon-thumb" style="background-image: linear-gradient(135deg, rgba(11, 34, 52, 0.35), rgba(18, 61, 89, 0.15)), url('${image}');"></div>
      <div class="sermon-header">
        <div>
          <p class="sermon-tag">${item.category || 'General'}</p>
          <h3>${item.title || 'Sermon'}</h3>
        </div>
        <span class="sermon-date">${item.sermon_date || 'TBD'}</span>
      </div>

      <div class="sermon-meta">
        <span><strong>Preacher:</strong> ${item.preacher || 'Pastor'}</span>
        <span><strong>Scripture:</strong> ${item.bible_scripture || 'God\'s Word'}</span>
      </div>

      <p>${item.description || 'Description coming soon.'}</p>

      <div class="sermon-actions">
        <button type="button" class="media-link">Video</button>
        <button type="button" class="media-link">Audio</button>
        <button type="button" class="media-link">Notes</button>
      </div>
    </article>
  `;
}

function buildEventCard(item) {
  const image = item.image_url || 'pic/serene-church-service-stockcake.jpg';
  const categoryClass = (item.category || 'general').toLowerCase().replace(/\s+/g, '-');

  return `
    <article class="event-card">
      <div class="event-image">
        <img src="${image}" alt="${item.title || 'Church Event'}" />
      </div>
      <div class="event-content">
        <div class="event-topline">
          <span class="event-pill ${categoryClass}">${item.category || 'Event'}</span>
          <span class="event-date">${item.event_date || 'TBD'}</span>
        </div>
        <h3>${item.title || 'Event'}</h3>
        <div class="event-meta">
          <div><span>Time</span><strong>${item.event_time || 'TBD'}</strong></div>
          <div><span>Location</span><strong>${item.location || 'Location TBD'}</strong></div>
          <div><span>Speaker</span><strong>Church Leadership</strong></div>
          <div><span>Registration</span><strong>Open</strong></div>
        </div>
        <p>${item.description || 'Event details coming soon.'}</p>
      </div>
    </article>
  `;
}

function buildMinistryCard(item) {
  const image = item.image_url || 'pic/Praise-and-Worship-58b5c8ba5f9b586046caf1fa.jpg';

  return `
    <article class="feature-block">
      <h3>${item.name || 'Ministry'}</h3>
      <p>${item.tagline || item.description || 'Ministry details coming soon.'}</p>
      <a href="${(item.name || 'ministries').toLowerCase().replace(/\s+/g, '-')}-ministry.html">Explore ${item.name || 'Ministry'}</a>
    </article>
  `;
}

function buildQuoteMarkup(item) {
  return `
    <div class="quote-card">
      <p class="eyebrow accent">Today’s Quote</p>
      <blockquote>“${item.quote_text || 'Faith moves mountains.'}”</blockquote>
      <p class="quote-meta">Quote: ${item.quote_text || 'Faith moves mountains.'}</p>
      <p class="quote-meta">Author: ${item.author || 'Pentecost Church'}</p>
      <p class="quote-meta">Date: ${item.quote_date || 'Today'}</p>
      <p class="quote-meta">Category: ${item.category || 'General'}</p>
      <p class="quote-meta">Status: ${item.status || 'Published'}</p>
    </div>
  `;
}

async function loadSermonsPage() {
  const container = document.querySelector('.sermon-list');
  if (!container) return;

  try {
    const sermons = await fetchFromApi('/api/sermons');
    container.innerHTML = sermons.map(buildSermonCard).join('');
    initializeSermonFilters();
  } catch (error) {
    console.error('Failed to load sermons:', error);
    container.innerHTML = '<p class="site-search-empty">Unable to load sermons right now.</p>';
  }
}

async function loadEventsPage() {
  const container = document.querySelector('.event-grid');
  if (!container) return;

  try {
    const events = await fetchFromApi('/api/events');
    container.innerHTML = events.map(buildEventCard).join('');
  } catch (error) {
    console.error('Failed to load events:', error);
    container.innerHTML = '<p class="site-search-empty">Unable to load upcoming events right now.</p>';
  }
}

async function loadMinistriesPage() {
  const container = document.querySelector('.content-grid');
  if (!container) return;

  try {
    const ministries = await fetchFromApi('/api/ministries');
    container.innerHTML = ministries.map(buildMinistryCard).join('');
  } catch (error) {
    console.error('Failed to load ministries:', error);
    container.innerHTML = '<p class="site-search-empty">Unable to load ministries right now.</p>';
  }
}

async function loadQuotePage() {
  const container = document.querySelector('.container .quote-card');
  if (!container) return;

  try {
    const quotes = await fetchFromApi('/api/quotes');
    const latestQuote = quotes[0] || {
      quote_text: 'Faith moves mountains.',
      author: 'Pastor’s Reflection',
      quote_date: new Date().toISOString().slice(0, 10),
      category: 'Prayer',
      status: 'Published',
    };
    container.outerHTML = buildQuoteMarkup(latestQuote);
  } catch (error) {
    console.error('Failed to load quote:', error);
  }
}

function initializeSermonFilters() {
  const sermonSearch = document.getElementById('sermonSearch');
  const filterButtons = document.querySelectorAll('.filter-btn');
  const sermonCards = document.querySelectorAll('.sermon-card');

  if (!sermonSearch || filterButtons.length === 0 || sermonCards.length === 0) {
    return;
  }

  if (sermonSearch.dataset.bound === 'true') {
    return;
  }

  sermonSearch.dataset.bound = 'true';

  let activeFilter = 'all';

  function applySermonFilters() {
    const searchTerm = sermonSearch.value.trim().toLowerCase();

    sermonCards.forEach((card) => {
      const text = card.textContent.toLowerCase();
      const category = card.dataset.category;
      const matchesFilter = activeFilter === 'all' || category === activeFilter;
      const matchesSearch = !searchTerm || text.includes(searchTerm);

      card.style.display = matchesFilter && matchesSearch ? 'flex' : 'none';
    });
  }

  sermonSearch.addEventListener('input', applySermonFilters);

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.filter;

      filterButtons.forEach((btn) => {
        btn.classList.toggle('active', btn === button);
      });

      applySermonFilters();
    });
  });
}

function initConnectedContent() {
  const page = document.body.dataset.page;

  if (page === 'sermons') {
    loadSermonsPage();
  }

  if (page === 'events') {
    loadEventsPage();
  }

  if (page === 'ministries') {
    loadMinistriesPage();
  }

  if (page === 'quote-of-the-day') {
    loadQuotePage();
  }
}

const siteSearchEntries = [
  {
    title: 'Home',
    href: 'visitor-home.html',
    description: 'Welcome to Pentecost Church and discover the church family.',
  },
  {
    title: 'About',
    href: 'about.html',
    description: 'Learn about church history, vision, mission, and core beliefs.',
  },
  {
    title: 'Services',
    href: 'services.html',
    description: 'Explore the church’s service types, worship rhythm, and weekly gatherings.',
  },
  {
    title: 'Sermons',
    href: 'sermons.html',
    description: 'Search sermons, scripture, preachers, and messages from the church.',
  },
  {
    title: 'Events',
    href: 'events.html',
    description: 'View upcoming events, gatherings, and church activities.',
  },
  {
    title: 'Ministries',
    href: 'ministries.html',
    description: 'See the church ministries and opportunities to serve.',
  },
  {
    title: 'Prayer Request',
    href: 'prayer-request.html',
    description: 'Submit a prayer request for yourself or your family.',
  },
  {
    title: 'Quote of the Day',
    href: 'quote-of-the-day.html',
    description: 'Read today’s encouragement, quote, and devotional inspiration.',
  },
  {
    title: 'Member Area',
    href: 'member-area.html',
    description: 'Access member login and the member dashboard experience.',
  },
];

const adminDashboardDefaults = {
  members: ['Grace Thompson', 'Pastor David', 'Member User'],
  sermons: ['Walking by Faith', 'Power in Prayer', 'Living in God\'s Presence'],
  events: ['Sunday Worship', 'Prayer Meeting', 'Church Conference'],
  ministries: ['Youth Ministry', 'Women\'s Ministry', 'Men\'s Ministry'],
  bibleVerses: ['Psalm 23:1', 'Romans 15:13', 'Joshua 1:9'],
  dailyQuotes: ['Faith moves mountains', 'Pray with expectation', 'God is faithful'],
  prayerRequests: ['Family healing', 'Work guidance', 'Community outreach'],
  offerings: ['Tithe', 'General Offering', 'Thanksgiving Offering'],
  gallery: ['Sunday Worship Gallery', 'Youth Event Photos', 'Prayer Night'],
  announcements: ['Midweek Prayer Service', 'Missionary Outreach', 'Leadership Meeting'],
  websiteSettings: ['Theme Settings', 'Homepage Hero Content', 'Footer Contact Info'],
};

const globalSearchInput = document.getElementById('globalSiteSearch');
const globalSearchResults = document.getElementById('siteSearchResults');

if (globalSearchInput && globalSearchResults) {
  function buildSearchEntries() {
    const pageEntries = siteSearchEntries.map((entry) => ({
      ...entry,
      searchableText: `${entry.title} ${entry.description}`.toLowerCase(),
      type: 'Page',
    }));

    const sermonEntries = Array.from(document.querySelectorAll('.sermon-card')).map((card) => ({
      title: card.dataset.title || card.querySelector('h3')?.textContent?.trim() || 'Sermon',
      href: 'sermons.html',
      description: [
        card.dataset.preacher ? `Preacher: ${card.dataset.preacher}` : '',
        card.dataset.scripture ? `Scripture: ${card.dataset.scripture}` : '',
        card.dataset.description || '',
      ]
        .filter(Boolean)
        .join(' • '),
      searchableText: [
        card.dataset.title || '',
        card.dataset.preacher || '',
        card.dataset.scripture || '',
        card.dataset.description || '',
      ]
        .join(' ')
        .toLowerCase(),
      type: 'Sermon',
    }));

    return [...pageEntries, ...sermonEntries];
  }

  function renderSearchResults() {
    const query = globalSearchInput.value.trim().toLowerCase();

    if (!query) {
      globalSearchResults.classList.remove('visible');
      globalSearchResults.innerHTML = '';
      return;
    }

    const matches = buildSearchEntries().filter((entry) => entry.searchableText.includes(query));

    if (!matches.length) {
      globalSearchResults.innerHTML = '<p class="site-search-empty">No matching pages or sermons were found.</p>';
      globalSearchResults.classList.add('visible');
      return;
    }

    const limitedMatches = matches.slice(0, 6);

    globalSearchResults.innerHTML = limitedMatches
      .map(
        (entry) => `
          <a href="${entry.href}" class="site-search-result">
            <span class="site-search-type">${entry.type}</span>
            <strong>${entry.title}</strong>
            <small>${entry.description}</small>
          </a>
        `
      )
      .join('');

    globalSearchResults.classList.add('visible');
  }

  globalSearchInput.addEventListener('input', renderSearchResults);

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-search')) {
      globalSearchResults.classList.remove('visible');
    }
  });
}

initConnectedContent();

const heroSlides = document.querySelectorAll('.hero-slide');
const heroDots = document.querySelectorAll('.hero-dot');

if (heroSlides.length > 0) {
  let activeSlideIndex = 0;

  function showSlide(index) {
    activeSlideIndex = (index + heroSlides.length) % heroSlides.length;

    heroSlides.forEach((slide, slideIndex) => {
      slide.classList.toggle('active', slideIndex === activeSlideIndex);
    });

    heroDots.forEach((dot, dotIndex) => {
      dot.classList.toggle('active', dotIndex === activeSlideIndex);
    });
  }

  heroDots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      showSlide(index);
      clearInterval(heroCycle);
      heroCycle = setInterval(() => showSlide(activeSlideIndex + 1), 4000);
    });
  });

  let heroCycle = setInterval(() => showSlide(activeSlideIndex + 1), 4000);
}

const sermonSearch = document.getElementById('sermonSearch');
const filterButtons = document.querySelectorAll('.filter-btn');
const sermonCards = document.querySelectorAll('.sermon-card');
const sermonModal = document.getElementById('sermonModal');
const sermonModalThumb = document.getElementById('sermonModalThumb');
const sermonModalTag = document.getElementById('sermonModalTag');
const sermonModalTitle = document.getElementById('sermonModalTitle');
const sermonModalPreacher = document.getElementById('sermonModalPreacher');
const sermonModalDate = document.getElementById('sermonModalDate');
const sermonModalScripture = document.getElementById('sermonModalScripture');
const sermonModalDescription = document.getElementById('sermonModalDescription');

if (sermonSearch && filterButtons.length > 0) {
  let activeFilter = 'all';

  function applySermonFilters() {
    const searchTerm = sermonSearch.value.trim().toLowerCase();

    sermonCards.forEach((card) => {
      const text = card.textContent.toLowerCase();
      const category = card.dataset.category;
      const matchesFilter = activeFilter === 'all' || category === activeFilter;
      const matchesSearch = !searchTerm || text.includes(searchTerm);

      card.style.display = matchesFilter && matchesSearch ? 'flex' : 'none';
    });
  }

  sermonSearch.addEventListener('input', applySermonFilters);

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.filter;

      filterButtons.forEach((btn) => {
        btn.classList.toggle('active', btn === button);
      });

      applySermonFilters();
    });
  });
}

if (sermonModal) {
  const closeModal = () => {
    sermonModal.classList.remove('open');
    sermonModal.setAttribute('aria-hidden', 'true');
  };

  sermonModal.addEventListener('click', (event) => {
    if (event.target.closest('[data-close-modal="true"]')) {
      closeModal();
    }
  });

  const closeButton = sermonModal.querySelector('.close-modal');
  if (closeButton) {
    closeButton.addEventListener('click', closeModal);
  }

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && sermonModal.classList.contains('open')) {
      closeModal();
    }
  });

  sermonCards.forEach((card) => {
    const actions = card.querySelector('.sermon-actions');
    if (!actions || actions.querySelector('.details-link')) {
      return;
    }

    const detailsButton = document.createElement('button');
    detailsButton.type = 'button';
    detailsButton.className = 'media-link details-link';
    detailsButton.textContent = 'View Details';

    actions.prepend(detailsButton);

    detailsButton.addEventListener('click', () => {
      if (sermonModalTag) sermonModalTag.textContent = card.dataset.tag || 'Sermon';
      if (sermonModalTitle) sermonModalTitle.textContent = card.dataset.title || 'Sermon Title';
      if (sermonModalPreacher) sermonModalPreacher.textContent = `Preacher: ${card.dataset.preacher || 'Pastor'}`;
      if (sermonModalDate) sermonModalDate.textContent = `Date: ${card.dataset.date || 'TBD'}`;
      if (sermonModalScripture) sermonModalScripture.textContent = `Scripture: ${card.dataset.scripture || 'God’s Word'}`;
      if (sermonModalDescription) sermonModalDescription.textContent = card.dataset.description || 'Description coming soon.';
      if (sermonModalThumb) {
        sermonModalThumb.style.backgroundImage = `linear-gradient(135deg, rgba(11, 34, 52, 0.35), rgba(18, 61, 89, 0.15)), url('${card.dataset.image || 'pic/serene-church-service-stockcake.jpg'}')`;
      }

      sermonModal.classList.add('open');
      sermonModal.setAttribute('aria-hidden', 'false');
    });
  });
}

const memberProfiles = {
  'member@email.com': {
    name: 'Grace Thompson',
    ministry: "Women's Ministry",
    events: ['Sunday Worship', "Women’s Prayer Meeting", 'Youth Outreach'],
    prayerRequests: ['Family healing', 'Work guidance'],
    givingHistory: ['Tithe - $200', 'Thanksgiving Offering - $100'],
    sermons: ['Faith That Moves Mountains', 'Living in God’s Presence'],
    notifications: ['Volunteer reminder', 'New prayer meeting schedule'],
    nextEvent: 'Sunday Worship',
    givingTotal: '$300',
    prayerCount: 2,
    notificationCount: 2,
  },
  'admin@pentecostchurch.org': {
    name: 'Pastor David',
    ministry: 'Leadership',
    events: ['Church Conference', 'Night Vigil', 'Leadership Meeting'],
    prayerRequests: ['Church revival', 'Community outreach'],
    givingHistory: ['Tithe - $500', 'Building Fund - $250'],
    sermons: ['The Power of Revival', 'Leading with Integrity'],
    notifications: ['Board update', 'Annual conference planning'],
    nextEvent: 'Church Conference',
    givingTotal: '$750',
    prayerCount: 2,
    notificationCount: 2,
  },
};

const prayerRequestForm = document.getElementById('prayerRequestForm');
const prayerRequestMessage = document.getElementById('prayerRequestMessage');

if (prayerRequestForm) {
  prayerRequestForm.addEventListener('submit', (event) => {
    event.preventDefault();

    if (prayerRequestMessage) {
      prayerRequestMessage.textContent = 'Your prayer request has been submitted successfully.';
    }

    prayerRequestForm.reset();
  });
}

const givingSection = document.querySelector('.home-giving-section');
const givingToggleButton = document.getElementById('toggleGivingSection');
const givingForms = document.querySelectorAll('.giving-form');
const givingTabs = document.querySelectorAll('.giving-tab');
const givingPanels = document.querySelectorAll('.giving-panel');

if (givingToggleButton && givingSection) {
  givingToggleButton.addEventListener('click', () => {
    const isExpanded = givingSection.classList.toggle('expanded');

    givingToggleButton.textContent = isExpanded ? 'Hide Giving' : 'View Giving';
    givingToggleButton.setAttribute('aria-expanded', String(isExpanded));

    if (isExpanded && givingTabs.length > 0 && givingPanels.length > 0) {
      const firstTab = givingTabs[0];
      const firstPanel = document.getElementById(`giving-panel-${firstTab.dataset.givingTab.toLowerCase().replace(/\s+/g, '-')}`);

      givingTabs.forEach((button) => {
        const isActive = button === firstTab;
        button.classList.toggle('active', isActive);
        button.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      givingPanels.forEach((panel) => {
        const isActive = panel === firstPanel;
        panel.classList.toggle('active', isActive);
      });
    }
  });
}

if (givingTabs.length > 0 && givingPanels.length > 0) {
  givingTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.givingTab;

      givingTabs.forEach((button) => {
        const isActive = button === tab;
        button.classList.toggle('active', isActive);
        button.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      givingPanels.forEach((panel) => {
        const isActive = panel.dataset.givingPanel === target;
        panel.classList.toggle('active', isActive);
      });
    });
  });
}

if (givingForms.length > 0) {
  givingForms.forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();

      const status = form.querySelector('.giving-form-status');
      const type = form.dataset.givingType || 'Offering';

      if (status) {
        status.textContent = `Thank you for your ${type.toLowerCase()} donation.`;
      }

      form.reset();
    });
  });
}

const contactForm = document.getElementById('contactForm');
const contactFormStatus = document.getElementById('contactFormStatus');

if (contactForm) {
  contactForm.addEventListener('submit', (event) => {
    event.preventDefault();

    if (contactFormStatus) {
      contactFormStatus.textContent = 'Your message has been sent successfully.';
    }

    contactForm.reset();
  });
}

const shareButton = document.querySelector('.share-btn');

if (shareButton) {
  shareButton.addEventListener('click', async () => {
    const verseText = 'The Lord is my shepherd; I shall not want.';
    const shareData = {
      title: 'Pentecost Church - Verse of the Day',
      text: `Verse of the Day: ${verseText}`,
      url: window.location.href,
    };

    if (navigator.share) {
      try {
        await navigator.share(shareData);
      } catch (error) {
        console.log('Share cancelled or failed.', error);
      }
    } else if (navigator.clipboard) {
      await navigator.clipboard.writeText(`${shareData.title}\n${shareData.text}\n${shareData.url}`);
      shareButton.textContent = 'Copied';
      setTimeout(() => {
        shareButton.textContent = 'Share';
      }, 1200);
    }
  });
}

const memberLoginForm = document.querySelector('body[data-page="member-area"] .member-login-form');
const adminLoginForm = document.getElementById('adminLoginForm');

if (memberLoginForm) {
  memberLoginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const emailInput = memberLoginForm.querySelector('input[type="email"]');
    const passwordInput = memberLoginForm.querySelector('input[type="password"]');
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      alert('Please enter your email and password.');
      return;
    }

    try {
      const result = await loginToApi(email, password);
      localStorage.setItem(ACCESS_TOKEN_KEY, result.access_token);
      localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(result.user));
      window.location.href = 'member-dashboard.html';
    } catch (error) {
      alert(error.message || 'Unable to sign in. Please check your credentials.');
    }
  });
}

if (adminLoginForm) {
  adminLoginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const emailInput = adminLoginForm.querySelector('input[type="email"]');
    const passwordInput = adminLoginForm.querySelector('input[type="password"]');
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    if (!email || !password) {
      alert('Please enter your email and password.');
      return;
    }

    try {
      const result = await loginToApi(email, password);
      localStorage.setItem(ACCESS_TOKEN_KEY, result.access_token);
      localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(result.user));
      localStorage.setItem('adminLoggedIn', 'true');
      localStorage.setItem('adminEmail', email);
      window.location.href = 'admin-dashboard.html';
    } catch (error) {
      alert(error.message || 'Invalid admin credentials.');
    }
  });
}

const dashboardPage = document.body.dataset.page === 'member-dashboard';

if (dashboardPage) {
  async function loadMemberDashboard() {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (!token) {
      window.location.href = 'member-area.html';
      return;
    }

    try {
      const user = JSON.parse(localStorage.getItem(CURRENT_USER_KEY) || '{}');
      const profile = await fetchFromApi('/api/users/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      document.getElementById('memberGreeting').textContent = `Welcome back, ${profile.full_name.split(' ')[0]}.`;
      document.getElementById('memberName').textContent = profile.full_name;
      document.getElementById('memberEmail').textContent = profile.email;
      document.getElementById('memberMinistry').textContent = `Role: ${profile.role}`;
      document.getElementById('nextEvent').textContent = 'Sunday Worship';
      document.getElementById('prayerCount').textContent = '1';
      document.getElementById('givingTotal').textContent = '$0';
      document.getElementById('notificationCount').textContent = '1';

      const [events, sermons, notifications] = await Promise.all([
        fetchFromApi('/api/events'),
        fetchFromApi('/api/sermons'),
        fetchFromApi('/api/notifications', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }),
      ]);

      const eventItems = events.slice(0, 3).map((event) => event.title);
      const sermonItems = sermons.slice(0, 3).map((sermon) => sermon.title);
      const notificationItems = notifications.slice(0, 3).map((item) => item.title);

      setListContent('churchEventList', eventItems);
      setListContent('prayerRequestList', ['Prayer request pending']);
      setListContent('givingHistoryList', ['No giving history yet']);
      setListContent('ministryList', ['Member access enabled']);
      setListContent('sermonList', sermonItems);
      setListContent('notificationList', notificationItems);
    } catch (error) {
      console.error('Failed to load member dashboard:', error);
      window.location.href = 'member-area.html';
    }
  }

  loadMemberDashboard();
}

const adminDashboardPage = document.body.dataset.page === 'admin-dashboard';

if (adminDashboardPage) {
  if (localStorage.getItem('adminLoggedIn') !== 'true') {
    window.location.href = 'admin-login.html';
  } else {
    const adminEmail = localStorage.getItem('adminEmail') || 'admin@pentecostchurch.org';
    const adminGreeting = document.getElementById('adminGreeting');

    if (adminGreeting) {
      adminGreeting.textContent = `Welcome, ${adminEmail.split('@')[0]}.`;
    }

    const adminData = JSON.parse(localStorage.getItem('adminDashboardData') || 'null') || adminDashboardDefaults;
    const sectionMap = {
      adminMembersList: ['members', 'members'],
      adminSermonsList: ['sermons', 'sermons'],
      adminEventsList: ['events', 'events'],
      adminMinistriesList: ['ministries', 'ministries'],
      adminBibleVersesList: ['bibleVerses', 'bible verses'],
      adminDailyQuotesList: ['dailyQuotes', 'daily quotes'],
      adminPrayerRequestsList: ['prayerRequests', 'prayer requests'],
      adminOfferingsList: ['offerings', 'offerings'],
      adminGalleryList: ['gallery', 'gallery'],
      adminAnnouncementsList: ['announcements', 'announcements'],
      adminSettingsList: ['websiteSettings', 'website settings'],
    };

    Object.entries(sectionMap).forEach(([listId, [dataKey, label]]) => {
      const list = document.getElementById(listId);
      const currentItems = adminData[dataKey] || adminDashboardDefaults[dataKey] || [];

      if (list) {
        list.innerHTML = currentItems.map((item) => `<li>${item}</li>`).join('');
      }

      const adminListBox = list?.closest('.admin-list-box');
      if (adminListBox && !adminListBox.dataset.editorAdded) {
        adminListBox.dataset.editorAdded = 'true';

        const editor = document.createElement('textarea');
        editor.className = 'admin-edit-area';
        editor.setAttribute('aria-label', `Edit ${label}`);
        editor.value = currentItems.join('\n');

        const saveButton = document.createElement('button');
        saveButton.type = 'button';
        saveButton.className = 'admin-save-btn';
        saveButton.textContent = `Save ${label}`;

        saveButton.addEventListener('click', () => {
          const updatedItems = editor.value
            .split('\n')
            .map((item) => item.trim())
            .filter(Boolean);

          adminData[dataKey] = updatedItems.length ? updatedItems : currentItems;
          localStorage.setItem('adminDashboardData', JSON.stringify(adminData));

          if (list) {
            list.innerHTML = adminData[dataKey].map((item) => `<li>${item}</li>`).join('');
          }

          updateAdminStats(adminData);
        });

        adminListBox.appendChild(editor);
        adminListBox.appendChild(saveButton);
      }
    });

    updateAdminStats(adminData);
  }
}

function updateAdminStats(adminData) {
  const counts = {
    adminMemberCount: adminData.members?.length || 0,
    adminSermonCount: adminData.sermons?.length || 0,
    adminEventCount: adminData.events?.length || 0,
    adminPrayerCount: adminData.prayerRequests?.length || 0,
  };

  Object.entries(counts).forEach(([id, value]) => {
    const stat = document.getElementById(id);
    if (stat) {
      stat.textContent = value;
    }
  });
}

function setListContent(listId, items) {
  const list = document.getElementById(listId);
  if (!list) return;

  list.innerHTML = items.map((item) => `<li>${item}</li>`).join('');
}
