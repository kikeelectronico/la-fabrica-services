import React from "react";
import "./notathome.css"

export default function NotAtHome(props) {
  return (
    <>
      {
        props.api_requested && props.homeware.status_flag && props.homeware.status.switch_at_home.desactivate ? 
          <div className="notAtHomeCard">
            <div className="notAtHomeMain">
              Interruptor de presencia desactivado 
            </div>    
          </div>
        : <></>
      }
      
    </> 
  )
}