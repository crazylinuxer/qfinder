
const { id } = Server.grabParamsFromURL();

const renderThumbs = thumbs => {
    let pattern = ``;

    thumbs.forEach((thumb, index) => {
        if (index === 0) {
            pattern += `<div class="thumb active" data-img="${thumb.link}"><img src="${thumb.link}" alt=""></div>`
        } else {
            pattern += `<div class="thumb" data-img="${thumb.link}"><img src="${thumb.link}" alt=""></div>`
        }
    });

    return pattern;
}

const renderSlider = (parent, data) => {
    let pattern = `
                    <div class="itemMain__slider-thumbs">
                        ${renderThumbs(data.pictures)}
                    </div>
                    <div class="itemMain__slider-current">
                        <img src="../../static/assets/images/ryzen_box.png" alt="">

                        <div class="q">
                            ${renderStars(data.stars_avg)}

                            <span class="average">${data.stars_avg.toFixed(1)}</span>
                        </div>
                    </div>
    `;

    parent.innerHTML = pattern;
}

const initSlider = () => {
    const thumbs = document.querySelector('.itemMain__slider-thumbs');
    const sliderImage = document.querySelector('.itemMain__slider-current > img');

    thumbs.addEventListener('click', e => {
        const thumb = e.target.closest('div.thumb');
        const btns = thumbs.querySelectorAll('.thumb');

        btns.forEach(btn => btn.classList.remove('active'));
        thumb.classList.add('active');

        sliderImage.setAttribute('src', thumb.getAttribute('data-img'))
    })
}

const renderDescription = (parent, data) => {
    
    console.log(data);

    parent.innerHTML = `
    <p>${data.description}</p>
    
    <div class="itemMain__btns">
        <a href="#" class="addToCart">
            <div>
                <p>Add to cart</p>
                <div>
                    <p class="price">$${data.price}</p>
                    <img src="../../static/assets/images/cart.png" alt="">
                </div>
            </div>
        </a>
        <a href="#" class="addToWishList">
            <div>
                <p>Add to wishlist</p>
                <div>
                    <img src="../../static/assets/images/heart.png" alt="">
                </div>
            </div>
        </a>
    `
}

const renderCharacteristics = (parent, data) => {
    for (const key in data.characteristics) {
        if (Object.hasOwnProperty.call(data.characteristics, key)) {
            parent.innerHTML += `
            <div class="table__row">
                <div>${key}</div>
                <div>${data.characteristics[key]}</div>
            </div>
            `
        }
    }

    const copy = document.querySelector('.itemMain__left-char');
    copy.innerHTML = parent.innerHTML;
}

const renderComments = (parent, data) => {
    console.log(parent, data)

    data.feedback.forEach(comment => {
        parent.innerHTML += `
        <div class="itemMain__comment" data-user-id="${comment.id}">
            <div class="itemMain__comment-info">
                <img src="../../static/assets/images/account.png" alt="">
                <p>${comment.user_name}</p>
                ${renderStars(+comment.stars)}
            </div>
            <p>${comment.body}</p>
        </div>
        `
    })
}

document.addEventListener('DOMContentLoaded', async () => {
    const product = await Server.getProductInfo(id);
    const slider = document.querySelector('.itemMain__slider');
    const description = document.querySelector('.itemMain__descirption');
    const characteristics = document.querySelector('.itemMain__charecteristics .table');
    const productName = document.querySelector('.catalogHeader__location p');
    const comments = document.querySelector('.itemMain__left-comments');
    

    renderSlider(slider, product);
    initSlider();
    renderDescription(description, product);
    renderCharacteristics(characteristics, product);
    renderComments(comments, product)


    productName.textContent = product.name;
    console.log(product);

    const leaveComment = document.querySelector('.itemMain__leaveComment');


    comments.addEventListener('click', (e) => {
        if (e.target.classList.contains('itemMain__leaveCommentBtn')) {
            leaveComment.classList.add('active');
            
            
            if (isLogged()) {
                e.preventDefault();
                console.log(isLogged())
            }
            

            const form = document.querySelector('.itemMain__leaveComment');

            form.addEventListener('submit', async e => {
                e.preventDefault();

                const data = {
                    body: e.target.body.value,
                    stars: +e.target.stars.value,
                    id: sessionStorage.getItem('id'),
                    product_id: product.id
                }

                leaveComment.classList.remove('active');
                const res = await Server.sendProductFeedback(data)
                console.log(res);
            })
        } 
    })
});

window.addEventListener('resize', () => {
    console.log('32');
    console.log()
    
})


   