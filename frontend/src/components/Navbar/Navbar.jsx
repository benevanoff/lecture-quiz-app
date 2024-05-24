
import styles from"./Navbar.module.css"
import React, { useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom";
import { HiAcademicCap } from "react-icons/hi2";
import { Link } from 'react-router-dom';


const Navbar = (props) => {
    const nav = useNavigate();
    const options_logged_out = ["Home", "Sign In", "About"]
    const options_logged_in = ["Home", "Profile", "About"]
    const links = {"Home": "/", "Sign In": "/signin", "About": "/about", "Contact": "contact", "Profile": "/profile"};
    return (
        <>
            <nav className= {styles.container}>
                <div className={styles.logo}>
                    <HiAcademicCap size="40px" />
                    <h1>LecQuiz</h1>
                </div>
                <div className={styles.list_container}>
                    <ul className={styles.ul_options}>
                        {props.isLoggedIn && options_logged_in.map((option) => {
                            return <li key={option} onClick={() => {nav(links[option])}}>{option}</li>
                        })}
                        {!props.isLoggedIn && options_logged_out.map((option) => {
                            return <li key={option} onClick={() => {nav(links[option])}}>{option}</li>
                        })}
                    </ul>
                </div>
            </nav>
        </>
    )
}

export default Navbar;