export class Playlist {
    constructor(name, description) {
      this.name = name;
      this.description = description;
      this.tracklist = [];
    }
    addTrackIfNotDuplicate(track) {
      const existingTrack = this.tracklist.find(t => t.trackHash === track.trackHash);
      if (!existingTrack) {
        this.tracklist.push(track);
      }
    }
    
  }
  
  export class Track {
    constructor(name, artistName, albumName, releaseYear) {
      this.name = name;
      this.artistName = artistName;
      this.albumName = albumName;
      this.trackHash = this.getTrackHash();
    }

    getTrackHash() {
      // Use a combination of the track name, artist, album, and year to create a unique hash
      return `${this.name}-${this.artistName}-${this.albumName}`.replace(/\s+/g, '-').toLowerCase();
    }
  }
  
  export class Artist {
    constructor(name) {
      this.name = name;
    }
  }
  
  export class UserData {
    constructor(serviceIdentifier) {
      this.serviceIdentifier = serviceIdentifier;
      this.playlists = {};
      this.tracks = {};
      this.artists = {};
    }
  
    addPlaylistIfNotDuplicate(playlist) {
      if (!this.playlists.hasOwnProperty(playlist.name)) {
        this.playlists[playlist.name] = playlist;
      }
    }
  
    addLikedTrackIfNotDuplicate(track) {
      const key = `${track.name}-${track.artistName}`;
      if (!this.tracks.hasOwnProperty(key)) {
        this.tracks[key] = track;
      }
    }
  
    addFollowedArtistIfNotDuplicate(artist) {
      if (!this.artists.hasOwnProperty(artist.name)) {
        this.artists[artist.name] = artist;
      }
    }
  
    dumpData() {
      console.log("Playlists:");
      for (const playlist of Object.values(this.playlists)) {
        console.log(`- ${playlist.name} (${playlist.description})`);
        console.log(`  ${playlist.tracklist.length} tracks`);
      }
  
      console.log("\nTracks:");
      for (const track of Object.values(this.tracks)) {
        console.log(`- ${track.name} (${track.artistName}, ${track.albumName}, ${track.releaseYear})`);
      }
  
      console.log("\nArtists:");
      for (const artist of Object.values(this.artists)) {
        console.log(`- ${artist.name}`);
      }
    }
  }
  
  export function concatUserDatas(userDatas) {
    const combinedUserData = new UserData();
    const seenPlaylists = {};
    const seenTracks = {};
    const seenArtists = {};
  
    for (const userData of userDatas) {
      if (userData.playlists !== undefined) {
        for (const playlist of Object.values(userData.playlists)) {
          if (!seenPlaylists.hasOwnProperty(playlist.name)) {
            seenPlaylists[playlist.name] = true;
            combinedUserData.addPlaylistIfNotDuplicate(playlist);
          }
        }
      }
      if (userData.tracks !== undefined) {
        for (const track of Object.values(userData.tracks)) {
          if (!seenTracks.hasOwnProperty(track.trackHash)) {
            seenTracks[track.trackHash] = true;
            combinedUserData.addLikedTrackIfNotDuplicate(track);
          }
        }
      }
      if (userData.artists !== undefined) {
        for (const artist of Object.values(userData.artists)) {
          if (!seenArtists.hasOwnProperty(artist.name)) {
            seenArtists[artist.name] = true;
            combinedUserData.addFollowedArtistIfNotDuplicate(artist);
          }
        }
      }
    }
  
    return combinedUserData;
  }
  
  
  
  
// Function to set a cookie with a given name, value, and expiration time
export function setCookie(name, value, daysToExpire) {
  const date = new Date();
  date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
  const expires = "expires=" + date.toUTCString();
  document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

// Function to get the value of a cookie with a given name
export function getCookie(name) {
  const cookieName = name + "=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookieArray = decodedCookie.split(';');
  for(let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i];
    while (cookie.charAt(0) === ' ') {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }
  return "";
}
