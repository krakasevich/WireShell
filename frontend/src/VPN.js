import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles/VPN.css';

const API_URL = "http://51.21.167.201:8000";

const locations = [
    { value: "sweden", label: "Sweden" },
    { value: "london", label: "London" }
];

function VPN() {
    const [selectedLocation, setSelectedLocation] = useState(locations[0].value);
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isInstructionsOpen, setIsInstructionsOpen] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const storedData = localStorage.getItem('user');
        console.log('Stored data in localStorage:', storedData);

        if (storedData) {
            const parsedData = JSON.parse(storedData);
            console.log('Parsed user data:', parsedData);

            setUserData({
                user_id: parsedData.id,
                username: parsedData.username
            });
        } else {
            console.log('No user data found in localStorage');
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('user');
        navigate('/');
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
        <div className="vpn_page">
            <div className="vpn_header">
                <h1>Welcome, {userData?.username}!</h1>
                <button onClick={handleLogout} className="logout_button">Logout</button>
            </div>

            <div className="vpn_content">
                <h2>Download the configuration file for WireGuard</h2>
                <div className='location_selector'>
                    <label htmlFor="Location">Select Location</label>
                    <select 
                        value={selectedLocation} 
                        onChange={(e) => setSelectedLocation(e.target.value)}
                        className="location_dropdown"
                    >
                        {locations.map((location) => (
                            <option key={location.value} value={location.value}>{location.label}</option>
                        ))}
                    </select>
                </div>

                <div className="download_section">
                    <button 
                        onClick={handleDownloadConfig}
                        disabled={isLoading}
                        className="download_button"
                    >
                        {isLoading ? 'Generating...' : 'Download'}
                    </button>
                    {error && <p className="error">{error}</p>}
                </div>

                <div className="setup_instructions">
                    <div className="instructions_header" onClick={() => setIsInstructionsOpen(!isInstructionsOpen)}>
                        <h3>Setup Instructions</h3>
                        <button className="toggle_button">
                            {isInstructionsOpen ? '▼' : '▶'}
                        </button>
                    </div>
                    
                    <div className={`instructions_content ${isInstructionsOpen ? 'open' : ''}`}>
                        <div className="instruction_step">
                            <h4>1. Download and Install the WireGuard Client</h4>
                            <p>Go to the official WireGuard website and download the appropriate client for your operating system:</p>
                            <a href="https://www.wireguard.com/install/" target="_blank" rel="noopener noreferrer">
                                https://www.wireguard.com/install/
                            </a>
                            <p>Choose your platform:</p>
                            <ul>
                                <li><strong>Windows</strong> – WireGuard for Windows</li>
                                <li><strong>macOS</strong> – WireGuard from the Mac App Store or Homebrew</li>
                                <li><strong>Linux</strong> – Install via package manager</li>
                            </ul>
                        </div>

                        <div className="instruction_step">
                            <h4>2. Download Your Configuration File</h4>
                            <p>After installing WireGuard, download your personalized configuration file using the dropdown and button above.
                            This file will have a <code>.conf</code> extension. Do <strong>not</strong> edit the contents unless instructed.</p>
                        </div>

                        <div className="instruction_step">
                            <h4>3. Import the Configuration into WireGuard</h4>
                            <p>On Desktop (Windows/macOS/Linux):</p>
                            <ol>
                                <li>Open the WireGuard application.</li>
                                <li>Click on <strong>"Add Tunnel"</strong> or <strong>"Import Tunnel(s) from File"</strong>.</li>
                                <li>Select the configuration file you downloaded.</li>
                                <li>Once imported, it will appear in your list of tunnels.</li>
                            </ol>
                        </div>

                        <div className="instruction_step">
                            <h4>4. Activate the VPN Tunnel</h4>
                            <p>Once the configuration is imported:</p>
                            <ul>
                                <li>Click or tap the <strong>"Activate"</strong> or <strong>"Toggle"</strong> switch next to the tunnel name.</li>
                                <li>You should now be connected to the VPN.</li>
                            </ul>
                            <p>To verify, you can visit <a href="https://whatismyipaddress.com/" target="_blank" rel="noopener noreferrer">
                                https://whatismyipaddress.com/
                            </a> and confirm that your IP address has changed.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default VPN;