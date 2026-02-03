/**
 * Lightweight GA4 event tracking helpers.
 * Uses gtag when available and no-ops otherwise.
 */
(function() {
    'use strict';

    const MEASUREMENT_ID = 'G-PYBSRQ1QFP';
    const tableDepthMarks = new Map();

    function loadGA() {
        if (window.gtag || window.__gaLoading) return;
        window.__gaLoading = true;
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);} 
        window.gtag = gtag;
        gtag('js', new Date());
        gtag('config', MEASUREMENT_ID);

        var script = document.createElement('script');
        script.async = true;
        script.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
        document.head.appendChild(script);
    }

    function scheduleGALoad() {
        if ('requestIdleCallback' in window) {
            requestIdleCallback(loadGA, { timeout: 2000 });
        } else {
            setTimeout(loadGA, 2000);
        }
    }

    function loadGAOnInteraction() {
        loadGA();
        window.removeEventListener('scroll', loadGAOnInteraction, { passive: true });
        window.removeEventListener('pointerdown', loadGAOnInteraction, { passive: true });
        window.removeEventListener('keydown', loadGAOnInteraction);
    }


    function canTrack() {
        return typeof window.gtag === 'function';
    }

    function track(eventName, params) {
        if (!canTrack()) return;
        window.gtag('event', eventName, Object.assign({
            measurement_id: MEASUREMENT_ID
        }, params || {}));
    }

    function getPath() {
        return window.location.pathname.replace(/^\//, '') || 'index.html';
    }

    function slugFromUrl(url) {
        if (!url) return '';
        return url.replace(/^\//, '').replace(/\.html$/, '');
    }

    function attachHomeTracking() {
        const homeNav = document.querySelector('.home-nav');
        if (homeNav) {
            homeNav.addEventListener('click', (e) => {
                const link = e.target.closest('a[href^="#"]');
                if (!link) return;
                const groupId = link.getAttribute('href').slice(1);
                track('nav_group_click', {
                    group_id: groupId,
                    group_label: link.textContent.trim(),
                    page_type: 'home',
                    guide_slug: slugFromUrl(getPath())
                });
            });
        }

        const cards = document.querySelectorAll('.home .card');
        if (cards.length > 0) {
            cards.forEach((card) => {
                card.addEventListener('click', () => {
                    const group = card.closest('.home-group');
                    const sectionId = group ? group.id : 'ungrouped';
                    const titleEl = card.querySelector('h2');
                    track('card_click', {
                        card_url: card.getAttribute('href') || '',
                        card_title: titleEl ? titleEl.textContent.trim() : '',
                        card_section: sectionId,
                        page_type: 'home',
                        guide_slug: slugFromUrl(getPath())
                    });
                });
            });
        }
    }

    function attachGuideTracking() {
        const faqItems = document.querySelectorAll('.faq-item');
        faqItems.forEach((item, index) => {
            const question = item.querySelector('h3');
            if (!question) return;
            question.addEventListener('click', () => {
                track('faq_expand', {
                    faq_question: question.textContent.trim(),
                    faq_index: index + 1,
                    page_type: 'guide',
                    guide_slug: slugFromUrl(getPath())
                });
            });
        });

        const relatedLinks = document.querySelectorAll('.related-grid a, .related-card');
        relatedLinks.forEach((link) => {
            link.addEventListener('click', () => {
                track('related_click', {
                    from_page: slugFromUrl(getPath()),
                    to_page: slugFromUrl(link.getAttribute('href') || ''),
                    to_title: link.textContent.trim(),
                    page_type: 'guide',
                    guide_slug: slugFromUrl(getPath())
                });
            });
        });
    }

    function tableIdFor(el) {
        const explicit = el.getAttribute('data-table-id');
        if (explicit) return explicit;
        const path = getPath();
        if (path.includes('vehicle-modification-cost')) return 'vehicle-cost';
        if (path.includes('hq-construction-cost')) return 'hq-cost';
        return slugFromUrl(path) || 'table';
    }

    function attachTableTracking() {
        const scrollAreas = document.querySelectorAll('.table-scroll');
        scrollAreas.forEach((area) => {
            const tableId = tableIdFor(area);
            let interacted = false;

            function markInteraction(type) {
                if (interacted) return;
                interacted = true;
                track('table_interaction', {
                    table_id: tableId,
                    interaction_type: type,
                    guide_slug: slugFromUrl(getPath()),
                    page_type: 'table'
                });
            }

            area.addEventListener('scroll', () => {
                markInteraction('scroll');
                trackTableDepth(area, tableId);
            }, { passive: true });
            area.addEventListener('wheel', () => markInteraction('wheel'), { passive: true });
            area.addEventListener('touchstart', () => markInteraction('touch'), { passive: true });

            const legend = area.closest('.data-table-card')?.querySelector('.table-legend');
            if (legend && 'IntersectionObserver' in window) {
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach((entry) => {
                        if (entry.isIntersecting) {
                            track('table_legend_view', {
                                table_id: tableId,
                                guide_slug: slugFromUrl(getPath()),
                                page_type: 'table'
                            });
                            observer.disconnect();
                        }
                    });
                }, { rootMargin: '0px 0px -40% 0px' });
                observer.observe(legend);
            }
        });
    }

    function trackTableDepth(area, tableId) {
        const maxScroll = area.scrollHeight - area.clientHeight;
        if (maxScroll <= 0) return;
        const pct = Math.min(100, Math.round((area.scrollTop / maxScroll) * 100));
        const marks = tableDepthMarks.get(area) || new Set();
        [25, 50, 75, 100].forEach((mark) => {
            if (pct >= mark && !marks.has(mark)) {
                marks.add(mark);
                track('table_scroll_depth', {
                    table_id: tableId,
                    depth_pct: mark,
                    guide_slug: slugFromUrl(getPath()),
                    page_type: 'table'
                });
            }
        });
        tableDepthMarks.set(area, marks);
    }

    // Expose a small API for search.js to call.
    window.analytics = window.analytics || {};
    window.analytics.trackEvent = track;
    window.analytics.trackSearch = function(type, payload) {
        track(type, Object.assign({
            guide_slug: slugFromUrl(getPath()),
            page_type: getPath() === 'index.html' ? 'home' : 'guide'
        }, payload || {}));
    };

    function init() {
        scheduleGALoad();
        window.addEventListener(\'scroll\', loadGAOnInteraction, { passive: true });
        window.addEventListener(\'pointerdown\', loadGAOnInteraction, { passive: true });
        window.addEventListener(\'keydown\', loadGAOnInteraction);
        attachHomeTracking();
        attachGuideTracking();
        attachTableTracking();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

