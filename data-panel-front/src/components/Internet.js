import React, { useState, useEffect } from "react";
import "./internet.css"

const API = "http://" + window.location.hostname + ":8000"

export default function Internet() {

  const [internet, setInternet] = useState(false);

  useEffect(() => {
    checkInternet();
    const interval = setInterval(() => checkInternet(), 10000)

    return()=>clearInterval(interval)
  }, [])

  const checkInternet = () => {
    fetch(API + "/internet")
    .then((response) => response.json())
    .then((data) => setInternet(data))
    .catch((error) => console.log(error))
  }

  return (
    <>      
      {
        !internet ?
          <>
            <div className="internetCard">
              <div className="internetFail">
                Sin conexión a Internet 
              </div>
            </div>
          </>
          : <></>
      }
    </> 
  )
}