/**
 * Academic Website - Main JavaScript
 * Includes mobile navigation, publication filtering, and Bibsonomy integration
 */

document.addEventListener('DOMContentLoaded', function() {
    initMobileNav();
    initPublicationFilters();
    initBibsonomy();
    setActiveNavLink();
});

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

// Configuration - UPDATE THESE VALUES
const BIBSONOMY_CONFIG = {
    username: 'cflath',  // Your Bibsonomy username
    apiKey: '6aecc79a36444ef0edaab8ff5f2bfbac',
    baseUrl: 'https://www.bibsonomy.org/api',
    resourceType: 'bibtex'  // or 'bookmark'
};

/**
 * Initialize Bibsonomy integration if on publications page
 */
function initBibsonomy() {
    const loadButton = document.getElementById('load-bibsonomy');
    const pubContainer = document.getElementById('bibsonomy-publications');
    const staticContent = document.querySelectorAll('.publication-list, h2.section-title.mt-2');
    const staticFooter = document.getElementById('static-footer');

    if (loadButton && pubContainer) {
        loadButton.addEventListener('click', async function() {
            // Hide static content
            staticContent.forEach(el => el.style.display = 'none');
            if (staticFooter) staticFooter.style.display = 'none';

            // Show and load dynamic content
            pubContainer.style.display = 'block';
            loadButton.textContent = 'Loading...';
            loadButton.disabled = true;

            await loadBibsonomyPublications(pubContainer);

            loadButton.textContent = '✓ Loaded from Bibsonomy';
        });
    }
}

/**
 * Fetch publications from Bibsonomy API using JSONP (to bypass CORS)
 */
async function loadBibsonomyPublications(container) {
    const { username, resourceType } = BIBSONOMY_CONFIG;

    // Show loading state
    container.innerHTML = '<p class="text-muted">Loading publications from Bibsonomy...</p>';

    try {
        // Use JSONP to bypass CORS restrictions
        const callbackName = 'bibsonomyCallback_' + Date.now();
        const url = `https://www.bibsonomy.org/json/user/${username}?callback=${callbackName}`;

        const data = await new Promise((resolve, reject) => {
            // Set timeout for the request
            const timeout = setTimeout(() => {
                cleanup();
                reject(new Error('Request timed out'));
            }, 10000);

            // Create callback function
            window[callbackName] = function(response) {
                cleanup();
                resolve(response);
            };

            // Cleanup function
            function cleanup() {
                clearTimeout(timeout);
                delete window[callbackName];
                if (script.parentNode) {
                    script.parentNode.removeChild(script);
                }
            }

            // Create and inject script tag
            const script = document.createElement('script');
            script.src = url;
            script.onerror = function() {
                cleanup();
                reject(new Error('Failed to load script'));
            };
            document.head.appendChild(script);
        });

        renderBibsonomyPublications(container, data);
    } catch (error) {
        console.error('Error fetching from Bibsonomy:', error);
        container.innerHTML = `
            <p class="text-muted">
                Unable to load publications dynamically.
                Please visit <a href="https://www.bibsonomy.org/user/${BIBSONOMY_CONFIG.username}" target="_blank">my Bibsonomy profile</a>
                or <a href="https://scholar.google.com/citations?user=5Iy85HsAAAAJ" target="_blank">Google Scholar</a> for a complete list.
            </p>
        `;
    }
}

/**
 * Render Bibsonomy publications to the page
 * Handles both JSONP format (items array) and API format (posts.post array)
 */
function renderBibsonomyPublications(container, data) {
    // Handle JSONP format (items array) or API format (posts.post array)
    let items = [];

    if (data.items && Array.isArray(data.items)) {
        // JSONP format
        items = data.items;
    } else if (data.posts && data.posts.post) {
        // API format
        items = Array.isArray(data.posts.post) ? data.posts.post : [data.posts.post];
    }

    if (items.length === 0) {
        container.innerHTML = '<p class="text-muted">No publications found.</p>';
        return;
    }

    // Group by year
    const publicationsByYear = {};
    items.forEach(item => {
        // JSONP format has different structure
        const year = item.year || (item.bibtex && item.bibtex.year) || 'Unknown';
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
            // Handle both JSONP and API formats
            const title = item.title || (item.bibtex && item.bibtex.title) || 'Untitled';
            const author = item.author || (item.bibtex && item.bibtex.author) || '';
            const entrytype = item.entrytype || (item.bibtex && item.bibtex.entrytype) || 'misc';
            const itemYear = item.year || (item.bibtex && item.bibtex.year) || '';
            const url = item.url || (item.bibtex && item.bibtex.url) || '';
            const doi = item.doi || (item.bibtex && item.bibtex.doi) || '';
            const venue = item.journal || item.booktitle || item.publisher ||
                         (item.bibtex && (item.bibtex.journal || item.bibtex.booktitle || item.bibtex.publisher)) || '';
            const bibtexKey = item.bibtexKey || item.id || '';

            const type = getPublicationType(entrytype);

            html += `
                <div class="publication-item" data-type="${type}">
                    <span class="publication-year">${escapeHtml(String(itemYear))}</span>
                    <h4 class="publication-title">${escapeHtml(title)}</h4>
                    <p class="publication-authors">${escapeHtml(author)}</p>
                    <p class="publication-venue">${escapeHtml(venue)}</p>
                    <div class="publication-links">
                        ${url ? `<a href="${escapeHtml(url)}" class="pub-link" target="_blank">Link</a>` : ''}
                        ${doi ? `<a href="https://doi.org/${escapeHtml(doi)}" class="pub-link" target="_blank">DOI</a>` : ''}
                        ${bibtexKey ? `<a href="https://www.bibsonomy.org/bibtex/${escapeHtml(bibtexKey)}/${BIBSONOMY_CONFIG.username}" class="pub-link" target="_blank">BibTeX</a>` : ''}
                    </div>
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
