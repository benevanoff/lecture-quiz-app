import styles from "./Signin.module.css";
import axios from "axios";
import React, { useState } from 'react';



const HOST =  "http://localhost:8080/login"; // TODO -> replace with enviroment variable

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
                window.location.reload(); // reload the whole page - hack to reload the Navbar since the query effect is in the application root component
            }
          } catch (error) {
            if (error.response.status == 403) setError('Invalid Credentials');
            console.log(error.message);
          }
    };

    return (<>
        <form>
        {errorMsg && <p>Error: {errorMsg}</p>}
        <h1>Sign-In</h1>
        <div className={styles.input_boxes}>
            <input placeholder="Email" type="text" id="signin-username-input" onChange={ (e) => setUsername(e.target.value)}/>
            <input placeholder="password" type="password" id="signin-password-input" onChange={(e) => setPassword(e.target.value)}/>
        </div>
        <button onClick={submitSignIn}>Submit</button>
        <p>New user? &nbsp; <a href="" >register here</a></p>
        </form>
    </>);
};

export default SignIn;