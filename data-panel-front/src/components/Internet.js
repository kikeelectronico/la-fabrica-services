import React, { useState, useEffect } from "react";
import "./internet.css"

const API = "http://api.data-panel.lafabrica"

export default function Internet() {

  const [internet, setInternet] = useState(false);

  useEffect(() => {
    let random_delay = Math.random() * 900
    setTimeout(() => {
      checkInternet();
      const interval = setInterval(() => checkInternet(), 10000)
    },random_delay)
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