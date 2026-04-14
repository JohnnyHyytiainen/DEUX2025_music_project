# Insights from EDA(Exploratory Data Analysis) on Spotify Charts

```
This dataset shows all the "Top 200" and "Viral 50" charts published globally by Spotify.
```
---

## Comprehensive list of what all the data columns in this dataset mean:

| Column | Meaning                                                                                       |
| :--- |:----------------------------------------------------------------------------------------------|
| **title** | The title of the song. *(type: str)*                                                          |
| **rank** | Rank on the chart in country (1-200) or globaly (1-50). *(type: int)*                         |
| **date** | The date for the measurement of the top chart. *(type: str)*                                  |
| **artist** | The name of the artist. *(type: str)*                                                         |
| **region** | The country or global. *(type: str)*                                                          |
| **chart**| If it is in top 200 (countries) or viral 500 (global). *(type: str)*                          |
| **trend** | If the song have moved up or down on on chart, same position or is a new entry. *(type: str)* |
| **streams** | How many streams the song has had in that country. *(type: float)*                            |


## Insights from basic EDA:

**Insights from my EDA:**

- There is alot of useful data, especially when looking in to a specific countries.
- There is a clear difference in toplists for the countries, this makes it more fun to see the charts later on.
- It is a big file with 26 million rows.
- Date has got the data type str. 

---