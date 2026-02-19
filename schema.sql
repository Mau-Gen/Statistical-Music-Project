CREATE DATABASE music_stats;

USE music_stats;

SHOW TABLES;

CREATE TABLE artists (
	id INTEGER AUTO_INCREMENT NOT NULL,
    artist_name VARCHAR(64),
    PRIMARY KEY(id)
    );
    
CREATE TABLE songs (
	id INTEGER AUTO_INCREMENT NOT NULL,
    song_name VARCHAR(64),
	artist_id INTEGER,
    monthly_listeners INTEGER,
    album_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (artist_id) REFERENCES artists(id),
    FOREIGN KEY (album_id) REFERENCES albums(id)
);

CREATE TABLE albums (
	id INTEGER AUTO_INCREMENT NOT NULL,
    album_name VARCHAR(64),
    release_year YEAR,
    artist_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE artist_genre (
	artist_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (artist_id) REFERENCES artists(id),
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);

CREATE TABLE genre (
	id INTEGER AUTO_INCREMENT NOT NULL,
    genre_name VARCHAR(64),
    PRIMARY KEY (id)
);

CREATE TABLE users (
	id INTEGER AUTO_INCREMENT NOT NULL,
    username VARCHAR(64),
    subscription VARCHAR(64),
    PRIMARY KEY (id)
);

CREATE TABLE playlists (
	id INTEGER AUTO_INCREMENT NOT NULL,
    user_id INTEGER,
    playlist_name VARCHAR(64),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE playlist_songs (
	playlist_id INTEGER,
    song_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id),
    FOREIGN KEY (song_id) REFERENCES songs(id)
);

CREATE TABLE listening_data (
	id INTEGER AUTO_INCREMENT NOT NULL,
    duration INTEGER,
	user_id INTEGER,
    listened_at TIMESTAMP,
    song_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (song_id) REFERENCES songs(id)
);

SHOW TABLES;

SELECT * FROM listening_data;