
const form = document.querySelector('.loginMain form');

form.addEventListener('submit', e => {
    e.preventDefault();

    const data = [
        e.target.email.value,
        e.target.password.value
    ];

    // document.cookie = '';

    Server.login(...data, true).then(status => {
        if (status >= 200 && status < 300) {
            Popup.open('Autorization', 'You are have been succesfully logged in!', status, '../');
            sessionStorage.setItem('logged', 'true');
            Server.getUserInfo();
        } else {
            Popup.open('Autorization', 'Smth went wrong', status, '../login/')
        }
    })
})