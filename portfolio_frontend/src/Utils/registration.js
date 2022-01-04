import axios from 'axios';

export default function registration_service(email, username, password) {
    return axios.post('auth/users/', {email, username, password}).then(response => {
        if(response.status) {
            return true;
        }
        return false;
    }).catch(error => {
        return false;
    })
};