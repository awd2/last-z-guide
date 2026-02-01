(function() {
    'use strict';

    var loaded = false;
    var loading = false;
    var pendingOpen = false;

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
                var trigger = document.querySelector('.search-trigger');
                if (trigger) trigger.click();
            }
        };
        script.onerror = function() {
            loading = false;
        };
        document.head.appendChild(script);
    }

    function requestOpen() {
        pendingOpen = true;
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
})();
