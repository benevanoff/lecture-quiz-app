import styles from "./Register.module.css";
import axios from "axios";
import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";

const REGISTER_URL = "http://localhost:8080/register"; // TODO -> replace with environment variable

const Register = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errorMsg, setError] = useState('');

    const submitRegister = async (e) => {
        e.preventDefault(); // Prevent form from submitting the default way

        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        try {
            const response = await axios.post(
                REGISTER_URL,
                { email, password },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                    withCredentials: true
                },
            );

            if (response.status === 200) {
                setError(false);
                console.log("Registration success");
                // Redirect to sign-in page on successful registration
                navigate('/signin');
            }
        } catch (error) {
            if (error.response) {
                if (error.response.status === 400) {
                    setError('Invalid input');
                } else if (error.response.status === 409) {
                    setError('Email already exists');
                } else {
                    setError('An error occurred');
                }
            } else {
                setError('An error occurred');
            }
            console.log(error.message);
        }
    };

    const signinRedirect = (e) => {
        e.preventDefault(); // Prevent default anchor behavior
        navigate('/signin');
    };

    return (
        <>
            <form className={styles.register_form} onSubmit={submitRegister}>
                {errorMsg && <p style={{ color: 'red' }}>Error: {errorMsg}</p>}
                <h1>Register</h1>
                <div className={styles.input_boxes}>
                    <input
                        placeholder="Email"
                        type="email"
                        id="register-email-input"
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        placeholder="Password"
                        type="password"
                        id="register-password-input"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <input
                        placeholder="Confirm Password"
                        type="password"
                        id="register-confirm-password-input"
                        onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                </div>
                <button type="submit" onClick={submitRegister}>Register</button>
                <p>Already have an account? &nbsp; <a href="" onClick={signinRedirect}>Sign in here</a></p>
            </form>
        </>
    );
};

export default Register;
