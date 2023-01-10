import React from "react";
import "./bedroom.css"


export default function Bedroom(props) {

  return (
    <>
      {
        props.api_requested && props.homeware.status_flag && 
        ( props.homeware.status.light001.on || props.homeware.status.rgb003.on ) ? 
          <div className="bedroomCard">
            <div className="bedroomMain">
              Dormitorio 
            </div>    
          </div>
        : <></>
      }
      
    </> 
  )
}