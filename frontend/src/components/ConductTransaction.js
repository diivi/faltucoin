import React, { useState,useEffect } from "react";
import {FormGroup, FormControl, Button} from 'react-bootstrap';
import {baseUrl} from '../config';
import { Link } from "react-router-dom";


function ConductTransaction(){
  const [amount, setAmount] = useState(0)
  const [recipient, setRecipient] = useState('')
  const [knownAddresses, setKnownAddresses] = useState([])

  useEffect(() => {
    fetch(`${baseUrl}/addresses`)
      .then(res=>res.json())
      .then(json=> setKnownAddresses(json));
  }, [])

  const updateRecipient = event =>{
    setRecipient(event.target.value);
  }

  const updateAmount = (event) => {
    setAmount(Number(event.target.value));
  };

  const submitTransaction =()=>{
    fetch(`${baseUrl}/wallet/transact`,{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({recipient,amount})
    }
    ).then(res => res.json())
     .then(json => {
       console.log('submitTransaction json', json);
       alert('Success!')
     })

  }

  return (
    <div className="transfer">
      <Link to="/">Home</Link>
      <hr />
      <h3>Conduct a Transaction</h3>
      <br />
      <FormGroup>
        <FormControl
          input="text"
          placeholder="recipient"
          value={recipient}
          onChange={updateRecipient}
        />
        <FormControl
          input="number"
          placeholder="amount"
          value={amount}
          onChange={updateAmount}
        />
      </FormGroup>
      <div>
        <Button variant="danger" onClick={submitTransaction}>
          Submit
        </Button>
      </div>
      <br/>
      <h4>
        Known Addresses
      </h4>
      <div>
        {
          knownAddresses.map((knownAddress,i) => {
            return(
            <span key={knownAddress}>
              <u> {knownAddress}</u>{i !== knownAddresses.length-1 ?', ':''}
            </span>
          )}) 
        }
      </div>
    </div>
  );
}

export default ConductTransaction