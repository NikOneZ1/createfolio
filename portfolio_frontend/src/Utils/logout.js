import axios from 'axios';

export function logout() {
    localStorage.removeItem("user");
}