import React, { useState, useEffect } from 'react';
import {baseUrl} from '../config';
import Block from './Block';

function Blockchain(){
  const [blockchain, setBlockchain] = useState([]);

  useEffect(() => {
    fetch(`${baseUrl}/blockchain`)
    .then( response => response.json())
    .then(json => setBlockchain(json))
  }, [])

  return(
    <div className="blockchain">
      <h3>Blockchain</h3>
      <div>
        {blockchain.map(block => (
          <Block key={block.hash} block={block}/>
        ))}
      </div>
    </div>
  )
}

export default Blockchain;