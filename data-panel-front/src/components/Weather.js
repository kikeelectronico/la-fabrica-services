import React, { useState, useEffect } from "react";
import "./weather.css"

const API = "http://" + window.location.hostname + ":8000"

export default function Weather() {

  const [data, setData] = useState({weather_flag: false, fail_to_update: true});
  const [uv_alert, setUvAlert] = useState("255, 0, 0");
  const [api_requested, setApiRequested] = useState(false);

  useEffect(() => {
    getData()
    const interval = setInterval(() => getData(), 60000)

    return()=>clearInterval(interval)
  }, [])

  const getData = () => {
      fetch(API + "/weather")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.log(error))
      .finally(() => setApiRequested(true))
  }

  useEffect(() => {
    evaluateAlerts()
  }, [data])

  const evaluateAlerts = () => {
    if (data.weather_flag) {
      var uv = data.weather.current.uv
      if (uv <= 2) setUvAlert("0,0,0")
      else if (uv <= 5) setUvAlert("255,255,0")
      else if (uv <= 7) setUvAlert("255,126,0")
      else if (uv <= 10) setUvAlert("255,0,0")
      else setUvAlert("126,0,35")
    }
  }

  return (
    <>
      {
        !data.fail_to_update && data.weather_flag && api_requested ? 
          <div
            className="weatherCard"
            style={{
              boxShadow: "0 0.1rem 1rem rgba(" + uv_alert  + ", 0.8)"
            }}
          >
            <img className="weatherIcon" alt="f" src={data.weather.current.condition.icon}/>
            <div className="weatherTemperature">
              {data.weather.current.temp_c} ºC - {data.weather.current.feelslike_c} ºC
            </div>
            <div className="weatherUltraviolet">
              UV {data.weather.current.uv}
            </div>
            <div className="weatherWind">
              {data.weather.current.wind_kph} km/h - {data.weather.current.wind_dir}
            </div>
          </div>
        : <></>
      }
      {
        data.fail_to_update && api_requested ? 
          <div className="weatherCard" >            
            <div className="weatherFail">
              Fallo al cargar datos meteorológicos
            </div>
          </div>
        : <></>
          
      }
      
    </> 
  )
}