const renderItems = (parent, data) => {
    data.forEach(item => {
        parent.innerHTML += `
        <div class="wishMain__item">
            <a href="${Server.baseURL + 'templates/item/index.html?id=' + item.id}" class="wishMain__item-link">
                <img src="${item.picture}" alt="${item.name}">
                <h2>${item.name}</h2>
            </a>
        
            <div class="itemMain__btns">
                <a href="#" data-id="${item.id}">
                    <div>
                        <div>
                            <p class="price">$${item.price}</p>
                            <img src="../../static/assets/images/cart.png" alt="">
                        </div>
                    </div>
                </a>
            </div>

            <div class="del" data-id="${item.id}"></div>
        </div>
        `
    });
}

if (isLogged()) {
    document.addEventListener('DOMContentLoaded', async () => {
        const wishlist = await Server.getWishList();
        const parent = document.querySelector('.wishMain .wrapper');
        renderItems(parent, wishlist)
        console.log(wishlist);

        const addToCartBtn = document.querySelectorAll('.itemMain__btns a');

        addToCartBtn.forEach(btn => {
            btn.addEventListener('click', async function(e) {
                e.preventDefault();

                const id = this.getAttribute('data-id')
        
                Server.addProductToCart(id).then(response => {
                    if (response.status === 201) {
                        Popup.open('Добавление товара в корзину', 'Товар успешно добавлен!', response.status, 'null')
                    } else if (response.status === 409) {
                        console.log('409')
                        Popup.open('Добавление товара в корзину', 'Ошибка. Товар уже есть в корзине.', response.status, 'null')
                    } else {
                        Popup.open('Добавление товара в корзину', 'Что-то пошло не так...', response.status, 'null')
                    }
                })
            })
        })

        const dels = document.querySelectorAll('.del');

        dels.forEach(delBtn => {
            delBtn.addEventListener('click', async function() {
                const id = this.getAttribute('data-id');

                const res = await Server.removeItemFromWishList(id);

                if (res === 200) {
                    this.parentNode.remove()
                }
            })
        })


    })
} else {
    window.location.replace(`${Server.baseURL}/login`)
}


