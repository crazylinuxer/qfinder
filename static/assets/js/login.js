
const form = document.querySelector('.loginMain form');
params = Server.grabParamsFromURL();



form.addEventListener('submit', e => {
    e.preventDefault();

    const data = [
        e.target.email.value,
        e.target.password.value
    ];

    // document.cookie = '';

    Server.login(...data, true).then(status => {
        if (status >= 200 && status < 300) {
            Popup.open('Autorization', 'You are have been succesfully logged in!', status, `${params.redirect_url ? params.redirect_url : '../'}`);
            sessionStorage.setItem('logged', 'true');
            Server.getUserInfo();
        } else {
            Popup.open('Autorization', 'Smth went wrong', status, '../login/index.html')
        }
    })
})

