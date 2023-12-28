function createSongContainer(song) {
    const container = document.createElement("div");
    container.classList.add("song-container");

    const title = document.createElement("div");
    title.classList.add("song-title");
    title.textContent = song.title;

    const artist = document.createElement("div");
    artist.classList.add("artist-name");
    artist.textContent = `by ${song.artist_name}`;

    container.appendChild(title);
    container.appendChild(artist);

    document.body.appendChild(container); // Add it to the body, adjust this based on your layout
}

// Example: Use the function to create a container for each song
const sampleSong = { title: "Sample Song", artist_name: "Sample Artist" };
createSongContainer(sampleSong);