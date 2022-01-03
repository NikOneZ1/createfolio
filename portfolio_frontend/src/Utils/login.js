import axios from 'axios';

export default function login_service(username, password){
    return axios.post('/auth/jwt/create/', {username, password}).then(response => {
        if(response.data.access) {
            localStorage.setItem("user", JSON.stringify(response.data));
        }
        return response.data;
    }).catch(error => {
        if (error.response) {
            //console.log(error.response.data);
            //console.log(error.response.status);
            //console.log(error.response.headers);
        } else if (error.request) {
            //console.log(error.request);
        } else {
            //console.log("Error", error.message);
        }
        return false;
    });
}