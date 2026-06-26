// marca el link activo en el sidebar segun la pagina actual
document.addEventListener('DOMContentLoaded', function() {
    var path = window.location.pathname.split('/').pop();
    var links = document.querySelectorAll('.sidebar .nav-link');
    links.forEach(function(link) {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        }
    });
});
