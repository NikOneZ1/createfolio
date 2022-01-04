import axios from 'axios';

export default function logout() {
    localStorage.removeItem("user");
}