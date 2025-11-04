console.log("scroll.js top");
document.addEventListener('DOMContentLoaded', () => {
    console.log("listener top");
    let page = 2;
    let loading = false;
    let hasMore = true;
    const feed = document.getElementById('feed');
    const loadingIndicator = document.getElementById('loading');
    const endMessage = document.getElementById('end-message');
    console.log("listener 1");
    if (!feed) console.error('Feed container not found!');
    if (!loadingIndicator) console.error('Loading indicator not found!');
    if (!endMessage) console.error('End message not found!');
    // Intersection Observer
    const observer = new IntersectionObserver(entries => {
        console.log("observer top");
        const entry = entries[0];
        if (entry.isIntersecting && !loading && hasMore) {
            console.log("listener 2");
            loading = true;
            loadingIndicator.style.display = 'block';
            console.log("listener 3");
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
            console.log("listener 4");
        }
        console.log("observer bottom");
    }, {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    });
    observer.observe(loadingIndicator);
    console.log("listener bottom");
});
console.log("scroll.js bottom");
