import React, { useState, useEffect } from "react";
import "./air.css"

const API = process.env.REACT_APP_DATA_PANEL_API_URL

export default function Air() {

  const [data, setData] = useState({weather_flag: false});
  const [aqi_alert, setAqiAlert] = useState("255, 0, 0");

  useEffect(() => {
    let random_delay = Math.random() * 900
    setTimeout(() => {
      getData()
      const interval = setInterval(() => getData(), 60000)
    },random_delay)
  }, [])

  const getData = () => {
      fetch(API + "/weather")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.log(error))
  }

  useEffect(() => {
    evaluateAlerts()
  }, [data])

  const evaluateAlerts = () => {
    if (data.weather_flag) {
      var aqi = data.weather.current.air_quality['us-epa-index']
      if (aqi < 50) setAqiAlert("0,0,0")
      else if (aqi < 100) setAqiAlert("255,255,0")
      else if (aqi < 150) setAqiAlert("255,126,0")
      else if (aqi < 200) setAqiAlert("255,0,0")
      else if (aqi < 300) setAqiAlert("143,63,151")
      else setAqiAlert("126,0,35")
    }
  }

  return (
    <>
      {
        !data.fail_to_update && data.weather_flag ? 
          <div
            className="airCard"
            style={{
              boxShadow: "0 0.1rem 1rem rgba(" + aqi_alert  + ", 0.8)"
            }}
          >
            <div className="airMain">
              AQI {data.weather.current.air_quality['us-epa-index']}
            </div>
            <hr className="airDivider"/>
            <div className="airThird">
              CO: {Math.round(data.weather.current.air_quality.co)} ppm
            </div>
            <div className="airThird">
              NO2: {Math.round(data.weather.current.air_quality.no2*100)/100} ppm
            </div>
            <div className="airThird">
              O3: {Math.round(data.weather.current.air_quality.o3*100)/100} ppm
            </div>
            <div className="airThird">
              SO2: {Math.round(data.weather.current.air_quality.so2*100)/100} ppm
            </div>
            
          </div>
        : <></>
      }
      
    </> 
  )
}