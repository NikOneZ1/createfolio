import React, {useState} from "react";
import {useNavigate} from "react-router-dom";
import Header from "../Components/Header";
import registration_service from "../Utils/registration";

export default function Registration() {
    let navigate = useNavigate();

    const [registration, setRegistration] = useState(() => {
        return {
            email: "",
            username: "",
            password: "",
        }
    })
    
    const [email_error, setEmailError] = useState(false);
    const [username_error, setUsernameError] = useState(false);
    const [password_error, setPasswordError] = useState(false);

    const changeRegistrationInput = event => {
        event.persist()
        setRegistration(prev => {
            return {
                ...prev,
                [event.target.name]: event.target.value
            }
        })
    }

    const Submit = event => {
        event.preventDefault();
        const response = () => {
            registration_service(registration.email, registration.username, registration.password).then((resp) => {
                if(resp[0]){
                    navigate('/login');
                }
                try{
                    setEmailError(resp[1].email);
                }
                catch(err){
                    setEmailError(false);
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
                    <h1 className="header1 text-center">Signup</h1>
                    <form onSubmit={Submit}>
                    {email_error && <label className="error-message">{email_error}</label>}                       
                        <p><input title="error" placeholder="Email" type="text" id="email" name="email" value={registration.email} onChange={changeRegistrationInput}/></p>
                        {username_error && <label className="error-message">{username_error}</label>}
                        <p><input placeholder="Username" type="text" id="username" name="username" value={registration.username} onChange={changeRegistrationInput}/></p>
                        {password_error && <label className="error-message">{password_error}</label>}
                        <p><input placeholder="Password" type="password" id="password" name="password" value={registration.password} onChange={changeRegistrationInput}/></p>
                        <input className="btn btn-outline-light" type="submit" value="Sign up"/>
                    </form>
                </div>
            </div>
        </div>
    )
}