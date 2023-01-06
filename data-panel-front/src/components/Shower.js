import React, { useState, useEffect } from "react";
import "./shower.css"

const API = "http://" + window.location.hostname + ":8000"

export default function Shower() {

  const [data, setData] = useState({});
  const [api_requested, setApiRequested] = useState(false);

  useEffect(() => {
    let random_delay = Math.random() * 900
    setTimeout(() => {
      getData()
      const interval = setInterval(() => getData(), 5000)
    },random_delay)
  }, [])

  const getData = () => {
      fetch(API + "/homeware")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.log(error))
      .finally(() => setApiRequested(true))
  }

  return (
    <>
      {
        api_requested && data.status_flag && !data.status.scene_ducha.deactivate ? 
          <div
            className="showerCard"
            style={{boxShadow: "0 0.1rem 1rem rgba(" + (data.status.radiator003.on ? "255,0,0" : "0,0,0")  + ", 0.8)"}}
          >
            <div className="showerMain">
              Baño 
            </div>
            <hr className="showerDivider"/>
            <div className="showerSecond">
              {data.status.thermostat_bathroom.thermostatTemperatureAmbient} ºC
            </div>        
            <div className="showerSecond">
              {data.status.thermostat_bathroom.thermostatHumidityAmbient} %
            </div>        
          </div>
        : <></>
      }
      
    </> 
  )
}