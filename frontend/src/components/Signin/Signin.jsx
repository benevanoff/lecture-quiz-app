import axios from "axios";
import React, { useState } from 'react';
import "./Signin.css"

const HOST =  "http://localhost:8080/login"; // TODO: replace with environment variable

const SignIn = () => {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMsg, setError] = useState(false);

    const submitSignIn = async () => {
        try {
            const response = await axios.post(
             HOST,
              {username: username, password: password},
              {
                headers: {
                  "Content-Type": "application/json",
                },
                withCredentials: true
              },
            );
      
            if (response.status === 200) {
                setError(false);
                console.log("loggin success");
            }
          } catch (error) {
            if (error.response.status == 403) setError('Invalid Credentials');
            console.log(error.message);
          }
    };

    return (<>
        <center>
        {errorMsg && <p>Error: {errorMsg}</p>}
        <h1>Sign In</h1>
        <div className="input-boxes">
            <input type="text" id="signin-username-input" onChange={ (e) => setUsername(e.target.value)}/>
            <input type="password" id="signin-password-input" onChange={(e) => setPassword(e.target.value)}/>
        </div>
        <button onClick={submitSignIn}>Submit</button>
        </center>
    </>);
};

export default SignIn;