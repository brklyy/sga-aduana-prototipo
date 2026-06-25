function toggleModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.toggle('show');
}

document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname.split('/').pop();
  document.querySelectorAll('.sidebar a').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });
});
