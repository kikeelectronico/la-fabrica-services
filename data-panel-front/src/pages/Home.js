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
import Shower from "../components/Shower"
import Bedroom from "../components/Bedroom"
import NotAtHome from "../components/NotAtHome"
import LightingScene from "../components/LightingScene"
import React, { useState, useEffect } from "react";

const API = process.env.REACT_APP_DATA_PANEL_API_URL

const scenes_to_show = [
  {
    "name": "Luz tenue",
    "id": "scene_dim"
  }
]

const home_alerts = [
  {
    "text": "Humedad baja",
    "severity": "normal",
    "image": "drops.png",
    "assert": {
      "device_id": "thermostat_livingroom",
      "param": "thermostatHumidityAmbient",
      "value": 30,
      "comparator": "<"
    }
  },
  {
    "text": "Humedad alta",
    "severity": "normal",
    "image": "drops.png",
    "assert": {
      "device_id": "thermostat_livingroom",
      "param": "thermostatHumidityAmbient",
      "value": 55,
      "comparator": ">"
    }
  },
  {
    "text": "Ventana abierta",
    "severity": "normal",
    "image": "window.png",
    "assert": {
      "device_id": "e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4",
      "param": "openPercent",
      "value": 100,
      "comparator": "="
    }
  }
]

export default function Home(props) {

  const [internet, setInternet] = useState(null)
  const [home, setHome] = useState(null)
  const [home_flag, setHomeFlag] = useState(null)
  const [weather, setWeather] = useState(null)
  const [weather_flag, setWeatherFlag] = useState(null)
  const [launches, setLaunches] = useState(null)
  const [launches_flag, setLaunchesFlag] = useState(null)
  const [spotify, setSpotify] = useState(null)
  const [spotify_playing, setSpotifyPlaying] = useState(false);

  useEffect(() => {
    const sse = new EventSource(API + "/stream", { withCredentials: false });
    sse.onmessage = e => {
      let event = JSON.parse(e.data)
      if (event.type === "internet") {setInternet(event.data)}
      else if (event.type === "home") {setHome(event.data); setHomeFlag(event.flags)}
      else if (event.type === "weather") {setWeather(event.data); setWeatherFlag(event.flags)}
      else if (event.type === "launches") {setLaunches(event.data); setLaunchesFlag(event.flags)}
      else if (event.type === "spotify") {setSpotify(event.data)}
    };
    sse.onerror = () => {
      sse.close();
    }
    return () => {
      sse.close();
    };
  }, [])

  useEffect(() => {
    if (spotify) {
      setSpotifyPlaying(spotify.playing.playing)
      props.setBackgroundImage(
        {
          url: spotify.playing.image,
          position: "0% " + spotify.playing.image_position*10 + "%"
        }
      )
    }
  }, [props.setBackgroundImage, spotify])

  return (
    <div className="homePage">
        <div className="title">
          <h1>La fábrica</h1>
        </div>
        <div className={"homeCardsContainer" + (spotify_playing ? " homeCardsContainerPlaying" : " homeCardsContainerNotPlaying")}>
          <Clock/>
          { internet ? <Internet data={internet}/> : <></> }
          { home && home_flag ? <Thermostat data={home}/> : <></> }
          { weather && weather_flag ? <Weather data={weather}/> : <></> }
          { weather && weather_flag ? <Air data={weather}/> : <></> }
          { home && home_flag ? <Power data={home}/> : <></> }
          { home && home_flag ? <Shower data={home}/> : <></> }
          { home && home_flag ? <Bedroom data={home}/> : <></> }
          { home && home_flag ? <NotAtHome data={home}/> : <></> }
          { launches && launches_flag ? <Launches data={launches}/> : <></> }
          { spotify ? <Spotify data={spotify}/> : <></> }
          { 
            home ? 
              scenes_to_show.map((scene, index) => {
                return <LightingScene data={home} scene={scene} key={index}/>
              })
            : <></>
          }
          { 
            home ? 
              home_alerts.map((alert, index) => {
                const condition = alert.assert
                if ( (condition.comparator === "<" && home.status[condition.device_id][condition.param] < condition.value)
                || (condition.comparator === "=" && home.status[condition.device_id][condition.param] === condition.value)
                || (condition.comparator === ">" && home.status[condition.device_id][condition.param] > condition.value) )
                  return <Alerts alert={alert} key={index}/>
              })
            : <></>
          }
          {/*
          <Alerts/>
          */}
        </div>
    </div>
  )
}