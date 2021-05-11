class Server {
    basePoint = 'http://127.0.0.1:5000/api/v1/';
    

    static async getAllProductTypes() {
        // console.log('hello!');
        const data = await fetch(`http://127.0.0.1:5000/api/v1/products/types`)
        const result = await data.json();

        console.log(result);
    }

    static async getProducts(type_id, tags, min_price, max_price, min_stars, max_stars) {
        console.log('hello!');
        const data = await fetch(`${this.basePoint}/products/by_type?${type_id}`)
        const result = await data.json();

        console.log(result);
    }
}

Server.getAllProductTypes()