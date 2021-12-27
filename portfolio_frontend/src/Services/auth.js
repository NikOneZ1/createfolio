import axios from 'axios';

function login(username, password){
    return axios.post('/auth/jwt/create/', {username, password}).then(response => {
        if(response.dadta.accessToken) {
            localStorage.setItem("user", JSON.stringify(response.data));
        }

        return response.data;
    });
}

function logout() {
    localStorage.removeItem("user");
}