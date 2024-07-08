import React from "react";
import "./alerts.css"

export default function Alerts(props) {

  const getStyle = () => {
    var style_name = "alertsCritical"
    if (props.alert['severity'] === "normal") style_name = "alertsNormal"
    else if (props.alert['severity'] === "high") style_name = "alertsHigh"
    else if (props.alert['severity'] === "low") style_name = "alertsLow"
    return style_name
  }

  return (
    <div
      className={ "alertsCard " + (props.alert['severity'] === "critical" ? "criticalShadow" : "")}
    >
      <img className="alertImage" src={props.alert['image']} alt="cloud"/>
      <div className={getStyle()}>
        {props.alert['text']} 
      </div>
    </div>
  )
}