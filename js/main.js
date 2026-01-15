/**
 * Academic Website - Main JavaScript
 * Includes mobile navigation, publication filtering, and Bibsonomy integration
 */

document.addEventListener('DOMContentLoaded', function() {
    initMobileNav();
    initPublicationFilters();
    initBibsonomy();
    setActiveNavLink();
    initCarouselButtons();
});

/**
 * Carousel scroll buttons
 */
function initCarouselButtons() {
    const carousel = document.querySelector('.pub-carousel');
    const leftBtn = document.querySelector('.carousel-btn-left');
    const rightBtn = document.querySelector('.carousel-btn-right');

    if (!carousel || !leftBtn || !rightBtn) return;

    const scrollAmount = 300;

    leftBtn.addEventListener('click', () => {
        carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    rightBtn.addEventListener('click', () => {
        carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
}

/**
 * Mobile Navigation Toggle
 */
function initMobileNav() {
    const navToggle = document.querySelector('.nav-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (navToggle && mainNav) {
        navToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            const isExpanded = mainNav.classList.contains('active');
            navToggle.setAttribute('aria-expanded', isExpanded);
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mainNav.contains(e.target) && !navToggle.contains(e.target)) {
                mainNav.classList.remove('active');
            }
        });
    }
}

/**
 * Set active navigation link based on current page
 */
function setActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.main-nav a');

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
}

/**
 * Publication Filter Functionality
 */
function initPublicationFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const publications = document.querySelectorAll('.publication-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;

            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Filter publications
            publications.forEach(pub => {
                if (filter === 'all' || pub.dataset.type === filter) {
                    pub.style.display = 'block';
                } else {
                    pub.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Bibsonomy API Integration
 * Fetches publications dynamically from Bibsonomy
 */

// Configuration
const BIBSONOMY_CONFIG = {
    username: 'cflath'
};

const OPENALEX_CONFIG = {
    authorId: 'A5073782971'  // OpenAlex author ID for Christoph M. Flath
};

/**
 * Initialize Bibsonomy integration if on publications page
 * Auto-loads publications on page load
 */
function initBibsonomy() {
    const pubContainer = document.getElementById('bibsonomy-publications');
    const staticContent = document.querySelectorAll('.static-publication-list, h2.static-section-title');
    const staticFooter = document.getElementById('static-footer');

    if (pubContainer) {
        // Hide static content
        staticContent.forEach(el => el.style.display = 'none');
        if (staticFooter) staticFooter.style.display = 'none';

        // Show and load dynamic content
        pubContainer.style.display = 'block';
        loadBibsonomyPublications(pubContainer);
    }

    // Load citation metrics from OpenAlex
    loadOpenAlexMetrics();
}

/**
 * Fetch author metrics from OpenAlex API
 */
async function loadOpenAlexMetrics() {
    const pubCountEl = document.getElementById('pub-count');
    const citationsEl = document.getElementById('citation-count');
    const hIndexEl = document.getElementById('h-index');

    if (!citationsEl && !hIndexEl && !pubCountEl) return;

    try {
        const response = await fetch(`https://api.openalex.org/authors/${OPENALEX_CONFIG.authorId}`);
        if (!response.ok) throw new Error('Failed to fetch');

        const author = await response.json();

        // Set pub count from OpenAlex on all pages
        if (pubCountEl && author.works_count) {
            pubCountEl.textContent = author.works_count.toLocaleString();
        }
        if (citationsEl && author.cited_by_count) {
            citationsEl.textContent = author.cited_by_count.toLocaleString();
        }
        if (hIndexEl && author.summary_stats?.h_index) {
            hIndexEl.textContent = author.summary_stats.h_index;
        }
    } catch (error) {
        console.error('Error fetching OpenAlex metrics:', error);
        // Keep fallback values shown in HTML
    }
}

/**
 * Load publications from local JSON file (exported from Bibsonomy)
 */
async function loadBibsonomyPublications(container) {
    // Show loading state
    container.innerHTML = '<p class="text-muted">Loading publications...</p>';

    try {
        const response = await fetch('data/publications.json');
        if (!response.ok) throw new Error('Failed to load publications');
        const data = await response.json();
        renderBibsonomyPublications(container, data);
    } catch (error) {
        console.error('Error loading publications:', error);
        container.innerHTML = `
            <p class="text-muted">
                Unable to load publications.
                Please visit <a href="https://www.bibsonomy.org/user/${BIBSONOMY_CONFIG.username}" target="_blank">my Bibsonomy profile</a>
                or <a href="https://scholar.google.com/citations?user=5Iy85HsAAAAJ" target="_blank">Google Scholar</a> for a complete list.
            </p>
        `;
    }
}

/**
 * Format authors array into a string
 */
function formatAuthors(authors) {
    if (!authors || !Array.isArray(authors)) return '';
    return authors.map(a => {
        if (typeof a === 'string') return a;
        return `${a.first || ''} ${a.last || ''}`.trim();
    }).join(', ');
}

/**
 * Render Bibsonomy publications to the page
 * JSONP format uses: label (title), authors (array), pub-type, year, journal, booktitle, doi, url
 */
function renderBibsonomyPublications(container, data) {
    // JSONP format returns items array
    let items = [];

    if (data.items && Array.isArray(data.items)) {
        // Filter to only Publication type items
        items = data.items.filter(item => item.type === 'Publication');
    }

    if (items.length === 0) {
        container.innerHTML = '<p class="text-muted">No publications found.</p>';
        return;
    }

    // Group by year
    const publicationsByYear = {};
    items.forEach(item => {
        const year = item.year || 'Unknown';
        if (!publicationsByYear[year]) {
            publicationsByYear[year] = [];
        }
        publicationsByYear[year].push(item);
    });

    // Sort years descending
    const sortedYears = Object.keys(publicationsByYear).sort((a, b) => b - a);

    let html = '';
    sortedYears.forEach(year => {
        html += `<h2 class="section-title mt-2">${year}</h2>`;
        html += '<div class="publication-list">';

        publicationsByYear[year].forEach(item => {
            // JSONP field names
            const title = item.label || 'Untitled';
            const author = formatAuthors(item.authors);
            const entrytype = item['pub-type'] || 'misc';
            const itemYear = item.year || '';
            const url = item.url || '';
            const doi = item.doi || '';
            const venue = item.journal || item.booktitle || '';
            const scholarSearch = `https://scholar.google.com/scholar?q=${encodeURIComponent(title)}`;

            const type = getPublicationType(entrytype);

            html += `
                <div class="publication-item" data-type="${type}">
                    <span class="publication-year">${escapeHtml(String(itemYear))}</span>
                    <h4 class="publication-title"><a href="${scholarSearch}" target="_blank">${escapeHtml(title)}</a></h4>
                    <p class="publication-authors">${escapeHtml(author)}</p>
                    <p class="publication-venue">${escapeHtml(venue)}</p>
                </div>
            `;
        });

        html += '</div>';
    });

    container.innerHTML = html;

    // Re-initialize filters after dynamic content load
    initPublicationFilters();
}

/**
 * Map BibTeX entry types to our filter categories
 */
function getPublicationType(entrytype) {
    const typeMap = {
        'article': 'journal',
        'inproceedings': 'conference',
        'conference': 'conference',
        'incollection': 'chapter',
        'inbook': 'chapter',
        'book': 'chapter',
        'phdthesis': 'thesis',
        'mastersthesis': 'thesis',
        'techreport': 'other',
        'misc': 'other'
    };
    return typeMap[entrytype?.toLowerCase()] || 'other';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Smooth scroll for anchor links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
