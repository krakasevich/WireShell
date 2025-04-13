import React from "react"
import { useNavigate } from "react-router-dom";
import './styles/Homepage.css'

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
          <h1 className='main_headline'>SecureNet — network security for everyone</h1>
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
          <h2>Why Choose SecureNet?</h2>
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
              <h3 >Security</h3>
              <p>Advanced encryption and security protocols to keep your data safe and private.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  export default HomePage;