import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './styles/Login.css';

const API_URL = "http://51.21.167.201:8000";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${API_URL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username,
                    password,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Login error: ${errorData.detail}`);
            }

            const data = await response.json();
            console.log('Login response data:', data);
            
            const userData = {
                id: data.user_id,
                username: data.username
            };
            console.log('Saving user data:', userData);
            
            localStorage.setItem("user", JSON.stringify(userData));
            console.log('Stored in localStorage:', localStorage.getItem("user"));
            
            navigate("/vpn");
        } catch (error) {
            console.error("Login error:", error);
            setError(error.message);
        }
    };

    const handleRegister = () => {
        navigate("/registration");
    };

    return (
        // <div className="login-container">
        <div className="auth_block">
            <div>
                <h2>Welcome back!</h2>
                <p>Sign in to your account</p>
            </div>
            
            <form onSubmit={handleSubmit}>
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
                <button className="btn_submit" type="submit">Sign In</button>
                {error && <p className="error">{error}</p>}
            </form>

            <div className="auth_switch">
                <p>Don't have an account? <button className="register" onClick={handleRegister}>Register</button></p>
            </div>
        </div>
    );
}

export default Login;