CREATE or REPLACE DATABASE Patrick_DB;

CREATE or REPLACE SCHEMA external_stage;

CREATE or REPLACE TABLE tblAlbum (
    album_id VARCHAR(50) PRIMARY KEY,
    album_name VARCHAR(255),
    album_release DATE,
    album_total_tracks INTEGER,
    album_external_urls VARCHAR(500)
);


CREATE or REPLACE TABLE tblArtist (
    artist_id TEXT PRIMARY KEY,
    artist_name TEXT NOT NULL,
    external_url TEXT
);

CREATE or REPLACE TABLE tblSong (
    song_id VARCHAR(50) PRIMARY KEY,
    song_name VARCHAR(255) NOT NULL,
    song_duration INTEGER,
    song_url VARCHAR(500),
    song_pop INTEGER,
    song_added TIMESTAMP,
    album_id VARCHAR(50),
    artist_id VARCHAR(50)
);


CREATE or REPLACE STAGE my_external_stage
url = 's3://siase-spotify-pipeline/transform-data/'    
STORAGE_INTEGRATION = my_s3_integration

list @my_external_stage



CREATE or REPLACE pipe tblalbum_spotify
auto_ingest = TRUE
AS
COPY INTO tblAlbum
FROM @my_external_stage/album_data/
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1)


CREATE or REPLACE pipe tblArtist_spotify
auto_ingest = TRUE
AS
COPY INTO tblArtist
FROM @my_external_stage/artist_data/
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1)


CREATE or REPLACE pipe tblSong_spotify
auto_ingest = TRUE
AS
COPY INTO tblSong
FROM @my_external_stage/songs_data/
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1)


desc pipe tblArtist_spotify

show pipes

SELECT * from tblAlbum

SELECT * from tblArtist

SELECT * from tblSong







