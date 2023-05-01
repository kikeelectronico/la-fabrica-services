import React, { useState, useEffect } from "react";
import ProgressBar from 'react-bootstrap/ProgressBar';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./spotify.css"

const API = process.env.REACT_APP_DATA_PANEL_API_URL
var loading = false

export default function Spotify(props) {

  const [spotify, setSpotify] = useState({});
  const [api_requested, setApiRequested] = useState(false);

  useEffect(() => {
    let random_delay = Math.random() * 900
    setTimeout(() => {
      getSpotify()
      const interval = setInterval(() => getSpotify(), 500)
    },random_delay)
  }, [])

  const getSpotify = () => {
    if (!loading) {
      loading = true
      fetch(API + "/spotify")
      .then((response) => response.json())
      .then((data) => {
        setSpotify(data)
        props.setPlayingSpotify(data.playing)
        let background_position = "0% " + data.image_position*10 + "%"
        props.setBackgroundImage({url: data.image, position: background_position})
      })
      .catch((error) => console.log(error))
      .finally(() => setApiRequested(true))
      setTimeout(() => {loading = false}, 2000)
    }
    
  }

  return (
    <>
      {
        spotify.playing && api_requested ? 
          <>
          <div
            className="spotifyCard"
          >
            <div className="spotifyData">
              <div className="spotifyTitle">
                {spotify.track_name.length > 60 ? spotify.track_name.substring(0, 60) + "..." : spotify.track_name}
              </div>
              <hr className="spotifyArtistsSeparator"/>
              <div className="spotifyArtist">
                {spotify.artists.length > 40 ? spotify.artists.substring(0, 40) + "..." : spotify.artists}
              </div>
              <hr className="spotifyArtistsSeparator"/>
              <div className="spotifyDevice">
                {spotify.device} ({spotify.volume})
              </div>
            </div>

            <div
              className="spotifyImageCard"
              style={{ 
                backgroundImage:  "url(" + spotify.image + ")"
              }}
            >
            </div>

            <div className="spotifyProgressBar">
              <ProgressBar animated variant="info" now={spotify.time} max={spotify.duration} />
            </div>
            
            
          </div>

          
          </>
        : <></>
      }
      {
        spotify.quota_exceeded && api_requested ? 
          <div className="spotifyCard">
            <div className="spotifyTitle">
              Excedida la cuota de Spotify WEB API
            </div>            
          </div>
        : <></>
      }
    </> 
  )
}