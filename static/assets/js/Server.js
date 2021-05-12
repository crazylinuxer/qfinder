class Server {
    static basePoint = 'http://127.0.0.1:5000/api/v1/';
    

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
        const r = await data.json();

        console.log(r);

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

        const r = await data.json();

        for (const key in r) {
            if (Object.hasOwnProperty.call(r, key)) {
                const element = r[key];
                sessionStorage.setItem(key, element);
            }
        }

        console.log(r);
        return data.status
    }

    static async getUserInfo(token = sessionStorage.getItem('access_token')) {
            const data = await fetch(`http://127.0.0.1:5000/api/v1/user`, {
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
                console.log(result);
                return data.status
            }
    }

    static async refreshToken(token) {
        const data = await fetch(`http://127.0.0.1:5000/api/v1/user/auth/refresh`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`  
                }
        })
        const res = await data.json();

        for (const key in res) {
            if (Object.hasOwnProperty.call(res, key)) {
                const element = res[key];
                sessionStorage.setItem(key, element);
            }
        }

        console.log(res)
    }

    static logout() {
      sessionStorage.setItem('user', null);
      sessionStorage.removeItem('refresh_token');
      sessionStorage.removeItem('access_token');
      sessionStorage.removeItem('id');
    }

    static async updateAccoutInfo(userData, token = sessionStorage.getItem('access_token')) {
        const data = await fetch(`http://127.0.0.1:5000/api/v1/user`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const result = await data.json();

        if (data.status === 401) {
            Server.refreshToken(sessionStorage.getItem('refresh_token'))
            Server.updateAccoutInfo(userData, token);
        } else {
            console.log(result);
            return data.status
        }

        console.log(result);
    }
}

// Server.signUp('Anton', 'Burchak', 'anton.burchak@mail.ru', 'qwerTy123')