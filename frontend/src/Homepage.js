import React from "react"
import { useNavigate } from "react-router-dom";
import './styles/Homepage.css'
import SwedenFlag from './images/Sweden.svg'
import UKFlag from './images/United_Kingdom.png'
import SingaporeFlag from './images/Singapore.png'
import ItalyFlag from './images/Italy.svg'
import PortugalFlag from './images/Portugal.svg'
import BrazilFlag from './images/Brazil.png'

function HomePage() {
    const navigate = useNavigate();
  
    const handleGetStarted = () => {
      navigate("/registration");
    };

    const handleLogin = () => {
      navigate("/login")
    }
  
    return (
      <div className='home_page'>
        <div className='home_info'>
          <h1 className='main_headline'>Get ready-to-use WireGuard config files for multiple regions</h1>
          <p className='headline'>
            Browse safely and anonymously with our high-speed VPN service.
            Protect your data across all your devices with just one click.
          </p>
          <div className="btns_authentication">
            <button className="btn_get_started" onClick={handleGetStarted}>Get Started</button>
            <button className="btn_login" onClick={handleLogin}>Login</button>
          </div>
          
        </div>

        <div className="choose_secureNet_section">
          <h2>Why Choose WireShell?</h2>
          <div className='inf_benefits'>          
            <div className='point'>
              <h3 >Lightning Speed</h3>
              <p>Experience blazing-fast connections with our optimized global network infrastructure.</p>
            </div>
            <div className='point'>
              <h3>Ease of Use</h3>
              <p>Simple, intuitive interface that works seamlessly across all your devices.</p>
            </div>
            <div className='point'>
              <h3 >Simple Setup</h3>
              <p>No complex setup. Just download, import, and connect — it's that easy.</p>
            </div>
          </div>
        </div>

        <div className="regions_section">
          <h2>Available Regions</h2>
          <div className="regions_grid">
            <div className="region_card">
              <img src={SwedenFlag} alt="Sweden" className="region_image" />
              <h3>Sweden</h3>
              <p>Stockholm</p>
            </div>
            <div className="region_card">
              <img src={UKFlag} alt="United Kingdom" className="region_image" />
              <h3>United Kingdom</h3>
              <p>London</p>
            </div>
            <div className="region_card">
              <img src={SingaporeFlag} alt="Singapore" className="region_image" />
              <h3>Singapore</h3>
              <p>Singapore</p>
            </div>
            <div className="region_card">
              <img src={ItalyFlag} alt="Italy" className="region_image" />
              <h3>Italy</h3>
              <p>Milan</p>
            </div>
            <div className="region_card">
              <img src={PortugalFlag} alt="Portugal" className="region_image" />
              <h3>Portugal</h3>
              <p>Lisbon</p>
            </div>
            <div className="region_card">
              <img src={BrazilFlag} alt="Brazil" className="region_image" />
              <h3>Brazil</h3>
              <p>Sao Paulo</p>
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  export default HomePage;