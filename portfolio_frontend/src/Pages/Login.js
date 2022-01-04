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

    const [username_error, setUsernameError] = useState(false);
    const [password_error, setPasswordError] = useState(false);
    const [invalid_data, setInvalidData] = useState(false);

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
                if(resp[0]){
                    navigate('/');
                }

                if(resp[2]==401)
                {
                    setInvalidData(true);
                }

                try{
                    setUsernameError(resp[1]["username"]);
                }
                catch(err){
                    setUsernameError(false);
                }

                try{
                    setPasswordError(resp[1]["password"]);
                }
                catch(err){
                    setPasswordError(false);
                }
            });
        };
        response();
    }

    return (
        <div>
            <Header/>
            <div className="row text-center">
                <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    <form onSubmit={Submit}>
                        {invalid_data && <p className="error-p">Wrong username or password.</p>}
                        {username_error && <label className="error-message">{username_error}</label>}
                        <p><input placeholder="Username" type="username" id="username" name="username" value={login.username} onChange={changeInputLogin}/></p>
                        {password_error && <label className="error-message">{password_error}</label>}
                        <p><input placeholder="Password" type="password" id="password" name="password" value={login.password} onChange={changeInputLogin}/></p>
                        <input className="btn btn-outline-light" type="submit" value="Log in"/>
                    </form>
                </div>
            </div>
        </div>
    )
}