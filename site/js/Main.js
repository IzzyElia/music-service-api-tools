import { initializeSpotify } from "./Spotify.js";

let config;



window.addEventListener("DOMContentLoaded", () => {
    fetch('../config.json')
    .then((response) => response.json())
    .then((data) => {
      let config = data;
      initializeSpotify(config);
    })
});