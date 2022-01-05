import React, { useState, useEffect } from 'react';
import {Link, useParams } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import API from '../Utils/API';
import Header from '../Components/Header'

export default function Profile () {
    const [portfolios, setPortfolios] = useState('');

    useEffect(() => {
        async function get_portfolios() {
            const token = "JWT " + JSON.parse(localStorage.getItem("user")).access;
            const user_portfolios = await API.get('api/user_portfolio', {headers: {'Authorization': token}})
            setPortfolios(user_portfolios.data);
        }
        get_portfolios();
    }, []);

    return (
        <div>
            <Header/>
            <div className="row">
                <div className="mx-auto d-block col col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    <h1 className="header1 text-center">My portfolios</h1>
                </div>
            </div>
            <br/>
            {portfolios && portfolios.map(portfolio => 
                <div className='row'>
                    <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                        <div className="row">
                            <div className="col-xs-12 col-sm-12 col-md-12 col-lg-6">
                                <Link to={`/portfolio/${portfolio.link}`} style={{ textDecoration: 'none' }}>
                                    <img className='project-image' src={ portfolio.image }></img>
                                </Link>
                            </div>
                            <div className="col-xs-12 col-sm-12 col-md-12 col-lg-6">
                                <Link to={`/portfolio/${portfolio.link}`} style={{ textDecoration: 'none' }}>
                                    <h1 className="header2 text-center">{portfolio.header}</h1>
                                </Link>
                                <Link to={`/portfolio/${portfolio.link}`} style={{ textDecoration: 'none' }}>
                                    <p className="text-center">{ portfolio.about_me }</p>
                                </Link>
                            </div>
                        </div>
                        <br/>
                        <div className="row">
                            <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8 text-center">
                                <Link to={'/'} style={{marginRight: 10, textDecoration: 'none' }}><button className=" text-center mr-3 ml-3 pl-3 ml-3 btn btn-outline-light">Change</button></Link>
                                <Link to={'/'} style={{marginLeft: 10, textDecoration: 'none' }}><button className=" text-center mr-3 btn btn-outline-danger">Delete</button></Link>
                            </div>
                        </div>
                        <hr/>
                    </div>
                </div>
            )}
        </div>
    )
}