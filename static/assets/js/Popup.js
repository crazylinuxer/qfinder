class Popup {

    static open(heading, text, status, ref) {
        const div = document.createElement('div');
        div.classList.add('popup');
        const h2 = document.createElement('h2');
        h2.textContent = heading;
        const p = document.createElement('p');
        p.textContent = text;
        const btn = document.createElement('a');
        btn.setAttribute('href', ref);
        btn.textContent = 'Ok'

        status >= 200 && status < 300 ? div.classList.add('success') : div.classList.add('error');

        div.appendChild(h2);
        div.appendChild(p);
        div.appendChild(btn);


        document.body.appendChild(div);
    }
}