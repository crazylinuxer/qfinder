

const renderCatalogItems  = async () => {
    const parent = document.querySelector('.catalogMain');
    const items = await Server.getProductTypes();
    console.log(items)
    items.forEach(item => {
        parent.innerHTML += `
        <a class="catalogMain__item" href="${Server.baseURL}templates/category/index.html?id=${item.id}&name=${item.name}">
            <img src="${item.picture}" alt="${item.name}">
            <p>${item.name}</p>
        </a>
        `
    });
}

renderCatalogItems();