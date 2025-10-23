console.log("JS loaded");

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM ready, JS running');

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
            console.log(`#loading in view, loading page ${page}...`);
            loading = true;
            loadingIndicator.style.display = 'block';

            fetch(`?page=${page}`, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(response => response.text())
                .then(html => {
                    if (html.trim() === '') {
                        console.log('No HTML returned, reached end of posts');
                        hasMore = false;
                        endMessage.style.display = 'block';
                    } else {
                        console.log(`Appending ${html.trim().length} characters of HTML`);
                        feed.insertAdjacentHTML('beforeend', html);
                        page += 1;
                        console.log(`Next page will be ${page}`);
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
