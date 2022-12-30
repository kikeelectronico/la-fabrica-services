import "./cocina.css"
import Clock from "../components/Clock"
import Internet from "../components/Internet"
import Thermostat from "../components/Thermostat"
import Power from "../components/Power"
import Alerts from "../components/Alerts"

export default function Cocina() {
  return (
    <div className="cocinaPage">
        <div className="title">
          <h1>La fábrica</h1>
        </div>
        <Clock/>
        <Internet/>
        <Power/>
        <Thermostat/>
        <Alerts/>
    </div>
  )
}