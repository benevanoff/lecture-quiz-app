import axios from "axios";
import React, { useState, useEffect } from 'react';
import LectureQuizTab from "./LectureQuizTab";

const LectureQuizList = () => {

    const [ lectures, setLectures ] = useState([]);
  
    useEffect(() => {
      const getLectureQuizes = async () => {
        try {
          const response = await axios.get('http://localhost:8080/lectures')
          if (response.status == 200) {
              console.log(response.data);
              setLectures(response.data);
          }
        } catch (error) {
          console.log(error);
        }
      };
      getLectureQuizes();
    }, []);
  
    return (<center>
      <h1>Lecture Quizzes</h1>
      {lectures.map((lecture_id) => {
        return <LectureQuizTab key={lecture_id} lecture_id={lecture_id}/>
      })}
    </center>);
  };

  export default LectureQuizList;