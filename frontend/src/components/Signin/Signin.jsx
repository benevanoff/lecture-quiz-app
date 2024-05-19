import axios from "axios";
import React, { useState } from 'react';

const HOST =  "http://localhost:8080/login"; // TODO: replace with environment variable

const SignIn = () => {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

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
                console.log("loggin success");
            }
          } catch (error) {
            console.log(error.message);
          }
    };

    return (<>
        <h1>Sign In</h1>
        <div>
            <input type="text" id="signin-username-input" onChange={ (e) => setUsername(e.target.value)}/>
            <input type="password" id="signin-password-input" onChange={(e) => setPassword(e.target.value)}/>
        </div>
        <button onClick={submitSignIn}>Submit</button>
    </>);
};

export default SignIn;