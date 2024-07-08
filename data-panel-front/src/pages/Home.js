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

export default function Home(props) {

  const [internet, setInternet] = useState(null)
  const [playing_spotify, setPlayingSpotify] = useState(false);

  useEffect(() => {
    const sse = new EventSource(API + "/stream", { withCredentials: false });
    const events = (event) => {
      if (event.type === "internet") setInternet(event.data)
    }
    sse.onmessage = event => events(JSON.parse(event.data));
    sse.onerror = () => {
      sse.close();
    }
    return () => {
      sse.close();
    };
  }, [])

  return (
    <div className="homePage">
        <div className="title">
          <h1>La fábrica</h1>
        </div>
        <div className={"homeCardsContainer" + (playing_spotify ? " homeCardsContainerPlaying" : " homeCardsContainerNotPlaying")}>
          <Clock/>
          { internet ? <Internet data={internet}/> : <></> }
          {/* <Thermostat homeware={homeware} api_requested={api_requested}/>
          <Weather/>
          <Air/>
          <Power homeware={homeware} api_requested={api_requested}/>
          <Alerts/>
          <Launches/>
          <Shower homeware={homeware} api_requested={api_requested}/>
          <Bedroom homeware={homeware} api_requested={api_requested}/>
          <NotAtHome homeware={homeware} api_requested={api_requested}/>
          <Spotify setPlayingSpotify={setPlayingSpotify} setBackgroundImage={props.setBackgroundImage} />
          {
            scenes_to_show.map(scene => {
              return <LightingScene homeware={homeware} api_requested={api_requested} scene={scene}/>
            })
          } */}
        </div>
    </div>
  )
}