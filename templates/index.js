const isLogged = JSON.parse(sessionStorage.getItem('user')) || null;

if (isLogged) {

    window.addEventListener('DOMContentLoaded', () => {
        const nav = document.querySelector('.header__navigation');
        nav.innerHTML = null;

        const logoutBtn = document.createElement('a');
        logoutBtn.setAttribute('href', './');
        logoutBtn.textContent = 'Logout';

        logoutBtn.addEventListener('click', () => Server.logout());

        nav.appendChild(logoutBtn);
    })


}