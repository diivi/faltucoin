import React,{useState} from "react";
import {Button} from 'react-bootstrap';
import Transaction from './Transaction';
import {MILLISECONDS_PY} from '../config';

function ToggleTransactionDisplay({block}){
  const [displayTransaction, setDisplayTransaction] = useState(false);
  const {data} = block;

  const toggleDisplayTransaction =() =>{
    setDisplayTransaction(!displayTransaction)
  }

  if(displayTransaction){
    return(
      <div>
        {data.map((transaction) => (
          <div key={transaction.id}>
            <hr />
            <Transaction transaction={transaction} />
          </div>
        ))}
        <br />
        <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>Hide Details</Button>
      </div>
    )
  }

  return (
    <div>
      <br />
      <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>Show Details</Button>
    </div>
  )
}

function Block({block}){
  const {timestamp,hash}= block;
  const displayHash = hash.substring(0,15)+'...';
  const displayTimestamp = new Date(timestamp/MILLISECONDS_PY).toLocaleString();

  return(
    <div className="block">
      <div>Hash: {displayHash}</div>
      <div>Timestamp: {displayTimestamp}</div>
      <ToggleTransactionDisplay block={block}/>
    </div>
  )

}

export default Block;