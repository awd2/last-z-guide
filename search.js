/**
 * Command Palette Search
 * Keyboard-first search experience with fuzzy matching
 */

(function() {
    'use strict';

    // State
    let fuse = null;
    let searchIndex = [];
    let selectedIndex = 0;
    let results = [];
    let isOpen = false;

    // DOM Elements (will be created)
    let overlay, modal, input, resultsContainer;

    // Fuse.js options for fuzzy search
    const fuseOptions = {
        keys: [
            { name: 'title', weight: 0.4 },
            { name: 'description', weight: 0.3 },
            { name: 'keywords', weight: 0.2 },
            { name: 'category', weight: 0.1 }
        ],
        threshold: 0.4,
        distance: 100,
        includeMatches: true,
        minMatchCharLength: 2
    };

    // Icons
    const icons = {
        search: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>`,
        document: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>`,
        empty: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>`
    };

    /**
     * Initialize search functionality
     */
    async function init() {
        try {
            // Load Fuse.js from CDN
            await loadFuseJS();

            // Load search index
            await loadSearchIndex();

            // Create DOM elements
            createSearchUI();

            // Bind events
            bindEvents();

            console.log('Search initialized successfully');
        } catch (error) {
            console.error('Failed to initialize search:', error);
        }
    }

    /**
     * Load Fuse.js library from CDN
     */
    function loadFuseJS() {
        return new Promise((resolve, reject) => {
            if (window.Fuse) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    /**
     * Load search index JSON
     */
    async function loadSearchIndex() {
        // Use relative path for both local file:// and production
        const basePath = window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/') + 1);
        const response = await fetch(basePath + 'search-index.json');
        searchIndex = await response.json();
        fuse = new Fuse(searchIndex, fuseOptions);
    }

    /**
     * Create search UI elements
     */
    function createSearchUI() {
        // Create overlay
        overlay = document.createElement('div');
        overlay.className = 'search-overlay';
        overlay.innerHTML = '';

        // Create modal
        modal = document.createElement('div');
        modal.className = 'search-modal';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-label', 'Search guides');

        modal.innerHTML = `
            <div class="search-input-wrapper">
                ${icons.search}
                <input
                    type="text"
                    class="search-input"
                    placeholder="Search guides..."
                    autocomplete="off"
                    aria-label="Search"
                >
                <div class="search-shortcut">
                    <kbd>esc</kbd>
                </div>
            </div>
            <div class="search-results" role="listbox"></div>
            <div class="search-footer">
                <span class="search-hint"><kbd>↑</kbd><kbd>↓</kbd> navigate</span>
                <span class="search-hint"><kbd>↵</kbd> select</span>
                <span class="search-hint"><kbd>esc</kbd> close</span>
            </div>
        `;

        // Add to DOM
        document.body.appendChild(overlay);
        document.body.appendChild(modal);

        // Get references
        input = modal.querySelector('.search-input');
        resultsContainer = modal.querySelector('.search-results');

        // Show initial state
        showEmptyState();
    }

    /**
     * Bind event listeners
     */
    function bindEvents() {
        // Keyboard shortcut to open (Cmd/Ctrl + K)
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                openSearch();
            }

            // Also open with / key when not in input
            if (e.key === '/' && !isInputFocused()) {
                e.preventDefault();
                openSearch();
            }
        });

        // Close on overlay click
        overlay.addEventListener('click', closeSearch);

        // Close on Escape
        modal.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                e.preventDefault();
                closeSearch();
            }
        });

        // Input handling
        input.addEventListener('input', handleInput);
        input.addEventListener('keydown', handleKeyNavigation);

        // Search trigger buttons
        document.querySelectorAll('.search-trigger').forEach(btn => {
            btn.addEventListener('click', openSearch);
        });
    }

    /**
     * Check if user is typing in an input field
     */
    function isInputFocused() {
        const active = document.activeElement;
        return active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.isContentEditable);
    }

    /**
     * Open search modal
     */
    function openSearch() {
        isOpen = true;
        overlay.classList.add('active');
        modal.classList.add('active');
        input.value = '';
        input.focus();
        selectedIndex = 0;
        showEmptyState();
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close search modal
     */
    function closeSearch() {
        isOpen = false;
        overlay.classList.remove('active');
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    /**
     * Handle input changes
     */
    function handleInput(e) {
        const query = e.target.value.trim();

        if (!query) {
            showEmptyState();
            return;
        }

        // Perform search
        results = fuse.search(query, { limit: 8 });
        selectedIndex = 0;

        if (results.length === 0) {
            showNoResults(query);
        } else {
            renderResults();
        }
    }

    /**
     * Handle keyboard navigation
     */
    function handleKeyNavigation(e) {
        if (results.length === 0) return;

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, results.length - 1);
                updateSelection();
                break;

            case 'ArrowUp':
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, 0);
                updateSelection();
                break;

            case 'Enter':
                e.preventDefault();
                if (results[selectedIndex]) {
                    navigateToResult(results[selectedIndex].item);
                }
                break;
        }
    }

    /**
     * Show empty state
     */
    function showEmptyState() {
        results = [];
        resultsContainer.innerHTML = `
            <div class="search-empty">
                ${icons.empty}
                <p>Type to search guides...</p>
            </div>
        `;
    }

    /**
     * Show no results message
     */
    function showNoResults(query) {
        resultsContainer.innerHTML = `
            <div class="search-no-results">
                <p>No results for "${escapeHtml(query)}"</p>
            </div>
        `;
    }

    /**
     * Render search results
     */
    function renderResults() {
        resultsContainer.innerHTML = results.map((result, index) => {
            const item = result.item;
            const isSelected = index === selectedIndex;

            // Highlight matches in title and description
            let title = highlightMatches(item.title, result.matches, 'title');
            let description = highlightMatches(item.description, result.matches, 'description');

            return `
                <a href="${item.url}"
                   class="search-result ${isSelected ? 'selected' : ''}"
                   role="option"
                   aria-selected="${isSelected}"
                   data-index="${index}">
                    <div class="search-result-header">
                        <span class="search-result-icon">${icons.document}</span>
                        <span class="search-result-title">${title}</span>
                        <span class="search-result-category">${item.category}</span>
                    </div>
                    <div class="search-result-description">${description}</div>
                </a>
            `;
        }).join('');

        // Add click handlers to results
        resultsContainer.querySelectorAll('.search-result').forEach(el => {
            el.addEventListener('click', (e) => {
                // Let the link navigate naturally
            });

            el.addEventListener('mouseenter', (e) => {
                selectedIndex = parseInt(el.dataset.index);
                updateSelection();
            });
        });
    }

    /**
     * Update selected item visual state
     */
    function updateSelection() {
        resultsContainer.querySelectorAll('.search-result').forEach((el, index) => {
            el.classList.toggle('selected', index === selectedIndex);
            el.setAttribute('aria-selected', index === selectedIndex);
        });

        // Scroll into view if needed
        const selected = resultsContainer.querySelector('.search-result.selected');
        if (selected) {
            selected.scrollIntoView({ block: 'nearest' });
        }
    }

    /**
     * Navigate to selected result
     */
    function navigateToResult(item) {
        closeSearch();
        window.location.href = item.url;
    }

    /**
     * Highlight matched text
     */
    function highlightMatches(text, matches, key) {
        if (!matches) return escapeHtml(text);

        const match = matches.find(m => m.key === key);
        if (!match) return escapeHtml(text);

        // Sort indices in reverse to replace from end
        const indices = match.indices.slice().sort((a, b) => b[0] - a[0]);

        let result = text;
        indices.forEach(([start, end]) => {
            const before = result.slice(0, start);
            const matched = result.slice(start, end + 1);
            const after = result.slice(end + 1);
            result = before + `<mark class="search-highlight">${escapeHtml(matched)}</mark>` + after;
        });

        return result;
    }

    /**
     * Escape HTML special characters
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
