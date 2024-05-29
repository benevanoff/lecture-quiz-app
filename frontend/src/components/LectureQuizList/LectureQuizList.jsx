import axios from "axios";
import React, { useState, useEffect } from 'react';
import styles from "./LectureQuizList.module.css"
import LectureQuizTab from "./LectureQuizTab";

const LectureQuizList = () => {

  const [lectures, setLectures] = useState([]);

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
  
  return (<>
    <div className={styles.quiz_list}>
      <h1>Lectures</h1>
      <div className={`${styles.lecture_list_container}`}>
        <ol>
          {lectures.map(({lecture_id}) => {
            return <LectureQuizTab key={lecture_id} lecture_id={lecture_id} />
          })}
        </ol>
      </div>
      <button className={'btn_dark'}>Let's Start</button>
    </div>
  </>);
};

export default LectureQuizList;
