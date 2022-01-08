import axios from 'axios';

export default function registration_service(email, username, password) {
    return axios.post('auth/users/', {email, username, password}).then(response => {
        if(response.status) {
            return [true];
        }
        return [false];
    }).catch(error => {
        if(error.response){
            return [false, error.response.data]
        }
        return [false];
    })
};