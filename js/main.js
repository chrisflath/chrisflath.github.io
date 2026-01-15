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
    username: 'flath',  // Your Bibsonomy username
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
 * Fetch publications from Bibsonomy API
 */
async function loadBibsonomyPublications(container) {
    const { username, apiKey, baseUrl, resourceType } = BIBSONOMY_CONFIG;

    // Show loading state
    container.innerHTML = '<p class="text-muted">Loading publications from Bibsonomy...</p>';

    try {
        // Bibsonomy API endpoint for user's posts
        const url = `${baseUrl}/users/${username}/posts?resourcetype=${resourceType}&format=json`;

        const response = await fetch(url, {
            headers: {
                'Authorization': 'Basic ' + btoa(username + ':' + apiKey),
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
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
 */
function renderBibsonomyPublications(container, data) {
    if (!data.posts || !data.posts.post || data.posts.post.length === 0) {
        container.innerHTML = '<p class="text-muted">No publications found.</p>';
        return;
    }

    const posts = data.posts.post;

    // Group by year
    const publicationsByYear = {};
    posts.forEach(post => {
        const bibtex = post.bibtex;
        const year = bibtex.year || 'Unknown';
        if (!publicationsByYear[year]) {
            publicationsByYear[year] = [];
        }
        publicationsByYear[year].push(post);
    });

    // Sort years descending
    const sortedYears = Object.keys(publicationsByYear).sort((a, b) => b - a);

    let html = '';
    sortedYears.forEach(year => {
        html += `<h2 class="section-title mt-2">${year}</h2>`;
        html += '<div class="publication-list">';

        publicationsByYear[year].forEach(post => {
            const bibtex = post.bibtex;
            const type = getPublicationType(bibtex.entrytype);

            html += `
                <div class="publication-item" data-type="${type}">
                    <span class="publication-year">${bibtex.year || ''}</span>
                    <h4 class="publication-title">${escapeHtml(bibtex.title || 'Untitled')}</h4>
                    <p class="publication-authors">${escapeHtml(bibtex.author || '')}</p>
                    <p class="publication-venue">${escapeHtml(getVenue(bibtex))}</p>
                    <div class="publication-links">
                        ${bibtex.url ? `<a href="${bibtex.url}" class="pub-link" target="_blank">Link</a>` : ''}
                        ${bibtex.doi ? `<a href="https://doi.org/${bibtex.doi}" class="pub-link" target="_blank">DOI</a>` : ''}
                        <a href="https://www.bibsonomy.org/bibtex/${post.postingdate ? post.postingdate.replace(/[^a-zA-Z0-9]/g, '') : ''}" class="pub-link" target="_blank">BibTeX</a>
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
 * Get publication venue (journal, booktitle, etc.)
 */
function getVenue(bibtex) {
    if (bibtex.journal) return bibtex.journal;
    if (bibtex.booktitle) return bibtex.booktitle;
    if (bibtex.publisher) return bibtex.publisher;
    return '';
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
