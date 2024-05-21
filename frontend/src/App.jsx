import './App.css'
import axios from "axios";
import React, { useState, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import About from './components/About/About';
import Contact from './components/Contact/Contact';
import Header from './components/Home/Header';
import Navbar from './components/Navbar/Navbar';
import SignIn from './components/Signin/Signin';
import LectureQuizList from './components/LectureQuizList/LectureQuizList';

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
          <Route path="/" element={<Header />} />
          <Route path="/about" element={<Header />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/lecturequizes" element={<LectureQuizList />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
