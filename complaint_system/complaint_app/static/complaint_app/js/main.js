// Auto-dismiss alerts
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.transition = 'opacity 0.5s';
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 500);
  }, 4000);
});

// Notification badge
async function updateNotifBadge() {
  try {
    const res = await fetch('/api/unread-count/');
    if (!res.ok) return;
    const data = await res.json();
    const badge = document.getElementById('notif-badge');
    if (badge) badge.classList.toggle('visible', data.count > 0);
  } catch (e) {}
}
updateNotifBadge();
setInterval(updateNotifBadge, 30000);

// Active nav highlight
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
  if (link.getAttribute('href') === currentPath) {
    link.style.color = 'var(--text)';
    link.style.background = 'var(--surface2)';
  }
});
