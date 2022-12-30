import React, { useState, useEffect } from "react";
import ProgressBar from 'react-bootstrap/ProgressBar';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./spotify.css"

const API = "http://" + window.location.hostname + ":8000"
var loading = false

export default function Spotify(props) {

  const [playing, setPlaying] = useState({});
  const [api_requested, setApiRequested] = useState(false);

  useEffect(() => {
    getSpotify()
    const interval = setInterval(() => getSpotify(), 1000)

    return()=>clearInterval(interval)
  }, [])

  const getSpotify = () => {
    if (!loading) {
      loading = true
      fetch(API + "/spotify")
      .then((response) => response.json())
      .then((spotify) => {setPlaying(spotify); props.setBackgroundImage(spotify.image)})
      .catch((error) => console.log(error))
      .finally(() => setApiRequested(true))
      setTimeout(() => {loading = false}, 1000)
    }
    
  }

  return (
    <>
      {
        playing.playing && api_requested ? 
          <>
          <div
            className="spotifyCard"
          >
            <div className="spotifyData">
              <div className="spotifyTitle">
                {playing.track_name.length > 60 ? playing.track_name.substring(0, 60) + "..." : playing.track_name}
              </div>
              <hr className="spotifyArtistsSeparator"/>
              <div className="spotifyArtist">
                {playing.artists.length > 40 ? playing.artists.substring(0, 40) + "..." : playing.artists}
              </div>
              <hr className="spotifyArtistsSeparator"/>
              <div className="spotifyDevice">
                {playing.device} ({playing.volume})
              </div>
            </div>

            <div
              className="spotifyImageCard"
              style={{ 
                backgroundImage:  "url(" + playing.image + ")"
              }}
            >
            </div>

            <div className="spotifyProgressBar">
              <ProgressBar animated variant="info" now={playing.time} max={playing.duration} />
            </div>
            
            
          </div>

          
          </>
        : <></>
      }
      {
        playing.quota_exceeded && api_requested ? 
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