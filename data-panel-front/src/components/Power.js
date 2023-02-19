import React from "react";
import "./power.css"

export default function Power(props) {
  return (
    <>
      {
        props.homeware.status_flag && props.api_requested ?
          <>
            <div
              className="powerCard"
              style={{boxShadow: "0 0.1rem 1rem rgba(" + (props.homeware.status.current001.brightness > 90 ? "255,0,0" : "0,0,0")  + ", 0.8)"}}
            >
              <div className="powerTemperature">
                {props.homeware.status.current001.brightness * 35} W
              </div>
            </div>
          </>
          : <></>
      }
      
      {
        !props.homeware.status_flag && props.api_requested ?
          <>
            <div className="powerCard">
              <div className="powerFail">
                Fallo al cargar datos de estado de Homeware 
              </div>
            </div>
          </>
          : <></>
      }
    </> 
  )
}