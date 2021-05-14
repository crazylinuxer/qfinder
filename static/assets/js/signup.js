
const form = document.querySelector('.loginMain form');

form.addEventListener('submit', e => {
    e.preventDefault();

    const data = [
        e.target.fname.value,
        e.target.lname.value,
        e.target.email.value,
        e.target.pass.value
    ];

    Server.signUp(...data, true).then(status => {
        if (status === 201) {
            Popup.open('Registration', 'You are have been succesfully registered!', status, '../login')
        } else {
            Popup.open('Registration', 'Smth went wrong', status, '../')
        }
    })
})