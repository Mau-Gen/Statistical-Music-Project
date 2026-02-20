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

SELECT * FROM songs;

ALTER TABLE songs ADD COLUMN duration INT;

UPDATE songs s
JOIN (
    -- Vi hittar max-lyssningen men lägger till en betydligt större 
    -- och mer varierad slumpmässig tid (mellan 10 och 120 sekunder)
    SELECT 
        s.id, 
        COALESCE(MAX(l.duration), 180) + FLOOR((RAND() * 10)) AS random_duration
    FROM songs s
    LEFT JOIN listening_data l ON s.id = l.song_id
    GROUP BY s.id
) AS calculated_data ON s.id = calculated_data.id
SET s.duration = calculated_data.random_duration;

SELECT duration FROM listening_data
WHERE listening_data.song_id = 2;

SELECT
                        songs.song_name,
                        COUNT(*) AS amount
                    FROM songs
                    JOIN listening_data ld ON ld.song_id = songs.id
                    WHERE ld.duration = songs.duration
                    GROUP BY songs.song_name
                    ORDER BY amount DESC;
                    
SELECT * FROM songs s
JOIN listening_data ld ON s.id = ld.song_id
WHERE ld.duration = s.duration;

DELIMITER $$

CREATE PROCEDURE CreateAUser(uname VARCHAR(64), sub_type VARCHAR(64))
DETERMINISTIC
BEGIN

	DECLARE FreeUser TINYINT;
    
    SELECT COUNT(*) INTO FreeUser
    FROM users
    WHERE uname = users.username;
    
    IF FreeUser = 0 THEN
		INSERT INTO users(username, subscription)
		VALUES (uname, sub_type);
        
        SELECT 'Completed' AS result;
        
	ELSE
		SELECT 'Failed' AS result;
        
	END IF;
END $$

DELIMITER ;
        
DROP PROCEDURE CreateAUser;
CALL CreateAUser('yippie', 'free');

SELECT * FROM users;

