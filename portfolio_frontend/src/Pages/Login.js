import React, {useState} from "react";
import {useNavigate} from "react-router-dom";
import Header from "../Components/Header";
import login_service from "../Utils/login";

export default function Login () {
    let navigate = useNavigate();

    const [login, setLogin] = useState(() => {
        return {
            username: "",
            password: "",
        }
    })

    const changeInputLogin = event => {
        event.persist()
        setLogin(prev => {
            return {
                ...prev,
                [event.target.name]: event.target.value
            }
        })
    }

    const Submit = event => {
        event.preventDefault();
        let response = login_service(login.username, login.password);
        const resp = () => {
            response.then((resps) => {
                if(resps){
                    navigate('/');
                }
            });
        };
        resp();
    }

    return (
        <div className="text-center">
            <Header/>
            <form onSubmit={Submit}>
                <p>Username: <input type="username" id="username" name="username" value={login.username} onChange={changeInputLogin}/></p>
                <p>Password: <input type="password" id="password" name="password" value={login.password} onChange={changeInputLogin}/></p>
                <input className="btn btn-outline-light" type="submit" value="Log in"/>
            </form>
        </div>
    )
}