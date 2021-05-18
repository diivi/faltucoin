import React,{useState, useEffect} from 'react';
import logo from '../assets/logo.png'
import {Link} from 'react-router-dom';
import { baseUrl } from "../config";

function App() {
  const [walletInfo,setWalletInfo] = useState({})

  useEffect(() => {
    fetch(`${baseUrl}/wallet/info`)
      .then(response => response.json())
      .then(json => setWalletInfo(json))
  }, [])

  const { address, balance } = walletInfo;

  return (
    <div className="App">
      <img src={logo} alt="Logo" className="logo" height="300px" width="auto" />
      <h3>Welcome to FaltuCoin</h3>
      <br/>
      <Link to="/blockchain">Blockchain</Link>
      <Link to="/transfer">Conduct a Transaction</Link>
      <br />
      <div className="wallet-info">
        <p>Address : {address}</p>
        <p>Balance : {balance}</p>
      </div>
    </div>
  );
}

export default App;
