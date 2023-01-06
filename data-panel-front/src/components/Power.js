import React, { useState, useEffect } from "react";
import "./power.css"

const API = "http://" + window.location.hostname + ":8000"

export default function Power() {

  const [homeware, setHomeware] = useState({status_flag: false});
  const [api_requested, setApiRequested] = useState(false);

  useEffect(() => {
    getData();
    const interval = setInterval(() => getData(), 2000)

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
              className="powerCard"
              style={{boxShadow: "0 0.1rem 1rem rgba(" + (homeware.status.current001.brightness > 90 ? "255,0,0" : "0,0,0")  + ", 0.8)"}}
            >
              <div className="powerTemperature">
                {homeware.status.current001.brightness * 35} W
              </div>
            </div>
          </>
          : <></>
      }
      
      {
        !homeware.status_flag && api_requested ?
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