(function() {
    'use strict';

    var loaded = false;
    var loading = false;
    var pendingOpen = false;

    function buildTOC() {
        if (document.querySelector('.toc')) return;
        var article = document.querySelector('article.guide, article.guide-content');
        if (!article) return;
        var header = article.querySelector('.guide-header');
        if (!header) return;

        var contentRoot = article.querySelector('.guide-content') || article;
        var headings = Array.prototype.slice.call(contentRoot.querySelectorAll('h2, h3'))
            .filter(function(heading) {
                return !heading.closest('.faq-section') && !heading.closest('.related-guides');
            });

        if (headings.length < 3) {
            var emptyPlaceholder = header.parentElement && header.parentElement.querySelector('.toc-placeholder');
            if (emptyPlaceholder) emptyPlaceholder.remove();
            return;
        }

        var usedIds = new Set();
        var items = headings.map(function(heading) {
            var id = heading.getAttribute('id');
            if (!id) {
                id = heading.textContent.trim().toLowerCase()
                    .replace(/[^a-z0-9\\s-]/g, '')
                    .replace(/\\s+/g, '-')
                    .replace(/-+/g, '-')
                    .replace(/^-|-$/g, '');
            }
            var uniqueId = id || 'section';
            var counter = 2;
            while (usedIds.has(uniqueId)) {
                uniqueId = id + '-' + counter;
                counter += 1;
            }
            usedIds.add(uniqueId);
            heading.setAttribute('id', uniqueId);
            return { id: uniqueId, text: heading.textContent.trim(), level: heading.tagName.toLowerCase() };
        });

        if (!items.length) {
            var placeholder = header.parentElement && header.parentElement.querySelector('.toc-placeholder');
            if (placeholder) placeholder.remove();
            return;
        }

        var toc = document.createElement('nav');
        toc.className = 'toc';
        toc.setAttribute('aria-label', 'On this page');

        var title = document.createElement('div');
        title.className = 'toc-title';
        title.textContent = 'On this page';
        toc.appendChild(title);

        var list = document.createElement('ul');
        list.className = 'toc-list';

        items.forEach(function(item) {
            var li = document.createElement('li');
            li.className = item.level === 'h3' ? 'toc-item toc-item--nested' : 'toc-item';
            var link = document.createElement('a');
            link.href = '#' + item.id;
            link.textContent = item.text;
            li.appendChild(link);
            list.appendChild(li);
        });

        toc.appendChild(list);
        var container = header.parentElement && header.parentElement.querySelector('.toc-placeholder');
        if (container) {
            container.classList.add('toc-placeholder--filled');
            container.appendChild(toc);
        } else {
            header.insertAdjacentElement('afterend', toc);
        }
    }

    function loadSearch() {
        if (loaded || loading) return;
        loading = true;
        var script = document.createElement('script');
        script.src = 'search.js';
        script.defer = true;
        script.onload = function() {
            loaded = true;
            loading = false;
            if (pendingOpen) {
                var openNow = function() {
                    var trigger = document.querySelector('.search-trigger');
                    if (trigger) trigger.click();
                };
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', openNow, { once: true });
                } else {
                    openNow();
                }
            }
        };
        script.onerror = function() {
            loading = false;
        };
        document.head.appendChild(script);
    }

    function requestOpen() {
        pendingOpen = true;
        window.__openSearchOnLoad = true;
        loadSearch();
    }

    document.addEventListener('click', function(e) {
        var trigger = e.target.closest && e.target.closest('.search-trigger');
        if (!trigger) return;
        if (!loaded) {
            e.preventDefault();
            requestOpen();
        }
    }, true);

    document.addEventListener('keydown', function(e) {
        var isCmdK = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
        var isSlash = e.key === '/' && !(document.activeElement && /input|textarea/i.test(document.activeElement.tagName));
        if (!isCmdK && !isSlash) return;
        if (!loaded) {
            e.preventDefault();
            requestOpen();
        }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildTOC);
    } else {
        buildTOC();
    }
})();
