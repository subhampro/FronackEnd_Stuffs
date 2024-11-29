const SpotifyWebApi = require('spotify-web-api-node');
const { exec } = require('child_process');

// Spotify credentials - Replace with your Spotify credentials
const spotifyApi = new SpotifyWebApi({
  clientId: '6d9a8a5c914448fb93aa605cc67b90f9',  // Replace with your actual Spotify client ID
  clientSecret: 'ebeabfcb91464c87b18ae944d386e294',  // Replace with your actual Spotify client secret
});

// Get access token from Spotify API
async function getSpotifyAccessToken() {
  try {
    const data = await spotifyApi.clientCredentialsGrant();
    spotifyApi.setAccessToken(data.body['access_token']);
  } catch (error) {
    console.error('Error getting Spotify access token', error);
  }
}

// Search for songs by artist from Spotify
async function getTopSongsByArtist(artistName) {
  try {
    const data = await spotifyApi.searchTracks(`artist:${artistName}`, { limit: 10 });
    const tracks = data.body.tracks.items;
    return tracks.map((track) => track.name);
  } catch (error) {
    console.error('Error searching for songs on Spotify', error);
    return [];
  }
}

// Function to escape special characters in the song name
function escapeSearchQuery(songName) {
  return songName.replace(/[)(]/g, '\\$&').replace(/["']/g, '\\$&');
}

// Download song from YouTube as MP3 using yt-dlp
function downloadSong(songName) {
  const escapedSongName = escapeSearchQuery(songName);
  const command = `yt-dlp -x --audio-format mp3 -o "%(title)s.%(ext)s" "ytsearch:${escapedSongName}"`;

  // Execute yt-dlp command to download the song
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing yt-dlp: ${stderr}`);
    } else {
      console.log(`Downloaded: ${songName}`);
    }
  });
}

// Main function to orchestrate Spotify and yt-dlp functionality
async function main(artistName) {
  await getSpotifyAccessToken();
  const songs = await getTopSongsByArtist(artistName);

  if (songs.length === 0) {
    console.log(`No songs found for artist: ${artistName}`);
    return;
  }

  console.log(`Found ${songs.length} songs for ${artistName}:`);
  songs.forEach((song, index) => {
    console.log(`${index + 1}. ${song}`);
    downloadSong(song);  // Download each song
  });
}

// Run the script
const artistName = process.argv[2];  // Get artist name from command-line arguments
if (!artistName) {
  console.log('Please provide an artist name.');
  process.exit(1);
}

main(artistName);
