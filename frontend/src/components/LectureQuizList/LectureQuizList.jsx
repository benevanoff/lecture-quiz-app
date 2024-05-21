import axios from "axios";
import React, { useState, useEffect } from 'react';

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
      {lectures.map((e) => {
        return <span key={'lecture-span-'+{e}}>Lecture ID: {e /*TODO: Make a custom component to render the lecture title from the lecture ID*/}</span>;
      })}
    </center>);
  };

  export default LectureQuizList;