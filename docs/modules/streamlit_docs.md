# Streamlit Module Overview Docs (Basic)


## Streamlit Arkitekturen
Streamlit har inbyggt "Native Multipage" stöd. Om du har en mapp som heter `pages/` så kommer Streamlit *automatiskt* att läsa alla Python filer där i och bygga en färdig meny i vänsterkanten åt oss. 

* `src/dashboard/app.py`: **Framsidan.** (Körs med `streamlit run app.py`) Här sätter vi t.ex vår "logga", projekttitel och en kort introduktion. Ingen tung dataanalys här då det är framsidan på dashboarden.

* `src/dashboard/pages/01_Global_EDA.py`: Filnamnet blir bokstavligen namnet i menyn! Här lägger vi t.ex lands och humöranalys(?)

* `src/dashboard/pages/02_Historical_Trends.py`: Här lägger vi t.ex historiska trender.

* `src/dashboard/pages/03_Physical_Media.py`: Här lägger vi t.ex analyser om mediaformatet(CD, Vinyl, etc etc)

* `src/dashboard/components/queries_global.py`: Istället för att klottra ner sidorna med hundratals rader SQL, sparar vi våra queries här som funktioner (`def get_top_explicit_query(): return "SELECT..."`) och importerar dem till respektive sida.

    - Vi kan göra FLERA `src/dashboard/components/queries_xyz.py` script, går att göra ett/fler queries script för att jobba på samma `/page/XX_script.py`


# DRY principen i Streamlit.
När man bygger multi-page apps i Streamlit och i andra projekt händer det att en ofta kopierar in t.ex databaskopplingen(`duckdb.connect()`) eller sökvägar till t.ex databasen i varje fil en jobbar med. 

**GÖR INTE DET.** Det kommer inte Kokchun eller Debbie uppskatta. Ska vi jobba efter kriterierna ska vi följa DRY principerna.

Istället för att använda oss av onödiga importer varje gång i varje nytt script så bygger vi en `engine` eller `config`-fil i `/components` foldern.
---

### Fil strukturen och förklaring av DRY.
Här är de exempel vi kan använda oss utav som mallar för att snabbt förstå flödet och komma in i dashboard byggandet. Streamlit KAN läsa emojis i filnamnet och på något vänster göra dom till nice ikoner i menyn, därför det är emojis i filnamnen(Jag är inte galen, jag lovar)

```text
dashboard/
├── app.py                            # Framsidan
├── components/
│   └── data_loader.py                # Vår DRY-motor för databasen
└── pages/
    ├── 01_🌍_Global_EDA.py           # Vår globala analys - (Exempel)  
    ├── 02_📈_Historical_Trends.py    # Vår historiska analys - (Exempel)  
    └── 03_💿_Physical_Media.py       # Format-skiftet - (Exempel)
```

Vår `data_loader.py` fil gör **en** sak och har **en** funktion, inget mer. Dess funktion är detta: den pratar med databasen, cachar resultatet och skickar tillbaka en Pandas DataFrame.
