import React, { useState, useEffect } from "react";
import "./launches.css"

const API = process.env.REACT_APP_DATA_PANEL_API_URL

export default function Launches() {

  const [launches, setLaunches] = useState({launches_flag: false, fail_to_update: false});
  const [api_requested, setApiRequested] = useState(false);

  useEffect(() => {
    let random_delay = Math.random() * 900
    setTimeout(() => {
      getData()
      const interval = setInterval(() => getData(), 10000)
    },random_delay)
  }, [])

  const getData = () => {
      fetch(API + "/launches")
      .then((response) => response.json())
      .then((data) => setLaunches(data))
      .catch((error) => console.log(error))
      .finally(() => setApiRequested(true))
  }

  const getLaunchTime = (launch) => {
    return launch.net.split("T")[1].split(":")
  }

  const getMisionName = (launch) => {
    let name = launch.name.split(" | ")[0]
    return name > 30 ? name.substring(0, 30) + "..." : name
  }

  return (
    <>
      {
        !launches.fail_to_update && launches.launches_flag && api_requested ? 
          
          launches.launches.map(launch => {
            return (
                  <div className="launchesCard">
                    <div className="launchesName">
                      {getMisionName(launch)}
                    </div>
                    <hr className="launchDivider"/>
                    <div className="launchesNet">
                      {getLaunchTime(launch)[0]} : {getLaunchTime(launch)[1]}
                    </div>
                  </div>
              )                
            })
          
        : <></>
      }
      {
        launches.fail_to_update && api_requested ? 
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