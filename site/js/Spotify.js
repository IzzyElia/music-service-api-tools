// Spotify.js

import { createUIElement } from "./UI.js";
import * as Shared from "./Shared.js";
import { refreshUserData } from "./DataViewer.js";

let config = undefined;

class Spotify {
    constructor(accessToken) {
      this.accessToken = accessToken;
    }


    async getUserPlaylists(userData) {
      let offset = 0;
      let hasMore = true;
    
      while (hasMore) {
        const endpoint = `https://api.spotify.com/v1/me/playlists?limit=50&offset=${offset}`;
        const response = await fetch(endpoint, {
          headers: {
            "Authorization": `Bearer ${this.accessToken}`,
          },
        });
        const data = await response.json();
    
        for (const playlistData of data.items) {
          const playlist = new Shared.Playlist(
            playlistData.name,
            playlistData.description
          );
          const tracks = await this.getPlaylistTracks(playlistData.id);
          for (const trackId in tracks) {
            playlist.addTrackIfNotDuplicate(tracks[trackId]);
          }
          userData.addPlaylistIfNotDuplicate(playlist);
        }
    
        hasMore = data.next !== null;
        offset += data.items.length;
      }
    }


    async getPlaylistTracks(playlistId) {
      let offset = 0;
      let hasMore = true;
      const tracks = {};
    
      while (hasMore) {
        const endpoint = `https://api.spotify.com/v1/playlists/${playlistId}/tracks?limit=100&offset=${offset}`;
        const response = await fetch(endpoint, {
          headers: {
            "Authorization": `Bearer ${this.accessToken}`,
          },
        });
        const data = await response.json();
    
        for (const trackData of data.items) {
          const track = new Shared.Track(
            trackData.track.name,
            trackData.track.artists[0].name,
            trackData.track.album.name,
          );
          tracks[trackData.track.id] = track;
        }
        refreshUserData(Shared.concatUserDatas(userDatas));
    
        hasMore = data.next !== null;
        offset += data.items.length;
      }
    
      return tracks;
    }
    
  
    async getUserLikedTracks(userData) {
      let offset = 0;
      let hasMore = true;
    
      while (hasMore) {
        const endpoint = `https://api.spotify.com/v1/me/tracks?limit=50&offset=${offset}`;
        const response = await fetch(endpoint, {
          headers: {
            "Authorization": `Bearer ${this.accessToken}`,
          },
        });
        const data = await response.json();
    
        for (const trackData of data.items) {
          const track = new Shared.Track(
            trackData.track.name,
            trackData.track.artists[0].name,
            trackData.track.album.name,
            trackData.track.album.release_date.slice(0, 4)
          );
          userData.add(track);
        }
        refreshUserData(Shared.concatUserDatas(userDatas));
    
        // Check if there are more items to fetch
        hasMore = data.next !== null;
        // Update the offset for the next request
        offset += data.items.length;
      }
    }
    
  
    async getUserFollowedArtists(userData) {
      let after = null;
      let hasMore = true;
    
      while (hasMore) {
        const endpoint = `https://api.spotify.com/v1/me/following?type=artist&limit=50${after ? `&after=${after}` : ''}`;
        const response = await fetch(endpoint, {
          headers: {
            "Authorization": `Bearer ${this.accessToken}`,
          },
        });
        const data = await response.json();
    
        for (const artistData of data.artists.items) {
          const artist = new Shared.Artist(artistData.name);
          userData.addFollowedArtist(artist);
        }
        refreshUserData(Shared.concatUserDatas(userDatas));
    
        hasMore = data.artists.next !== null;
        after = data.artists.cursors.after;
      }
    }

    async addExistingPlaylists(userData) {
      for (const playlist of userData.playlists) {
        // Check if the playlist already exists on Spotify
        const endpoint = `https://api.spotify.com/v1/me/playlists?limit=1&q=${encodeURIComponent(playlist.name)}`;
        const response = await fetch(endpoint, {
          headers: {
            "Authorization": `Bearer ${this.accessToken}`,
          },
        });
        const data = await response.json();
    
        if (data.items.length > 0) {
          // Playlist already exists on Spotify
          const spotifyPlaylist = data.items[0];
          const spotifyTracks = await this.getPlaylistTracks(spotifyPlaylist.id);
    
          // Compare the track list with the existing playlist
          if (Shared.isEqualPlaylist(playlist, spotifyTracks)) {
            continue; // Skip this playlist
          }
    
          // Only add the tracks that are not present in the existing playlist
          for (const trackId in playlist.tracks) {
            if (!spotifyTracks.hasOwnProperty(trackId)) {
              await this.addTrackToPlaylist(spotifyPlaylist.id, trackId);
            }
          }
        } else {
          // Playlist doesn't exist on Spotify, create a new one
          const spotifyPlaylist = await this.createPlaylist(playlist.name, playlist.description);
          for (const trackId in playlist.tracks) {
            await this.addTrackToPlaylist(spotifyPlaylist.id, trackId);
          }
        }
      }
    }
    
    async addExistingLikedTracks(userData) {
      for (const track of userData.likedTracks) {
        // Check if the track already exists in the user's Liked Songs
        const endpoint = `https://api.spotify.com/v1/me/tracks/contains?ids=${track.id}`;
        const response = await fetch(endpoint, {
          headers: {
            "Authorization": `Bearer ${this.accessToken}`,
          },
        });
        const data = await response.json();
    
        if (!data[0]) {
          // Track doesn't exist in the user's Liked Songs, add it
          await this.addTrackToLibrary(track.id);
        }
      }
    }
    
    async addExistingFollowedArtists(userData) {
      for (const artist of userData.followedArtists) {
        // Check if the artist is already followed by the user
        const endpoint = `https://api.spotify.com/v1/me/following/contains?type=artist&ids=${artist.id}`;
        const response = await fetch(endpoint, {
          headers: {
            "Authorization": `Bearer ${this.accessToken}`,
          },
        });
        const data = await response.json();
    
        if (!data[0]) {
          // Artist is not followed by the user, follow them
          await this.followArtist(artist.id);
        }
      }
    }
    
    
  }
  
  
  
  function createSpotifyLoginButton(parent) {
    const button = createUIElement("button", parent);
    button.innerText = "Login with Spotify";
    button.addEventListener("click", redirectToSpotifyAuthorization);
    return button;
  }
  
  function redirectToSpotifyAuthorization() {
    const clientId = config.spotifyClientId;
    const redirectUri = config.rootUrl + '/spotify-authorization.html';
    const scope = 'user-library-read user-follow-read playlist-read-private playlist-modify-public playlist-modify-private';
    const responseType = 'token';
  
    const url = `https://accounts.spotify.com/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}&response_type=${responseType}`;
  
    window.location.href = url;
  }

  function createLoadingSpinner(parent) {
    const spinner = createUIElement("div", parent);
    spinner.classList.add("spinner");
    return spinner;
  }
  
  // This function is called from site/js/Main.js
  // It checks if the user is already logged in to Spotify, and if not, it creates a login button
  function initializeSpotify(_config) {
    config = _config;
    const parent = document.getElementById("spotify-wrapper");
    const queryParams = new URLSearchParams(window.location.search);
    const accessToken = Shared.getCookie("spotify_access_token");
  
    if (accessToken) {
      const spotify = new Spotify(accessToken);
      // Check if the access token is still valid
      const endpoint = "https://api.spotify.com/v1/me";
      fetch(endpoint, {
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      })
      .then((response) => {
        if (response.ok) {
          // Add loading spinner
          const spinner = createLoadingSpinner(parent);
  
          let spotifyUserData = new Shared.UserData("Spotify");
          // Remove any existing Spotify user data
          const spotifyUserDataIndex = userDatas.findIndex(userData => userData.serviceIdentifier === 'Spotify');
          if (spotifyUserDataIndex !== -1) {
            userDatas.splice(spotifyUserDataIndex, 1);
          }
          // Add the new spotify user data
          userDatas.push(spotifyUserData);
          // Use Promise.all to wait for all the requests to complete
          Promise.all([
            spotify.getUserPlaylists(spotifyUserData),
            spotify.getUserLikedTracks(spotifyUserData),
            spotify.getUserFollowedArtists(spotifyUserData),
          ]).then(() => {
  
            // Change spinner to "Done"
            spinner.classList.remove("spinner");
            spinner.innerText = "Done";
            refreshUserData(Shared.concatUserDatas(userDatas));
          });
        } else {
          // The token is not valid, so create the login button
          createSpotifyLoginButton(parent);
        }
      });
    } else {
      // The access token is not present, so create the login button
      createSpotifyLoginButton(parent);
    }
  }

  function getAccessTokenFromHash() {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    return params.get('access_token');
  }

  function redirectToHomePage() {
    window.location.href = './index.html';
  }

  // This function is called from spotify-authorization.html, after spotify has redirected the user back to the site following authentication
  // It extracts the access token from the hash and stores it in a cookie, then redirects the user back to the home page
  function onSpotifyAuthentication() {
    const accessToken = getAccessTokenFromHash();
    if (accessToken) {
      Shared.setCookie('spotify_access_token', accessToken, 1);
      redirectToHomePage();
    }
  }
    
  
  
  export { initializeSpotify, onSpotifyAuthentication };
  