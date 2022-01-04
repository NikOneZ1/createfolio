import axios from 'axios';

export default function logout_service() {
    localStorage.removeItem("user");
}