import React from "react";
import "./thermostat.css"

export default function Thermostat(props) {

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
            </div>
          </>
          : <></>
      }
      
      
    </> 
  )
}