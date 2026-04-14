# Insights from EDA(Exploratory Data Analysis) on Spotify Global Music Dataset (2009–2025)

```
This dataset shows timeless hits from 2009 to 2023. It offers insights on how music trends, artist popularity, and genres.
```
---

## Comprehensive list of what all the data columns in this dataset mean:

| Column | Meaning                                                                           |
| :--- |:----------------------------------------------------------------------------------|
| **track_id** | The songs id. *(type: str)*                                                       |
| **track_name** | The title of the song. *(type: str)*                                              |
| **track_number** | The songs placement of the order in the album. *(type: int)*                      |
| **track_popularity** | The trending of the song on the platform at the moment. *(type: int)*             |
| **track_duration_ms** | How long the song is. *(type: int)*                                               |
| **explicit**| If the song contains explicit words (bad language, violence etc.). *(type: bool)* |
| **artist_name** | The name of the artist. *(type: str)*                                             |
| **artist_popularity** | How popular the artist is at the moment. *(type: float)*                          |
| **artist_followers** | How many folowers the artist has got at the moment. *(type: float)*               |
| **artist_genres** | The artist's primary genre. *(type: str)*                                         |
| **album_id** | The ID of the album. *(type: str)*                                                |
| **album_name** | The title of the album the song belongs to. *(type: str)*                         |
| **album_release_date** | The release date of the album the song belongs to. *(type: str)*                  |
| **album_total_tracks** | The amount of tracs containing in the album. *(type: int)*                        |
| **album_type** | If the album is a single or album. *(type: str)*                                  |


## Insights from basic EDA:

**Insights from my EDA:**

- The "track_popularity" and "artist_popularity" can be misleading. You don't know when the measurement was made.
- "artist_genres" is missing from about half or the rows.
- The amount of "artist_followers" can differ for an artist depending on the song. Since it is artist followers and not followers for a song. This gives unsure data since it is not clarified when the number is from.


---