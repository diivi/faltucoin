import React,{useState, useEffect} from 'react';
import logo from '../assets/logo.png'
import { baseUrl } from "../config";
import Blockchain from './Blockchain';
import ConductTransaction from './ConductTransaction'

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
      <br />
      <div className="wallet-info">
        <p>Address : {address}</p>
        <p>Balance : {balance}</p>
      </div>
      <br />
      <Blockchain/>
      <br/>
      <ConductTransaction/>  
    </div>
  );
}

export default App;
