import React from "react";
import "./weather.css"

export default function Weather(props) {

  const shadowColor = () => {
    var uv = props.data.forecast.current.uv
    if (uv <= 2) return "0,0,0"
    else if (uv <= 5) return "255,255,0"
    else if (uv <= 7) return "255,126,0"
    else if (uv <= 10) return "255,0,0"
    else return "126,0,35"
  }

  return (
    <>
      {
        props.data ? 
          <div
            className="weatherCard"
            style={{
              boxShadow: "0 0.1rem 1rem rgba(" + shadowColor()  + ", 0.8)"
            }}
          >
            <img className="weatherIcon" alt="f" src={props.data.forecast.current.condition.icon}/>
            <div className="weatherTemperature">
              {props.data.forecast.current.temp_c} ºC - {props.data.forecast.current.feelslike_c} ºC
            </div>
            <div className="weatherUltraviolet">
              UV {props.data.forecast.current.uv}
            </div>
            <div className="weatherWind">
              {props.data.forecast.current.wind_kph} km/h - {props.data.forecast.current.wind_dir}
            </div>
          </div>
        : 
          <div className="weatherCard" >            
            <div className="weatherFail">
              Fallo al cargar datos meteorológicos
            </div>
          </div>          
      }
      
    </> 
  )
}