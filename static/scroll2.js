console.log("JS loaded 2");

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM ready, JS running 2');
    // your infinite scroll code here
});

const scrollContainer = document.querySelector('.middle-col');
    scrollContainer.addEventListener('scroll', () => {
    console.log("Scroll detected");
});