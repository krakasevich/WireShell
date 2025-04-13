import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import "./styles/Dashboard.css";

const API_URL = "http://51.21.167.201:8000";

function Dashboard() {
    const [selectedLocation, setSelectedLocation] = useState('Sweden');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [user, setUser] = useState(null);

    useEffect(() => {
        const userData = localStorage.getItem('user');
        if (!userData) {
            navigate('/');
            return;
        }
        setUser(JSON.parse(userData));
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('user');
        navigate('/');
    };

    const handleDownloadConfig = async () => {
        try {
            const response = await fetch(`${API_URL}/generate-config`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    location: selectedLocation.toLowerCase(),
                    user_id: user.id
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate config');
            }
            
            const data = await response.json();
            const blob = new Blob([data.config], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `wireguard-${selectedLocation.toLowerCase()}.conf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error generating config:', error);
            setError('Error generating configuration file: ' + error.message);
        }
    };

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div className="dashboard-container">
            <div className="header">
                <h2>Welcome, {user.username}!</h2>
                <button onClick={handleLogout} className="logout-button">Logout</button>
            </div>
            
            <div className="content">
                <div className="location-selector">
                    <h3>Select Location</h3>
                    <select 
                        value={selectedLocation}
                        onChange={(e) => setSelectedLocation(e.target.value)}
                    >
                        <option value="Sweden">Sweden</option>
                        <option value="Netherlands">Netherlands</option>
                        <option value="Germany">Germany</option>
                    </select>
                </div>
                
                <button onClick={handleDownloadConfig} className="download-button">
                    Download Configuration
                </button>
                
                {error && <p className="error">{error}</p>}
            </div>
        </div>
    );
}

export default Dashboard; 