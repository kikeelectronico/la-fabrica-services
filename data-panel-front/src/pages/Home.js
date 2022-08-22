import "./home.css"
import Clock from "../components/Clock"
import Internet from "../components/Internet"
import Spotify from "../components/Spotify"
import Thermostat from "../components/Thermostat"
import Power from "../components/Power"
import Weather from "../components/Weather"
import Air from "../components/Air"
import Alerts from "../components/Alerts"
import Launches from "../components/Launches"

export default function Home() {
  return (
    <div className="homePage">
        <div className="title">
          <h1>La fábrica</h1>
        </div>
        <Clock/>
        <Internet/>
        <Thermostat/>
        <Weather/>
        <Air/>
        <Power/>
        <Alerts/>
        <Launches/>
        <Spotify/>
    </div>
  )
}