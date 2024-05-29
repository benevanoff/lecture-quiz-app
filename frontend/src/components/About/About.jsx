import React from "react";
import styles from "./About.module.css"

const About = () => {
    return (
        <>
        <h1 className={styles.heading}>LecQuiz</h1>
        <div className={styles.container}>
        <hr />
            <div className={styles.txt_des}>
                <h1>Know more!</h1>
                <p>Welcome to LecQuiz!, where knowledge meets fun! Our platform is designed to help you expand your understanding across a variety of topics through engaging quizzes and interactive learning modules. Whether you're a trivia enthusiast, a student looking to supplement your studies, or simply someone curious about the world around you, our services offers a diverse range of quizzes on subjects spanning from science and history to literature. With each quiz, you'll not only test your existing knowledge but also uncover new facts and insights, making learning an enjoyable and rewarding experience. Join our community of curious minds and embark on a journey of continuous!</p>
            </div>
            <div className={styles.side_img}>

                <img src="/home-header-image.svg" alt="img" />
            </div>
        </div>
        <center>
            <p>Source code for this application can be found on GitHub</p>
            <p>To report a bug, please open a GitHub issue: https://github.com/benevanoff/lecture-quiz-app/issues</p>
        </center>
        </>
    )
}

export default About;