// Example interactivity for dashboard
document.addEventListener('DOMContentLoaded', () => {
    // Toggle sidebar active link
    const sidebarLinks = document.querySelectorAll('.sidebar-menu li a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', () => {
            sidebarLinks.forEach(l => l.parentElement.classList.remove('active'));
            link.parentElement.classList.add('active');
        });
    });

    // Example: alert on quick card click
    const quickCards = document.querySelectorAll('.quick-card');
    quickCards.forEach(card => {
        card.addEventListener('click', () => {
            alert(`Redirecting to ${card.textContent.trim()}`);
        });
    });
});
