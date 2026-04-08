# Insights from EDA(Exploratory Data Analysis) on top spotify songs in 73 countries dataset. GLOBAL

```
This dataset(several versions) presents the top songs currently trending for over 70 countries where the top 50 songs for each country is updated daily up to 2025-06-11. The purpose of this dataset according to kaggle is to provide the most up to date information on the popularity of songs accross the world.
```
---

## Comprehensive list of what all the data columns in this dataset mean:

| Column | Meaning |
| :--- | :--- |
| **spotify_id** | The unique identifier for the song in the Spotify database. *(type: str)* |
| **name** | The title of the song. *(type: str)* |
| **artists** | The name(s) of the artist(s) associated with the song. Do `split(', ')` to convert to a list. *(type: str)* |
| **daily_rank** | The daily rank of the song in the top 50 list. *(type: int)* |
| **daily_movement** | The change in rankings compared to the previous day. *(type: int)* |
| **weekly_movement**| The change in rankings compared to the previous week. *(type: int)* |
| **country** | The ISO code of the country of the Top 50 Playlist. If Null, then the playlist is 'Global Top 50'. *(type: str)* |
| **snapshot_date** | The date on which the data was collected from the Spotify API. *(type: str)* |
| **popularity** | A measure of the song's current popularity on Spotify. *(type: int)* |
| **is_explicit** | Indicates whether the song contains explicit lyrics. *(type: bool)* |
| **duration_ms** | The duration of the song in milliseconds. *(type: int)* |
| **album_name** | The title of the album the song belongs to. *(type: str)* |
| **album_release_date** | The release date of the album the song belongs to. *(type: str)* |
| **danceability** | A measure of how suitable the song is for dancing based on various musical elements. *(type: float)* |
| **energy** | A measure of the intensity and activity level of the song. *(type: float)* |
| **key** | The key of the song. *(type: int)* |
| **loudness** | The overall loudness of the song in decibels. *(type: float)* |
| **mode** | Indicates whether the song is in a major or minor key. *(type: int)* |
| **speechiness** | A measure of the presence of spoken words in the song. *(type: float)* |
| **acousticness** | A measure of the acoustic quality of the song. *(type: float)* |
| **instrumentalness** | A measure of the likelihood that the song does not contain vocals. *(type: float)* |
| **liveness** | A measure of the presence of a live audience in the recording. *(type: float)* |
| **valence** | A measure of the musical positiveness conveyed by the song. *(type: float)* |
| **tempo** | The tempo of the song in beats per minute. *(type: float)* |
| **time_signature** | The estimated overall time signature of the song. *(type: int)* |


- First thoughts from exploring the dataset:
    - This dataset is quite big. Containing 2110316 rows and 25 columns.

    - This dataset contains `str`, `int64`, `bool` and `float64` as its data types.

    - The dataset contains ALOT of NULL values.
        - Name: 30 null values
        - Artists: 29 null values
        - Country: 28908 null values
        - Album_name: 822 null values
        - Album_release_date: 659 null values
    - **NOTE ABOUT NULL VALUES:** 28 908 `NULL` values in `Country` does not mean its faulty data, it represents the `GLOBAL` top-list. This is **Important** to know. `If Null, then the playlist is GLOBAL TOP 50`


## First insights from basic EDA:

**Insights from my EDA:**

- Shape (2.1 mil rows): This is a big file. It's the perfect size to show why DuckDB is needed later in our project, as regular Pandas can start to be a bit slow when UX wants to filter this live in a dashboard.

- The Country column (28,908 Null values): Looking at `df.head()`. The first three rows have NaN (Null) on country, but rank 1, 2 and 3. What does this mean logically? Well, that NaN in this dataset represents "Global" (the global top list) If we just drop null values, we are deleting the most important list! I need to do a `.fillna('Global')`.

- Snapshot_date (str): The dates are loaded as text strings. In order to answer one of our more *important* questions about trends over time (summer vs winter for example) I need to cast this to the correct datetime object so I can extract "Month" and "Year".

- Missing artists (30 rows): 30 rows out of 2.1 million are nothing to be concerned about. I'll just drop these.

---

## From RAW data to processed data and the next steps.

1) To process my data i need to clean it and make some changes to clear up confusion as mentioned above.
    - I need to make use of the `fillna()`-method in Pandas to replace missing data that is represented as `NaN`(Not a Number). If Country has a `NaN`-value instead of an ISO country code that means its a `GLOBAL` top list.
    
    - I need to make use of the `dropna`-function in pandas to remove all rows that contain missing values on name(song title) and artist. 29+30 is a negligible number of rows.

    - **CRITICAL** I need to make use of the `to_datetime()`-function to convert datetime str to real DateTime objects to be able to make analysis on a real timeline.

    - With converting date in str format to real datetime objects its critical for me to add another column in the dataset to be able to analyze 'Seasonal trends'. Easy fix by adding another column named 'month'

```python
# 1) Hantera saknade länder, NaN (Null values) -> Global
df['country'] = df['country'].fillna('Global')

# 2) Droppa de FÅ rader där artistnamn eller låtnamn saknas(Är 59stycken totalt. Irrelevant på 2.1miljoner)
df = df.dropna(subset=['name', 'artists'])

# 3) Konvertera datumsträng till riktiga DateTime objects.
# === KRITISKT FÖR TIDSANALYSEN ===
df['snapshot_date'] = pd.to_datetime(df['snapshot_date'])

# 4) Skapa ny column med Månad för att underlätta för att analysera "säsongs trender"
df['month'] = df['snapshot_date'].dt.month

print("Cleaning done. New Null-Values:")
print(df.isnull().sum())
```

- **New output from processed data cell:**

```markdown
Cleaning done. New Null-Values:
spotify_id              0
name                    0
artists                 0
daily_rank              0
daily_movement          0
weekly_movement         0
country                 0
snapshot_date           0
popularity              0
is_explicit             0
duration_ms             0
album_name            792
album_release_date    630
danceability            0
energy                  0
key                     0
loudness                0
mode                    0
speechiness             0
acousticness            0
instrumentalness        0
liveness                0
valence                 0
tempo                   0
time_signature          0
month                   0
dtype: int64
```


# Insights from NATIONAL-EDA on top spotify songs in 73 countries dataset.

## What country listens to the most explicit songs according to spotifys universal dataset?

```
Worlds top 10 most 'Explicit' Nations according to Spotifys data:
country  explicit_percentage  total_unique_songs
     GR                 68.5                 904
     CL                 64.4                 597
     DO                 60.8                 873
     MX                 57.3                 495
     SK                 56.4                 944
     FR                 54.1                 903
     BY                 52.9                 772
     SV                 51.6                 572
     GT                 51.5                 443
     CZ                 50.7                 845
```

- Results and insights of explicit music analysis:
```text
Greece (GR) in first place with 68.5%! Who would have guessed it? Over two-thirds(2/3) of the music on their top list has an "Explicit" stamp.

Latin America dominates: Chile (CL), Dominican Republic (DO), Mexico (MX), El Salvador (SV) and Guatemala (GT).

Insights: Latin American hiphop and reggaeton, which often have explicit lyrics are incredibly dominant globally, and its clearly visible in this dataset.


Europes unexpected contributions: Slovakia (SK), France (FR), Belarus (BY) and the Czech Republic (CZ). 

Insights: The French and Eastern European rap scene in particular seems to be pushing these numbers up.

No Nordic countries (SE, NO, DK, FI) in the top 10. We up in the north seem to be listening to a bit more "clean" music, or at least music that isnt flagged as heavily by Spotify.
```


# What countries are the happiest, saddest (Valence) and likes the highest tempo? (BPM)
```text
The Kings of Joy (Latin America and... Japan?): 

Latin America completely dominates the joy list. Mexico (MX), Uruguay (UY), Brazil (BR). The results are clear that genres like reggaeton, cumbia and Brazilian funk lift the mood extremely. But that Japan (JP) sneaks in at fifth place? That is a wonderful AND a very unexpected insight! J-pop is often extremely upbeat and colorful.


The Heartbreak Belt (Southeast Asia): 

The "depressed" list (lowest valence) is completely dominated by Southeast Asia: Indonesia (ID), Malaysia (MY), Vietnam (VN), Taiwan (TW). There is a massive music culture in these countries around extremely emotional power ballads and heartbreak songs (in Indonesia it is often called "Galau" music apparently). Its also very interesting that the USA (US) is in the top 10 most depressed! A lot of moody trap and melancholic pop there right the previous years.


The Techno & Eurodance axis (BPM): 

Here we see what most of us could expect. Eastern and Central Europe crushes all opposition when it comes to tempo. Bulgaria (BG), Romania (RO), Czech Republic (CZ), Slovakia (SK), Austria (AT) and Germany (DE). Here, pumping bass, house, techno and fast paced electronic music are as always the order of the day!


Odd detail to further investigate: Look at Slovakia (SK) and the Czech Republic (CZ). They are in the top 10 most depressing, BUT at the same time top 10 fastest. Fast but sad music? It smells like intense, melancholic electronic music or hard rock by a long way! Needs to be investigated more with genres!
```

## Crushing the happiness == BPM myth!
```text
Insights and an odd mythbuster. 

Fast music ≠ Happy music.
The fact that the trend line is pointing downwards is a fantastic insight! If you think about it purely musically, it actually makes sense when we look at a global scale:

High BPM but Low Joy: 
Think intense, dark techno, hard rock/metal, or stressful and aggressive trap-hip-hop. The tempo may be 140+ BPM, but the mood (valence) is dark, angry or melancholic.

Low BPM but High Joy: 
Think reggae, lo-fi beats, or a cozy acoustic summer song. The tempo simmers at a leisurely 80 BPM, but the music is extremely positive and uplifting.

---

If my findings are correct We've just busted a myth in the data. Fast tempo doesnt mean happy music – in fact, its the opposite. If youre building a 'mood filter' in the app, BPM and Happiness need to be two completely separate controls!"
```


## The nordic "vibe wars"

```text
The Northern War: 

Swedens Embarrassing Loss..
Hahaha, I have to laugh at the bar chart! If you look at the results, they defy all stereotypes:

Finland (Red) are the happy bundles of energy! People often joke that Finns are quiet and melancholic, but their charts absolutely crush the rest of the Nordics in both Joy and Energy.

Denmark (Yellow) owns the dance floor. They have the highest Danceability. (Maybe its all their Danish club music and sausage pop?)

Sweden (Green)... We are the most depressed and tired. We are last in both Valence and Energy. Our charts are filled with melancholic pop, dark hip hop and EPA dunk.
```