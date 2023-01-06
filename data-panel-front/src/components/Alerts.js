import React, { useState, useEffect } from "react";
import "./alerts.css"

const API = "http://" + window.location.hostname + ":8000"

export default function Alerts() {

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    let random_delay = Math.random() * 900
    setTimeout(() => {
      getData();
      const interval = setInterval(() => getData(), 10000)
    },random_delay)
  }, [])

  const getData = () => {
    fetch(API + "/alerts")
    .then((response) => response.json())
    .then((data) => setAlerts(data))
    .catch((error) => console.log(error))
  }

  return (
    <>
      {
        alerts.map((alert) => {
          var style_name = "alertsCritical"
          if (alert['severity'] === "normal") style_name = "alertsNormal"
          else if (alert['severity'] === "high") style_name = "alertsHigh"
          else if (alert['severity'] === "low") style_name = "alertsLow"

          return (
            <div
              className={ "alertsCard " + (alert['severity'] === "critical" ? "criticalShadow" : "")}
            >
              <img className="alertImage" src={alert['image']} alt="cloud"/>
              <div className={style_name}>
                {alert['text']} 
              </div>
            </div>
          )
        })
      }
    </> 
  )
}