import React, { useState, useEffect } from "react";
  import "./launches.css"
  
  const API = "http://" + window.location.hostname + ":8000"
  
  export default function Launches() {
  
    const [data, setData] = useState({launches_flag: false, fail_to_update: true});
    const [uv_alert, setUvAlert] = useState("0, 0, 0");
    const [api_requested, setApiRequested] = useState(false);
  
    useEffect(() => {
      getData()
      const interval = setInterval(() => getData(), 10000)
  
      return()=>clearInterval(interval)
    }, [])
  
    const getData = () => {
        fetch(API + "/launches")
        .then((response) => response.json())
        .then((data) => setData(data))
        .catch((error) => console.log(error))
        .finally(() => setApiRequested(true))
    }
  
    useEffect(() => {
      evaluateAlerts()
    }, [data])
  
    const evaluateAlerts = () => {
      /*if (data.weather_flag) {
        var uv = data.weather.current.uv
        if (uv <= 2) setUvAlert("0,0,0")
        else if (uv <= 5) setUvAlert("255,255,0")
        else if (uv <= 7) setUvAlert("255,126,0")
        else if (uv <= 10) setUvAlert("255,0,0")
        else setUvAlert("126,0,35")
      }*/
    }

    const getLaunchTime = (launch) => {
      if (launch) {
        return launch.net.split("T")[1].split(":")
      } else {
        setData({fail_to_update: true})
        return ""
      }
    }

    const getMisionName = (launch) => {
      if (launch) {
        return launch.mission.name.length > 30 ? launch.mission.name.substring(0, 30) + "..." : launch.mission.name
      } else {
        setData({fail_to_update: true})
        return ""
      }
    }
  
    return (
      <>
        {
          !data.fail_to_update && data.launches_flag && api_requested ? 
            
              data.launches.map(launch => {

                {
                  launch !== undefined ?    
                    <div
                      className="launchesCard"
                      style={{
                        boxShadow: "0 0.1rem 1rem rgba(" + uv_alert  + ", 0.8)"
                      }}
                    >
                      <div className="launchesName">
                        {getMisionName()}
                      </div>
                      <hr className="launchDivider"/>
                      <div className="launchesNet">
                        {getLaunchTime()[0]} : {getLaunchTime()[1]}
                      </div>
                    </div>
                  :
                    <></>
                }

                
              })
            
          : <></>
        }
        {
          data.fail_to_update && api_requested ? 
            <div className="weatherCard" >            
              <div className="launchesFail">
                Fallo al cargar datos de lanzamientos
              </div>
            </div>
          : <></>
            
        }
        
      </> 
    )
  }