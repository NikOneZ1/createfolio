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
    
    const [registration_failed, setRegistrationFailed] = useState(false);

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
                if(resp){
                    navigate('/login');
                }
                setRegistrationFailed(true);
            });
        };
        response();
    }

    return (
        <div>
        <Header/>
        <div className="row text-center">
            <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    {registration_failed && <div className="alert"><p className="alert-p">Wrong data. Please, input correct data.</p></div>}
                    <form onSubmit={Submit}>
                        <p><input placeholder="Email" type="email" id="email" name="email" value={registration.email} onChange={changeRegistrationInput}/></p>
                        <p><input placeholder="Username" type="username" id="username" name="username" value={registration.username} onChange={changeRegistrationInput}/></p>
                        <p><input placeholder="Password" type="password" id="password" name="password" value={registration.password} onChange={changeRegistrationInput}/></p>
                        <input className="btn btn-outline-light" type="submit" value="Sign up"/>
                    </form>
                </div>
            </div>
        </div>
    )
}