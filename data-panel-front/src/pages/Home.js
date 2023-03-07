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
import React, { useState, useEffect } from "react";

const API = process.env.REACT_APP_DATA_PANEL_API_URL

export default function Home(props) {

  const [homeware, setHomeware] = useState({status_flag: false});
  const [api_requested, setApiRequested] = useState(false);

  useEffect(() => {
    let random_delay = Math.random() * 900
    setTimeout(() => {
      getHomeware()
      const interval = setInterval(() => getHomeware(), 2000)
    },random_delay)
  }, [])

  const getHomeware = () => {
    fetch(API + "/homeware")
    .then((response) => response.json())
    .then((homeware) => setHomeware(homeware))
    .catch((error) => console.log(error))
    .finally(() => setApiRequested(true))
  }


  return (
    <div className="homePage">
        <div className="title">
          <h1>La fábrica</h1>
        </div>
        <Clock/>
        <Internet/>
        <Thermostat homeware={homeware} api_requested={api_requested}/>
        <Weather/>
        <Air/>
        <Power homeware={homeware} api_requested={api_requested}/>
        <Alerts/>
        <Launches/>
        <Shower homeware={homeware} api_requested={api_requested}/>
        <Bedroom homeware={homeware} api_requested={api_requested}/>
        <NotAtHome homeware={homeware} api_requested={api_requested}/>
        <Spotify setBackgroundImage={props.setBackgroundImage} />
    </div>
  )
}