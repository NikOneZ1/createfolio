import axios from 'axios';

export default function login_service(username, password){
    return axios.post('/auth/jwt/create/', {username, password}).then(response => {
        if(response.data.access) {
            localStorage.setItem("user", JSON.stringify(response.data));
        }
        return [response.data];
    }).catch(error => {
        if(error.response){
            return [false, error.response.data, error.response.status]
        }
        return [false];
    });
}