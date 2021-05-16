const isLogged = JSON.parse(sessionStorage.getItem('user')) || null;

const cng = document.querySelector('.changed');

window.addEventListener('DOMContentLoaded', () => {
    if (isLogged) {
        const firstName = document.querySelector('.f_name div p');
        const lastName = document.querySelector('.l_name div p');
        const email = document.querySelector('.email div p');

        const user = isLogged;

        firstName.textContent = user.first_name;
        lastName.textContent = user.last_name;
        email.textContent = user.email;

        const cv = document.querySelector('.accountMain form');
        cv.addEventListener('submit', e => e.preventDefault());
        cv.addEventListener('click', (e) => {
            if (e.target.getAttribute('data-name')) {
                changeToInput(e);
            }
        })
    }

    function changeToInput(e) {
        const initialText = e.target.textContent;
        e.target.outerHTML = `<input type="text" name="${e.target.getAttribute('data-name')}" value="${e.target.textContent}"/>`;

        const input = document.querySelector(`input[name=${e.target.getAttribute('data-name')}]`);
        input.focus();
        const attribute = e.target.getAttribute('data-name');

        input.addEventListener('blur', (e) => {
            e.target.outerHTML = `<p data-name="${attribute}">${e.target.value}</p>`;

            if (initialText !== input.value) {
                console.log('changed');

                const firstName = document.querySelector('.f_name div p');
                const lastName = document.querySelector('.l_name div p');
                const email = document.querySelector('.email div p');

                const data = {
                    email: email.textContent,
                    first_name: firstName.textContent,
                    last_name: lastName.textContent
                }

                // console.log(data);

                Server.updateAccoutInfo(data)
                Server.getUserInfo();
                cng.classList.add('active');

                setTimeout(() => cng.classList.remove('active'), 1000)
            }
        })
    }

    const logoutBtn = document.querySelector('form button');

    logoutBtn.addEventListener('click', () => {
        Server.logout();
        window.location.replace(`${Server.baseURL}index.html`);
    });
})