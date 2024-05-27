import React from 'react'
import styles from './Home.module.css';

const Home = () => {

    return (<>
        <h1 className={styles.home_header_heading}>Lecture Quizzes</h1>
        <h2></h2>
        <header className={styles.home_header}>
            <div className={styles.content}>
                <div>
                    <p>Introducing our innovative quiz app, designed to make learning Science, English, and Maths both fun and effective! Our app offers a comprehensive range of quizzes that cover essential terms, concepts, and phrases in these subjects, helping users enhance their vocabulary and comprehension.</p>
                    <button>
                        Start Learning!
                    </button>
                </div>
                <img src="../../../public/achievement-svgrepo-com.svg" alt="img" />
            </div>
        </header>
        <hr />
        <div>
            <section className={styles.home_section1}>
                <h1>Features</h1>
                <ul className={styles.home_ul}>
                    <li>
                        Engaging Quizzes:
                        <p> With a variety of interactive quizzes, users can test their knowledge and reinforce learning through immediate feedback.</p>
                    </li>
                    <li>
                        Quality Content:
                        <p> Our content is developed and reviewed by experienced educators and professionals in each field, ensuring that the material is both accurate and up-to-date.</p>
                    </li>
                    <li>
                        Progress Tracking:
                        <p> Users can track their progress over time, identify areas for improvement, and celebrate their achievements.</p>
                    </li>
                    <li>
                        Diverse Topics:
                        <p>From grammar and vocabulary in English to complex equations in Maths and scientific concepts in Science, our quizzes cover a wide range of topics, providing a well-rounded learning experience.</p>
                    </li>
                    <li>
                        User-Friendly Interface:
                        <p> Our intuitive design makes it easy for users of all ages to navigate and enjoy the learning process.</p>
                    </li>
                </ul>
            </section>
            <section className={styles.home_section2}>
            </section>
            <section className={styles.home_section3}>

            </section>
        </div>
    </>)
}

export default Home;
