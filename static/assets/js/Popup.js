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

        if (ref === 'null') {
            btn.addEventListener('click', e => {
                e.preventDefault()
                
                const pop = document.querySelector('.popup');

                pop.remove();
            });
            
        }

        document.body.appendChild(div);

        const pop = document.querySelector('.popup');
        pop.style.top = `calc(50% - ${pop.clientHeight}px / 2)`;
    }
}