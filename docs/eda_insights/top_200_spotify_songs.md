# Insights from EDA(Exploratory Data Analysis) on top spotify songs in 73 countries dataset.

```
This dataset(several versions) presents the top songs currently trending for over 70 countries where the top 50 songs for each country is updated daily up to 2025-06-11. The purpose of this dataset according to kaggle is to provide the most up to date information on the popularity of songs accross the world.
```
---

## Comprehensive list of what all the data columns in this dataset mean:

| Column | Meaning |
| :--- | :--- |
| **spotify_id** | The unique identifier for the song in the Spotify database. *(type: str)* |
| **name** | The title of the song. *(type: str)* |


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