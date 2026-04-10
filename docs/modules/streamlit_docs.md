# Streamlit Module Overview Docs (Basic)


## Streamlit Arkitekturen
Streamlit har inbyggt "Native Multipage" stöd. Om du har en mapp som heter `pages/` så kommer Streamlit *automatiskt* att läsa alla Python filer där i och bygga en färdig meny i vänsterkanten åt oss. 

* `src/dashboard/app.py`: **Framsidan.** (Körs med `streamlit run app.py`) Här sätter vi t.ex vår "logga", projekttitel och en kort introduktion. Ingen tung dataanalys här då det är framsidan på dashboarden.

* `src/dashboard/pages/01_Global_EDA.py`: Filnamnet blir bokstavligen namnet i menyn! Här lägger vi t.ex lands och humöranalys(?)

* `src/dashboard/pages/02_Historical_Trends.py`: Här lägger vi t.ex historiska trender.

* `src/dashboard/pages/03_Physical_Media.py`: Här lägger vi t.ex analyser om mediaformatet(CD, Vinyl, etc etc)

* `src/dashboard/components/queries_global.py`: Istället för att klottra ner sidorna med hundratals rader SQL, sparar vi våra queries här som funktioner (`def get_top_explicit_query(): return "SELECT..."`) och importerar dem till respektive sida.

    - Vi kan göra FLERA `src/dashboard/components/queries_xyz.py` script, går att göra ett/fler queries script för att jobba på samma `/page/XX_script.py`


