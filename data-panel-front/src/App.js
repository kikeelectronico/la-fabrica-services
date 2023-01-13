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

  const [background_image, setBackgroundImage] = useState("./black.png");
  
  return (
    <div
      className="App"
      style={{ 
        backgroundImage: "url(" + (background_image ? background_image : "./black.png" )  + ")"
      }}
    >
      <div className="appOverlay"></div>
      <div className="appContent">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home setBackgroundImage={setBackgroundImage}/>} />
            <Route path="/cocina" element={<Cocina/>} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
