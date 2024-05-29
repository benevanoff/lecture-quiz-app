import styles from "./Navbar.module.css";
import '../../Global.css'
import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { HiAcademicCap } from "react-icons/hi";



const Navbar = (props) => {
    const nav = useNavigate();
    const location = useLocation();
    const options_logged_out = ["Home", "Sign In", "About"];
    const options_logged_in = ["Home", "Profile", "About"];
    const links = {"Home": "/", "Sign In": "/signin", "About": "/about", "Contact": "/contact", "Profile": "/profile"};

    return (
        <>
            <nav className={styles.container}>
                <div className={`${styles.logo} slide_in_left`} onClick={() => {nav(links["Home"])}}>
                    <HiAcademicCap size="40px" />
                    <h1>LecQuiz</h1>
                </div>
                <div className={styles.list_container}>
                    <ul className={styles.ul_options}>
                        {props.isLoggedIn && options_logged_in.map((option) => {
                            return (
                                <li key={option} onClick={() => {nav(links[option])}} style={{ color: location.pathname === links[option] ? "black" : "inherit" }}>
                                    {option}
                                </li>
                            );
                        })}
                        {!props.isLoggedIn && options_logged_out.map((option) => {
                            return (
                                <li key={option} onClick={() => {nav(links[option])}} style={{ color: location.pathname === links[option] ? "black" : "inherit" }}>
                                    {option}
                                </li>
                            );
                        })}
                    </ul>
                </div>
            </nav>
        </>
    );
}

export default Navbar;
