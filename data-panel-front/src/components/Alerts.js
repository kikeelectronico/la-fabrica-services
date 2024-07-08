import React from "react";
import "./alerts.css"

export default function Alerts(props) {

  const assert = () => {
    const condition = props.alert.assert
    if (condition.comparator === "<")
      return props.data.status[condition.device_id][condition.param] < condition.value
    if (condition.comparator === "=")
      return props.data.status[condition.device_id][condition.param] = condition.value
    if (condition.comparator === ">")
      return props.data.status[condition.device_id][condition.param] > condition.value
    return false
  }

  const getStyle = () => {
    var style_name = "alertsCritical"
    if (props.alert['severity'] === "normal") style_name = "alertsNormal"
    else if (props.alert['severity'] === "high") style_name = "alertsHigh"
    else if (props.alert['severity'] === "low") style_name = "alertsLow"
    return style_name
  }

  return (
    <>
    {
      assert() ?
        <div
          className={ "alertsCard " + (props.alert['severity'] === "critical" ? "criticalShadow" : "")}
        >
          <img className="alertImage" src={props.alert['image']} alt="cloud"/>
          <div className={getStyle()}>
            {props.alert['text']} 
          </div>
        </div>
      : <></>
    }
    </>
  )
}