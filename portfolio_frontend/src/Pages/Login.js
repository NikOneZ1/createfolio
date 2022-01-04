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
    const [login_failed, setLoginFailed] = useState(false);

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
        const response = () => {
            login_service(login.username, login.password).then((resp) => {
                if(resp){
                    navigate('/');
                }
                setLoginFailed(true);
            });
        };
        response();
    }

    return (
        <div>
            <Header/>
            <div className="row text-center">
                <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    {login_failed && <div className="alert"><p className="alert-p">Wrong username or password. Please, input correct data.</p></div>}
                    <form onSubmit={Submit}>
                        <p>Username: <input type="username" id="username" name="username" value={login.username} onChange={changeInputLogin}/></p>
                        <p>Password: <input type="password" id="password" name="password" value={login.password} onChange={changeInputLogin}/></p>
                        <input className="btn btn-outline-light" type="submit" value="Log in"/>
                    </form>
                </div>
            </div>
        </div>
    )
}