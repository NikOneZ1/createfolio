import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import logout from "../Utils/logout";

export default function Header () {
        const [authorized, setAuthorized] = useState(false);

        useEffect(() => {
            if(localStorage.getItem("user")){
                console.log(localStorage.getItem("user"));
                setAuthorized(true);
            }
            else{
                setAuthorized(false);
            }
        }, []);

        const Logout = () => {
            logout(); 
            setAuthorized(false);
        }

        return (
            <div className='App'>
                <div className="container">
                    <header className="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
                        <Link to='/' style={{ textDecoration: 'none' }}>
                        <div href="" className="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-decoration-none" mb-checked="1" data-tip="">
                            <img className='logo' src="https://res.cloudinary.com/huvho6cay/image/upload/v1640185082/media/1291761_desktop_job_online_portfolio_portfolio_resume_icon_b4lmwy.png" alt="Createfolio"></img>
                            <h2 className='logo-font'>Createfolio</h2>
                        </div>
                        </Link>

                        <div className="col-md-3 text-end">
                            {!authorized && <Link to='/login' style={{ textDecoration: 'none' }} className="nav-element me-5">Login</Link>}
                            {!authorized && <a href="#" className="nav-element ml-5">Signup</a>}
                            {authorized && <Link to='/' style={{ textDecoration: 'none' }} className="nav-element me-5">Profile</Link>}
                            {authorized && <a href='#' onClick={() => Logout()} className="nav-element ml-5">Logout</a>}
                        </div>
                    </header>
                </div>
            </div>
        )
}