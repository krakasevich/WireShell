import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/VPN.css';

const API_URL = "http://51.21.167.201:8000";

const locations = [
    { value: "sweden", label: "Sweden" }
];

function VPN() {
    const [selectedLocation, setSelectedLocation] = useState(locations[0].value);
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const storedData = localStorage.getItem('user');
        if (storedData) {
            const parsedData = JSON.parse(storedData);
            setUserData({
                user_id: parsedData.id,
                username: parsedData.username
            });
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('user');
        navigate('/login');
    };

    const handleDownloadConfig = async () => {
        if (!userData) {
            navigate('/login');
            return;
        }

        try {
            setIsLoading(true);
            setError('');

            const response = await fetch(`${API_URL}/api/generate-config`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userData.user_id,
                    location: selectedLocation
                }),
            });

            if (!response.ok) {
                throw new Error(`Error generating configuration file: ${await response.text()}`);
            }

            const data = await response.json();
            
            // Создаем blob из конфигурации
            const blob = new Blob([data.config], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            
            // Создаем временную ссылку для скачивания
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            
            // Очищаем
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            setError(error.message);
            console.error('Error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="vpn-container">
            <div className="header">
                <h1>VPN Dashboard</h1>
                <button onClick={handleLogout} className="logout-button">Logout</button>
            </div>

            <div className="content">
                <div className="location-selector">
                    <h2>Select Location</h2>
                    <select 
                        value={selectedLocation} 
                        onChange={(e) => setSelectedLocation(e.target.value)}
                    >
                        {locations.map((location) => (
                            <option key={location.value} value={location.value}>{location.label}</option>
                        ))}
                    </select>
                </div>

                <div className="download-section">
                    <button 
                        onClick={handleDownloadConfig}
                        disabled={isLoading}
                        className="download-button"
                    >
                        {isLoading ? 'Generating...' : 'Download Configuration'}
                    </button>
                    {error && <p className="error">{error}</p>}
                </div>

                <div className="instructions">
                    <h2>Setup Instructions</h2>
                    <ol>
                        <li>Download and install WireGuard client from <a href="https://www.wireguard.com/install/" target="_blank" rel="noopener noreferrer">here</a></li>
                        <li>Download your configuration file by clicking the button above</li>
                        <li>Open WireGuard and click "Import tunnel(s) from file"</li>
                        <li>Select the downloaded configuration file</li>
                        <li>Click "Activate" to start the VPN tunnel</li>
                    </ol>
                </div>
            </div>
        </div>
    );
}

export default VPN;