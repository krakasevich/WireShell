import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './styles/Registration.css'

const API_URL = "http://51.21.167.201:8000";

function RegisterPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleSignInRedirect = () => {
        navigate("/login");
    };

    const validateForm = () => {
        if (!username || username.length < 3) {
            setMessage("Username must be at least 3 characters long");
            return false;
        }
        
        if (!password || password.length < 6) {
            setMessage("Password must be at least 6 characters long");
            return false;
        }
        
        return true;
    }

    const handleRegister = async () => {
        if (!validateForm()) return;

        try {
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                setMessage("Registration successful!");
                setTimeout(() => {
                    navigate("/login");
                }, 2000);
            } else {
                setMessage(data.detail || "Registration failed");
            }
        } catch (error) {
            setMessage("Error connecting to server");
            console.error('Error:', error);
        }
    };
  
    return (
        <div className="auth_block">
            <div>
                <h2>Create your account</h2>
                <p>Join us today!</p>
            </div>
  
            <div className="user_info">
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>  
  
            <div className="auth_button">
                <button onClick={handleRegister}>Create Account</button>
                {message && <p>{message}</p>}
            </div>

            <div className="auth_switch">
                <p>Already have an account? <button onClick={handleSignInRedirect}>Sign In</button></p>
            </div>
        </div>
    );
}
  
export default RegisterPage;