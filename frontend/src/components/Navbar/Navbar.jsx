import React from "react";
import styles from "./Navbar.module.css"
import { HiAcademicCap } from "react-icons/hi2";
import { Link } from 'react-router-dom';


const Navbar = () => {
    const options = ["Home", "Signin", "about", "Contact"]

    return (<>
        <nav className={styles.container}>
            <div className={styles.logo}>
                <HiAcademicCap size="40px" />
                <h1>LecQuiz</h1>
            </div>
            <div className={styles.list_container}>
                <ul className={styles.ul_options}>
                    {options.map((option) => (
                        <Link key={option} to={`/${option.toLowerCase()}`}>{option}</Link>
                    ))}
                </ul>
            </div>
        </nav>
    </>)
}

function myFunction(option) {
    if (option === "Home") {
        console.log("directed to Home");
    }
}

export default Navbar