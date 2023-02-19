import React from "react";
import "./shower.css"

export default function Shower(props) {
  return (
    <>
      {
        props.api_requested && props.homeware.status_flag && !props.homeware.status.scene_ducha.deactivate ? 
          <div
            className="showerCard"
            style={{boxShadow: "0 0.1rem 1rem rgba(" + (props.homeware.status.radiator003.on ? "255,0,0" : "0,0,0")  + ", 0.8)"}}
          >
            <div className="showerMain">
              Baño 
            </div>
            <hr className="showerDivider"/>
            <div className="showerSecond">
              {props.homeware.status.thermostat_bathroom.thermostatTemperatureAmbient} ºC
            </div>        
            <div className="showerSecond">
              {props.homeware.status.thermostat_bathroom.thermostatHumidityAmbient} %
            </div>        
          </div>
        : <></>
      }
      
    </> 
  )
}