

const cng = document.querySelector('.changed');
const  renderForm = (parent) => {
    parent.innerHTML = `
        <form>
            <div class="f_name">
                <p>First name: </p>
                <div>
                    <p data-name="f_name">Ivan</p>
                </div>
            </div>
            <div class="l_name">
                <p>Last name: </p>
                <div>
                    <p data-name="l_name">Ivanov</p>
                </div>
            </div>
            <div class="email">
                <p>Email: </p>
                <div>
                    <p data-name="email">ivanivanov@mail.com</p>
                </div>
            </div>


            <button>Log out</button>
        </form>
    `;
}
if (isLogged()) {
    window.addEventListener('DOMContentLoaded', () => {

            let user = JSON.parse(sessionStorage.getItem('user'));
        if (isLogged) {
            const wrapper = document.querySelector('.accountMain');

            renderForm(wrapper);

            const firstName = document.querySelector('.f_name div p');
            const lastName = document.querySelector('.l_name div p');
            const email = document.querySelector('.email div p');


            user = JSON.parse(sessionStorage.getItem('user'));

            console.log(user);

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

            input.addEventListener('blur', async (e) => {
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

                    await Server.updateAccoutInfo(data)
                    const user = await Server.getUserInfo();
                    //const user_data = await user.json();
                    console.log(user)
                    //sessionStorage.setItem('user', JSON.stringify(user));

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
} else {
    window.location.replace(`${Server.baseURL}/login/index.html`)
}
