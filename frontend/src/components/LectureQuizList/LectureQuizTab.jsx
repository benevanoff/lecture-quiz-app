import axios from "axios";
import { useNavigate } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import './LectureQuizList.css'

const LectureQuizTab = (props) => {

    const [ title, setTitle ] = useState('');
    const nav = useNavigate();

    useEffect(() => {
        const getLectureQuiz = async () => {
            try {
                const response = await axios.get('http://localhost:8080/l'+props.lecture_id)
                if (response.status == 200) {
                    console.log(response.data);
                    setTitle(response.data.title);
                }
            } catch (error) {
                console.log(error);
            }
        };
        getLectureQuiz();
    });
    return <span className='lecture-preview' key={'lecture-'+props.lecture_id} onClick={(e) => {nav('/lecture/' + props.lecture_id)}}>{title}</span>;
};

export default LectureQuizTab;