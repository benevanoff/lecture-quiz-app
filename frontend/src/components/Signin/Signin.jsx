import styles from "./Signin.module.css";
import axios from "axios";
import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";

const HOST = "http://localhost:8080/login"; // TODO -> replace with environment variable

const SignIn = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setError] = useState('');

  const submitSignIn = async (e) => {
    e.preventDefault(); // Prevent form from submitting the default way
    try {
      const response = await axios.post(
        HOST,
        { username, password },
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true
        },
      );

      if (response.status === 200) {
        setError(false);
        console.log("login success");
        window.location.reload(); // reload the whole page - hack to reload the Navbar since the query effect is in the application root component
      }
    } catch (error) {
      if (error.response && error.response.status === 403) {
        setError('Invalid credentials')
      } else {
        setError('an error occured');
      }
      console.log(error.message);
    }
  };

  const handleRegisterRedirect = (e) => {
    e.preventDefault(); // Prevent default anchor behavior
    navigate('/register');
  };

  return (
    <>
      <form className={styles.signin_form} onSubmit={submitSignIn}>
        {errorMsg && <p style={{ color: 'red' }}>Error: {errorMsg}</p>}
        <h1>Sign-In</h1>
        <div className={styles.input_boxes}>
          <input
            placeholder="Email"
            type="text"
            id="signin-username-input"
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            placeholder="Password"
            type="password"
            id="signin-password-input"
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" onClick={submitSignIn}>Submit</button>
        <p>
          New user? &nbsp;
          <a href="/register" onClick={handleRegisterRedirect}>register here</a>
        </p>
      </form>
    </>
  );
};

export default SignIn;
