import './App.css';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import Home from "./pages/Home.js"
import Cocina from "./pages/Cocina.js"
import React, { useState } from "react";

function App() {

  const [background_image, setBackgroundImage] = useState("https://i.scdn.co/image/ab67616d0000b273e14f11f796cef9f9a82691a7");

  return (
    <div
      className="App"
      style={{ 
        backgroundImage: "linear-gradient( \
          rgba(0, 0, 0, 0.7), \
          rgba(0, 0, 0, 0.7) \
        ), \
        url(" + background_image + ")"
      }}
    >
      
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home setBackgroundImage={setBackgroundImage}/>} />
        <Route path="/cocina" element={<Cocina/>} />
      </Routes>
    </BrowserRouter>
    </div>
  );
}

export default App;
