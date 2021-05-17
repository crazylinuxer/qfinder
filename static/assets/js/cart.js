
const renderCartItems = (cartList, parent) => {
    console.log(cartList.content.length);
    

    if (cartList.content.length === 0) {
        parent.innerHTML += '<h3>You don\'t have any items in cart :(</h3>'
    } else {
        cartList.content.forEach(cartItem => {
            parent.innerHTML += `
                <div class="cartMain__item">
                    <a href="#" class="cartMain__item-img">
                        <img src="${cartItem.picture}" alt="${cartItem.name}">
                    </a>
    
                    <div class="cartMain__item-right">
                        <div>
                            <a href="#">
                                <h2>${cartItem.name}</h2>
                            </a>
                            <p class="cartMain__item-price">$${cartItem.price}</p>
                        </div>
    
                        <div>
                            <a href="#" class="addToWishList" data-id="${cartItem.id}">
                                <img src="../../static/assets/images/heart.png" alt="">
                                <span>Add to wishlist</span>
                            </a>
                            <a href="#" class="removeFromCart" data-remove="${cartItem.id}">
                                <img src="../../static/assets/images/X.png" alt="">
                                <span>Remove from cart</span>
                            </a>
                        </div>
                    </div>
                 </div>
            `;
    
            
        })
    }

    parent.innerHTML += `
    <div class="cartMain__total">
        <p>Total: </p>
        <a href="#">
            <span>$${cartList.total_price}</span>
            <span>Buy</span>
        </a>
    </div>
    `
}

if (isLogged()) {
    document.addEventListener('DOMContentLoaded', async () => {
        const response = await Server.getCartList();
        const wrapper = document.querySelector('.cartMain .wrapper');

        renderCartItems(response, wrapper);

        const cartMain = document.querySelectorAll('.removeFromCart');
        const addToWidhListBtn = document.querySelectorAll('.addToWishList');

        cartMain.forEach(item => {
            item.addEventListener('click', async function(e) {
                e.preventDefault();

                const id = this.getAttribute('data-remove')

                const res = await Server.RemoveProductFromCart(id);

                if (res === 200) {
                    wrapper.innerHTML = '';
                }

                const response = await Server.getCartList();
                renderCartItems(response, wrapper);
            })
        })

        addToWidhListBtn.forEach(el => {
            el.addEventListener('click', async function(e) {
                e.preventDefault();

                const id = this.getAttribute('data-id');

                Server.addProductToWishList(id).then(response => {
                    if (response.status === 201) {
                        Popup.open('Добавление товара в список желаний', 'Товар успешно добавлен!', response.status, 'null')
                    } else if (response.status === 409) {
                        console.log('409')
                        Popup.open('Добавление товара в список желаний', 'Ошибка. Товар уже есть в списке.', response.status, 'null')
                    } else {
                        Popup.open('Добавление товара в список желаний', 'Что-то пошло не так...', response.status, 'null')
                    }
                })
            })
        })


        console.log(cartMain);
    })
} else {
    window.location.replace(`${Server.baseURL}/login/index.html`)
}
