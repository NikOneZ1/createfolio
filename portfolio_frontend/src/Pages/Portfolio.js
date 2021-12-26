import React, { Component, useState, useEffect } from 'react';
import {Link, useParams} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import API from '../Utils/API';

const Portfolio = () => {   
    const [link, setLink] = useState(useParams().link);
    const [image, setImage] = useState(null);
    const [header, setHeader] = useState(null);
    const [about_me, setAboutMe] = useState(null);
    const [projects, setProjects] = useState(null);
    const [contacts, setContacts] = useState(null);

    useEffect(async () => {
        let data = await API.get("/api/portfolio/"+link);
        data = data.data
        setImage(data.image);
        setHeader(data.header);
        setAboutMe(data.about_me);
        setProjects(data.projects);
        setContacts(data.contacts);
    });

    return (
        <div className='container'>
            <div className="row">
                <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    <img className="mx-auto d-block portfolio-logo" src={image}></img>
                </div>
            </div>

            <div className="row">
                <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    <h1 className="header1 text-center">{ header }</h1>
                </div>
            </div>

            <div className="row">
                <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    <p className="text-center">{ about_me }</p>
                </div>
            </div>

            <div className="row">
                <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    <hr/>
                </div>
            </div>

            <div className="row">
                <div className="mx-auto d-block col col-xs-10 col-sm-10 col-md-10 col-lg-8">
                    <h1 className="header1 text-center">Projects</h1>
                </div>
            </div>
            <br/>

            {projects && projects.map(project => 
                <div className='row'>
                    <div className="mx-auto d-block col-xs-10 col-sm-10 col-md-10 col-lg-8">
                        <div className="row">
                            <div className="col-xs-12 col-sm-12 col-md-12 col-lg-6">
                                <a href={project.project_link} style={{ textDecoration: 'none' }}>
                                    <img className='project-image' src={ project.image }></img>
                                </a>
                            </div>
                            <div className="col-xs-12 col-sm-12 col-md-12 col-lg-6">
                                <a href={project.project_link} style={{ textDecoration: 'none' }}>
                                    <h1 className="header2 text-center">{project.name}</h1>
                                </a>
                                <p className="text-center">{ project.description }</p>
                            </div>
                        </div>
                        <hr/>
                    </div>
                </div>
            )}
            
            <div className="row">
                <div className="mx-auto d-block col col-xs-10 col-sm-10 col-md-10 col-lg-8">
                        <h1 className="header1 text-center">Contacts</h1>
                </div>
            </div>
            <br/>

            <div className="row">
                <div className="contact mx-auto d-block col col-xs-10 col-sm-10 col-md-10 col-lg-8 text-center">
                {contacts && contacts.map(contact =>
                    <div className="row justify-content-center">
                        <div className="col-1">
                            <img className='contact-logo' src={ contact.logo }></img>
                        </div>
                        <div className="col-3">
                            <a style={{ textDecoration: 'none' }} href={ contact.link }><p>{ contact.social_network }</p></a>
                        </div>
                    </div>
                )}
                </div>
            </div>

        </div>
    )
}

export default Portfolio