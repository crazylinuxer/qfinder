const isLogged = JSON.parse(sessionStorage.getItem('user')) || null;

if (isLogged) {

    window.addEventListener('DOMContentLoaded', () => {
        const nav = document.querySelector('.header__navigation');
        const logoutBtn = document.createElement('a');

        const accountBtn = document.querySelector('.main__navigation nav a:nth-child(2)');

        logoutBtn.setAttribute('href', './');
        accountBtn.setAttribute('href', './account/');
        logoutBtn.textContent = 'Logout';

        logoutBtn.addEventListener('click', () => Server.logout());

        nav.innerHTML = null;
        nav.appendChild(logoutBtn);
        
    })


}