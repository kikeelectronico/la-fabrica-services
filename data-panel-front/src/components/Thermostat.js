import React, { useState, useEffect } from "react";
import "./thermostat.css"

const API = "http://" + window.location.hostname + ":8000"

export default function Thermostat() {

  const [homeware, setHomeware] = useState({});
  const [api_requested, setApiRequested] = useState(false);

  useEffect(() => {
    getData();
    const interval = setInterval(() => getData(), 5000)

    return()=>clearInterval(interval)
  }, [])

  const getData = () => {
    fetch(API + "/homeware")
    .then((response) => response.json())
    .then((homeware) => setHomeware(homeware))
    .catch((error) => console.log(error))
    .finally(() => setApiRequested(true))
  }

  return (
    <>
      {
        homeware.status_flag && api_requested ?
          <>
            <div
              className="thermostatCard"
              style={{boxShadow: "0 0.1rem 1rem rgba(" + (homeware.status.radiator003.on ? "255,0,0" : "0,0,0")  + ", 0.8)"}}
            >
              <div className="thermostatTemperature">
                {homeware.status.termos.thermostatTemperatureAmbient} ºC
              </div>
            </div>
          </>
          : <></>
      }
      
      
    </> 
  )
}