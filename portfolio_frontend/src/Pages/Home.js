import React, { Component } from 'react';
import {Link} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

import Header from '../Components/Header'

export default class Home extends Component {
    render() {
        return (
            <div className='App'>
                <Header/>
                <div className="position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center">
                    <div className="col-md-5 p-lg-5 mx-auto my-5">
                        <h1 className="header1">Create your own portfolio</h1>
                        <p className="homepage-text mt-4">Add information about yourself, your best projects and share it with other people.</p>                   
                        <a className="btn btn-outline-light" href="#" mb-checked="1" data-tip="">Create portfolio</a>
                    </div>
                </div>
            </div>
        )
    }
}