import './App.css'
import axios from "axios";
import React, { useState, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import Register from './components/Register/Register';
import About from './components/About/About';
import Navbar from './components/Navbar/Navbar';
import SignIn from './components/Signin/Signin';
import LectureQuizList from './components/LectureQuizList/LectureQuizList';
import LecturePage from './components/Lecture/LecturePage';
import Home from './components/Home/Home'

const App = () => {

  const [ isLoggedInState, setIsLoggedIn ] = useState(false);

  useEffect(() => {
    const isLoggedIn = async () => {
        try {
            const response = await axios.get('http://localhost:8080/account', { headers: { "Content-Type": "application/json" }, withCredentials: true })
            if (response.status == 200) {
                console.log(response.data);
                setIsLoggedIn(true);
            }
        } catch (error) {
          console.log(error);
          setIsLoggedIn(false);
        }
    }
    isLoggedIn();
}, [isLoggedInState]);

  return (
    <>
      <BrowserRouter>
        <Navbar isLoggedIn={isLoggedInState}/>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/register" element={<Register />} />
          <Route path="/lecturequizes" element={<LectureQuizList />} />
          <Route path="/lecture/:lecture_id" element={<LecturePage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
