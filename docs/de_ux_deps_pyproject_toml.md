# Förslag på de deps(dependencies) vi kommer behöva som minst för projektet

Bare bones som bör täcka de dependencies vi behöver. Varför ingen FastAPI eller Psycopg?

UX som designar i Figma, gör överlämningar till oss(DE), och sedan är det vi (DE) som bygger själva produkten i Streamlit och PowerBI.
Streamlit är redan en fullstack lösning i Python. Den har sin egen server och hanterar sin egen state. Att bygga ett FastAPI lager mellan vår DuckDB-data och vår Streamlit applikation lägger bara till nätverkslatens, extra kod och en ny punkt där systemet kan krascha. Efter att ha läst på lite mer kring streamlit så är jag nästan säker på att det ej kommer behövas.


```bash
[project]
name = "dataviz-de-ux-collab"
version = "0.1.0"
description = "Cross-functional data visualization platform (DE + UX)"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    # Ingestion & Utility
    "requests>=2.31.0",
    "python-dotenv>=1.0.0",
    "loguru>=0.7.0",
    
    # Processering & EDA (Krav)
    "pandas>=2.2.0",
    "duckdb>=0.10.0",
    
    # Visualisering & Frontend (Krav)
    "streamlit>=1.32.0",
    "matplotlib>=3.8.0",
    "seaborn>=0.13.0",    # Frivillig, men gör Matplotlib våra grafer snyggare snabbare
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.3.0",
]

[tool.ruff]
line-length = 88
select = ["E", "F", "I"] # Errors, Pyflakes, Isort

[tool.pytest.ini_options]
testpaths = ["tests"]
```