import React from "react";
import "./thermostat.css"

export default function Thermostat(props) {

  const thermostatMode = () => {
    var mode = props.homeware.status.thermostat_livingroom.thermostatMode
    if (mode == "heat") return "Calor"
    if (mode == "cool") return "Frio"
    if (mode == "off") return "Apagado"
  }

  return (
    <>
      {
        props.homeware.status_flag && props.api_requested ?
          <>
            <div
              className="thermostatCard"
              style={{boxShadow: "0 0.1rem 1rem rgba(" + (props.homeware.status.radiator001.on ? "255,0,0" : "0,0,0")  + ", 0.8)"}}
            >
              <div className="thermostatTemperature">
                {props.homeware.status.thermostat_livingroom.thermostatTemperatureAmbient} ºC
              </div>
              <hr className="thermostatDivider"/>
              <div className="thermostatStatus">
                {thermostatMode()}
              </div>      
            </div>
          </>
          : <></>
      }
      
      
    </> 
  )
}