
document.addEventListener('DOMContentLoaded', async () => {
    const pageHeading = document.querySelector('.catalogHeader__location p');
    const pagePicture = document.querySelector('.catalogHeader__location > img');

    const { id: type_id, name } = Server.grabParamsFromURL();
    const items = await Server.getProductTypes();

    const image = items.find(item => item.id === type_id).picture;

    pageHeading.textContent = name;
    pagePicture.setAttribute('src', image);

    const renderItems = async (type_id, options) => {
        const items = await Server.getAllProductsByType(type_id, options);
        const parent = document.querySelector('.categoryMain__items');
        
        parent.innerHTML = null;

        if (items.length > 0) {
            items.forEach(item => {
                parent.innerHTML += `
                <a class="categoryMain__item" href="${Server.baseURL}/templates/item/?id=${item.id}">
                    <img src="${item.picture}" alt="${item.name}">
                    
                    ${renderStars(item.stars_avg)}
                    
                    <div class="categoryMain__item-info">
                        <h2>${item.name}</h2>
                        <span>$${item.price}</span>
                    </div>
                </a>
                `
            })
        } else {
            parent.innerHTML += `Sorry, nothing founded :(`
        }
        

        console.log(items);
    }


    const renderForm = async () => {
        const tags = await Server.getAllTags();
        const parent = document.querySelector('.options');

        tags.forEach(tag => {
            parent.innerHTML += `
                <input type="checkbox" id="${tag.id}">
                <label for="${tag.id}">${tag.title}</label>
            `
        })
    }

    const renderStat = async (id = type_id) => {
        const stat = await Server.getCategoryStat(id);

        const priceMin = document.querySelector('input[name=price_min]');
        const priceMax = document.querySelector('input[name=price_max]');

        const starsMin = document.querySelector('input[name=stars_min]');
        const starsMax = document.querySelector('input[name=stars_max]');

        starsMin.disabled = true;
        starsMax.disabled = true;
        priceMin.disabled = true;
        priceMax.disabled = true;

        if (stat.min_stars && stat.max_stars) {
            starsMin.value = stat.min_stars;
            starsMax.value = stat.max_stars;

            starsMin.disabled = false;
            starsMax.disabled = false;

            starsMin.setAttribute('min', stat.min_stars);
            starsMax.setAttribute('max', stat.max_stars);
        }

        if (stat.min_price && stat.max_price) {
            priceMin.value = stat.min_price;
            priceMax.value = stat.max_price;

            priceMin.disabled = false;
            priceMax.disabled = false;
        }

        
       

        console.log(stat);
    }

    renderForm();
    renderItems(type_id);
    renderStat(type_id);

    const form = document.querySelector('.categoryMain__options');

    form.addEventListener('change', e => {
        console.log(e.target);
        const parent = document.querySelector('.categoryMain__items');

        const priceMin = document.querySelector('input[name=price_min]');
        const priceMax = document.querySelector('input[name=price_max]');

        const starsMin = document.querySelector('input[name=stars_min]');
        const starsMax = document.querySelector('input[name=stars_max]');

        parent.innerHTML = `<img src="../../static/assets/images/spinner.gif" class="spin">`;

        const options = {
            tags: [],
            min_price: +priceMin.value,
            max_price: +priceMax.value,
        };

        if (!starsMin.disabled && !starsMax.disabled) {
            options.min_stars = starsMin.value;
            options.max_stars = starsMax.value;
        }

        const tags = document.querySelectorAll('.options input[type=checkbox]:checked');

        tags.forEach(input => options.tags.push(input.getAttribute('id')));

        console.log(options);
        renderItems(type_id, options);
    })
})