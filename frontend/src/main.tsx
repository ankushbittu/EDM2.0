import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./App.css"; // or index.css if you prefer

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

