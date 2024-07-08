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
  }
]

export default function Home(props) {

  const [internet, setInternet] = useState(null)
  const [home, setHome] = useState(null)
  const [weather, setWeather] = useState(null)
  const [launches, setLaunches] = useState(null)
  const [spotify, setSpotify] = useState(null)
  const [spotify_playing, setSpotifyPlaying] = useState(false);

  useEffect(() => {
    const sse = new EventSource(API + "/stream", { withCredentials: false });
    sse.onmessage = e => {
      let event = JSON.parse(e.data)
      if (event.type === "internet") setInternet(event.data)
      else if (event.type === "home") setHome(event.data)
      else if (event.type === "weather") setWeather(event.data)
      else if (event.type === "launches") setLaunches(event.data)
      else if (event.type === "spotify") setSpotify(event.data)
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
  }, [props, spotify])

  return (
    <div className="homePage">
        <div className="title">
          <h1>La fábrica</h1>
        </div>
        <div className={"homeCardsContainer" + (spotify_playing ? " homeCardsContainerPlaying" : " homeCardsContainerNotPlaying")}>
          <Clock/>
          { internet ? <Internet data={internet}/> : <></> }
          { home ? <Thermostat data={home}/> : <></> }
          { weather ? <Weather data={weather}/> : <></> }
          { weather ? <Air data={weather}/> : <></> }
          { home ? <Power data={home}/> : <></> }
          { home ? <Shower data={home}/> : <></> }
          { home ? <Bedroom data={home}/> : <></> }
          { home ? <NotAtHome data={home}/> : <></> }
          { launches ? <Launches data={launches}/> : <></> }
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
                return <></>
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