import * as Shared from './Shared.js';
import { createUIElement } from './UI.js';

// Tracks the currently expanded playlists
let expandedPlaylists = {};



export function refreshUserData() {
    
    const userDataWrapper = document.getElementById('user-data-wrapper');
    if (!userDataWrapper.getAttribute('initialized')) {
        // Create containers for each section
        const playlistsContainer = createUIElement('div', userDataWrapper);
        playlistsContainer.id = 'playlists-container';
        const artistsContainer = createUIElement('div', userDataWrapper);
        artistsContainer.id = 'artists-container';
        const tracksContainer = createUIElement('div', userDataWrapper);
        tracksContainer.id = 'tracks-container';
    
        // Create headers for each section and attach event listeners
        createSectionHeader('Playlists', playlistsContainer, renderPlaylists);
        createSectionHeader('Followed Artists', artistsContainer, renderArtists);
        createSectionHeader('Liked Tracks', tracksContainer, renderTracks);

        // Set initialized to true so that the containers are not recreated
        userDataWrapper.setAttribute('initialized', 'true');
    }
    else {
        const playlistContainer = document.getElementById('playlists-container');
        const artistsContainer = document.getElementById('artists-container');
        const tracksContainer = document.getElementById('tracks-container');
        refreshSection(playlistContainer, renderPlaylists);
        refreshSection(artistsContainer, renderArtists);
        refreshSection(tracksContainer, renderTracks);
    }
  }
  
  function createSectionHeader(title, parent, renderFn) {
    const headerWrapper = createUIElement('div', parent);
    headerWrapper.setAttribute('header', 'true');
    const headerText = createUIElement('h2', headerWrapper);
    headerText.innerText = title;
    const contents = createUIElement('div', parent);
    contents.setAttribute('contents', 'true');
    headerWrapper.addEventListener('click', () => { toggleSection(parent, renderFn, null); })
  }

  function createPlaylistSection(playlist, parent) {
    const wrapper = createUIElement('div', parent);
    const headerWrapper = createUIElement('div', wrapper);
    headerWrapper.setAttribute('header', 'true');
    const headerText = createUIElement('h3', headerWrapper);
    headerText.innerText = playlist.name;
    const contents = createUIElement('div', wrapper);
    contents.setAttribute('contents', 'true');
    if (expandedPlaylists[playlist.name]) {
        wrapper.setAttribute('data-expanded', 'true');
        renderTracklist(contents, playlist.name);
    }
    headerWrapper.addEventListener('click', () => { togglePlaylist(wrapper, renderTracklist, playlist.name); })
  }
  
  function toggleSection(container, renderFn) {
    const isExpanded = container.getAttribute('data-expanded') === 'true';
  
    if (isExpanded) {
      container.setAttribute('data-expanded', 'false');
    } else {
      container.setAttribute('data-expanded', 'true');
    }

    refreshSection(container, renderFn, null);
    return container;
  }

  function togglePlaylist(container, renderFn, playlistName) {
    const isExpanded = container.getAttribute('data-expanded') === 'true';
  
    if (isExpanded) {
      container.setAttribute('data-expanded', 'false');
      delete expandedPlaylists[playlistName];
    } else {
      container.setAttribute('data-expanded', 'true');
      expandedPlaylists[playlistName] = true;
    }

    refreshSection(container, renderFn, playlistName);
    return container;
  }
  
  function refreshSection(container, renderFn, context) {
    const isExpanded = container.getAttribute('data-expanded') === 'true';
    const contents = container.querySelector('[contents]');
  
    if (isExpanded) {
        // Clear and re-render the section
        contents.innerHTML = '';
        renderFn(contents, context);
    } else {
        // Clear the section
        contents.innerHTML = '';
    }
  }

  function renderPlaylists(container) {
    const userData = Shared.concatUserDatas(userDatas);
    const playlists = userData.playlists;
    for (const id in playlists) {
      const playlist = playlists[id];
      createPlaylistSection(playlist, container);
    }
  }
  
  function renderTracklist(container, playlistName) {
    const userData = Shared.concatUserDatas(userDatas);
    const playlist = userData.playlists[playlistName];
    const tracklist = playlist.tracklist;
    const tracklistElement = createUIElement('ul', container);
    tracklistElement.classList.add('tracklist');
  
    for (const track of tracklist) {
      const trackElement = createUIElement('li', tracklistElement);
      trackElement.classList.add('track-item');
      trackElement.textContent = `${track.name} - ${track.artistName} - ${track.albumName} (${track.releaseYear})`;
    }
  }
  
  function renderArtists(container) {
    const userData = Shared.concatUserDatas(userDatas);
    const artists = userData.artists;
    for (const id in artists) {
      const artist = artists[id];
      const artistElement = createUIElement('div', container);
      artistElement.classList.add('artist-item');
      artistElement.textContent = artist.name;
    }
  }
  
  function renderTracks(container) {
    const userData = Shared.concatUserDatas(userDatas);
    const tracks = userData.tracks;
    for (const id in tracks) {
      const track = tracks[id];
      const trackElement = createUIElement('div', container);
      trackElement.classList.add('track-item');
      trackElement.textContent = `${track.name} - ${track.artistName} - ${track.albumName} (${track.releaseYear})`;
    }
  }