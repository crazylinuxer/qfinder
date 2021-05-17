class Server {
    static baseURL = 'http://127.0.0.1:5000/';
    static basePoint = `http://127.0.0.1:5000/api/v1/`;

    static async signUp(f_name, l_name, email, password) {
        const data = await fetch(`http://127.0.0.1:5000/api/v1/user/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                email: email,
                first_name: f_name,
                last_name: l_name,
                password: password
            })
        })

        return data.status;
    }

    static async login(email, password) {
        const data = await fetch(`${this.basePoint}user/auth`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })

        const result = await data.json();

        for (const key in result) {
            if (Object.hasOwnProperty.call(result, key)) {
                const element = result[key];
                sessionStorage.setItem(key, element);
            }
        }

        return data.status
    }

    static async getUserInfo(token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}user`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })

        const result = await data.json();

        sessionStorage.setItem('user', JSON.stringify(result));

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.getUserInfo(token);
        } else {
            return data;
        }
    }

    static async refreshToken(token) {
        const data = await fetch(`${this.basePoint}user/auth/refresh`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })

        const result = await data.json();

        for (const key in result) {
            if (Object.hasOwnProperty.call(result, key)) {
                const element = result[key];
                sessionStorage.setItem(key, element);
            }
        }
    }

    static logout() {
        sessionStorage.setItem('user', null);
        sessionStorage.removeItem('refresh_token');
        sessionStorage.removeItem('access_token');
        sessionStorage.removeItem('id');
    }

    static async updateAccoutInfo(userData, token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}user`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.updateAccoutInfo(userData, token);
        } else {
            return data.status
        }
    }

    static async getProductTypes(token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}products/types`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.getProductTypes(token);
        } else {
            return result;
        }
    }

    static async getAllProductsByType(type_id, options, token = sessionStorage.getItem('access_token')) {
     

            let url = `${this.basePoint}products/by_type?type=${type_id}`;
            
            if (options) {
                for (const key in options) {
                    if (Object.hasOwnProperty.call(options, key) && options[key]) {
                        if (key === 'tags' && options[key].length === 0) {
                            null;
                        } else {
                            url += `&${key}=${options[key]}`; 
                        }
                        
                    }
                }
            }
            
            console.log(url)

        const data = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.getAllProductsByType(type_id, options, token);
        } else {
            return result;
        }
    }

    static async getAllTags(token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}products/tags`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.getAllTags(token);
        } else {
            return result;
        }
    }

    static async getCategoryStat(id, token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}products/type_stat?type=${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.getCategoryStat(id, token);
        } else {
            return result;
        }
    }

    static async getProductInfo(product_id, token = sessionStorage.getItem('access_token')) {
        
        const auth = token ? {'Authorization': `Bearer ${token}`} : {};

        if (token) {
            const data = await fetch(`${this.basePoint}products/info?product=${product_id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
            });

            const result = await data.json();
            console.log(result);
            if (data.status === 401) {
                Server.refreshToken(sessionStorage.getItem('refresh_token'))
                Server.getProductInfo(product_id, token);
            } else {
                return result;
            }

    } else {
        const data = await fetch(`${this.basePoint}products/info?product=${product_id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const result = await data.json();
            console.log(result);
            if (data.status === 401) {
                Server.refreshToken(sessionStorage.getItem('refresh_token'))
                Server.getProductInfo(product_id, token);
            } else {
                return result;
            }
    }

}

    static async sendProductFeedback(options, token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}actions/feedback`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify(options)
        });

        const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.sendProductFeedback(options, token);
        } else {
            return result;
        }
    }

    static async addProductToCart(id, token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}actions/cart`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify({
                id
            })
        });

        // const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.addProductToCart(id, token);
        } else {
            return data;
        }
    }

    static async addProductToWishList(id, token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}actions/wishlist`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify({
                id
            })
        });

        // const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.addProductToCart(id, token);
        } else {
            return data;
        }
    }

    static async getCartList(token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}actions/cart`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        });

        const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.getCartList(token);
        } else {
            return result;
        }
    }

    static async getWishList(token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}actions/wishlist`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        });

        const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.getCartList(token);
        } else {
            return result;
        }
    }

    static async RemoveProductFromCart(id, token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}actions/cart?product_id=${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        });

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.RemoveProductFromCart(token);
        } else {
            return data.status;
        }
    }

    static async removeComment(id, token = sessionStorage.getItem('access_token')) {
        console.log(`${this.basePoint}actions/cart?product_id=${id}`);
        const data = await fetch(`${this.basePoint}actions/feedback?feedback_id=${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        });

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.removeComment(id, token);
        } else {
            return data.status;
        }
    }

    static async removeItemFromWishList(id, token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`${this.basePoint}actions/wishlist?product_id=${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        });

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.removeItemFromWishList(id, token);
        } else {
            return data.status;
        }
    }

    static grabParamsFromURL() {
        const url = new URLSearchParams(document.location.search.substring(1));

        return Object.fromEntries(url.entries());
    }
}