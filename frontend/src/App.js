import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import './styles/Global.css'
import HomePage from "./Homepage";
import RegisterPage from "./Registration";
import Login from "./Login";
import VPN from "./VPN";

function Profile() {
    const [isOpen, setIsOpen] = useState(false);
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            setUser(JSON.parse(userData));
        }
    }, []);

    const handleSwitchAccount = () => {
        localStorage.removeItem('user');
        navigate('/login');
    };

    const handleLogout = () => {
        localStorage.removeItem('user');
        navigate('/');
    };

    if (!user) return null;

    return (
        <div className="profile_container">
            <button 
                className="profile_button"
                onClick={() => setIsOpen(!isOpen)}
            >
                Profile
            </button>
            {isOpen && (
                <div className="profile_dropdown">
                    <p>Welcome, {user.username}!</p>
                    <button className="switch_account" onClick={handleSwitchAccount}>
                        Switch Account
                    </button>
                    <button className="logout" onClick={handleLogout}>
                        Logout
                    </button>
                </div>
            )}
        </div>
    );
}

function Header() {
    const location = useLocation();
    const userData = localStorage.getItem('user');
    const showProfile = location.pathname === '/vpn' && userData;

    return (
        <div className="header_container">
          <h2 className='caption'>
            SecureNet
            {showProfile && <Profile />}
          </h2>
        </div>
    );
}

function AppContent() {
    return (
        <div>
            <Header />
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/registration" element={<RegisterPage />} />
                <Route path="/login" element={<Login />} />
                <Route path="/vpn" element={<VPN />} />
            </Routes>
        </div>
    );
}

function App() {
    return (
        <Router>
            <AppContent />
        </Router>
    );
}

export default App;