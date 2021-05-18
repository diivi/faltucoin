import React from "react";
import {MILLISECONDS_PY} from '../config';

function Block({block}){
  const {timestamp,hash ,data }= block;
  const displayHash = hash.substring(0,15)+'...';
  const displayTimestamp = new Date(timestamp/MILLISECONDS_PY).toLocaleString();

  return(
    <div className="block">
      <div>Hash: {displayHash}</div>
      <div>Timestamp: {displayTimestamp}</div>
      <div>{JSON.stringify(data)}</div>
    </div>
  )

}

export default Block;