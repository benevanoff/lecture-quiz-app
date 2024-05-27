import axios from "axios";
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const LecturePage = () => {
    const { lecture_id } = useParams();
    const [ lectureTitle, setTitle ] = useState('');
    const [ lectureBody, setBody ] = useState('');

    useEffect(() => {
        const getLectureQuiz = async () => {
            try {
                const response = await axios.get('http://localhost:8080/l'+lecture_id)
                if (response.status == 200) {
                    console.log(response.data);
                    setTitle(response.data.title);
                    setBody(response.data.body)
                }
            } catch (error) {
                console.log(error);
            }
        };
        getLectureQuiz();
    });

    return (<>
    <div className={StyleSheet.quiz_card}>    
            <h1>{lectureTitle}</h1>
            <p>{lectureBody}</p>
    </div>
    </>)};

export default LecturePage;