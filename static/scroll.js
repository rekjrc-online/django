document.addEventListener('DOMContentLoaded', () => {
    let page = 2;  // first page is already loaded
    let loading = false;
    let hasMore = true;
    const feed = document.getElementById('feed');
    const loadingIndicator = document.getElementById('loading');
    const endMessage = document.getElementById('end-message');
    // Intersection Observer
    const observer = new IntersectionObserver(entries => {
        const entry = entries[0];
        if (entry.isIntersecting && !loading && hasMore) {
            loading = true;
            loadingIndicator.style.display = 'block';
            fetch(`?page=${page}`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(response => response.text())
                .then(html => {
                    if (html.trim() === '') {
                        hasMore = false;
                        endMessage.style.display = 'block';
                    } else {
                        feed.insertAdjacentHTML('beforeend', html);
                        page += 1;
                    }
                })
                .catch(err => console.error('Error fetching posts:', err))
                .finally(() => {
                    loading = false;
                    loadingIndicator.style.display = hasMore ? 'block' : 'none';
                });
        }
    }, {
        root: null, // viewport
        rootMargin: '0px',
        threshold: 0.1  // triggers when 10% of #loading is visible
    });
    observer.observe(loadingIndicator);
});
