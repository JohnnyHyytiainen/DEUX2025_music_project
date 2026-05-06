from pathlib import Path

BASE_PATH = Path(__file__).parents[1]

ASSETS_PATH = BASE_PATH / "assets"
COMPONENTS_PATH = BASE_PATH / "components"

IMAGE_PATH = ASSETS_PATH / "image"
STYLE_PATH = ASSETS_PATH / "style"
MARKDOWN_PATH = ASSETS_PATH / "markdown"

CHARTS_PATH = COMPONENTS_PATH / "charts"
FILTER_PATH = COMPONENTS_PATH / "filters"
QUERIES_PATH = COMPONENTS_PATH / "queries"

# ===============================
# FÄRGSKALOR & TEMA GLOBAL PAGES
# -- Färgskalor för spektrum-grafer (Gradienter) --
SCALE_MOOD = ["#1A1A95", "#CBC835"]  # Melankolisk (Blå) -> Glad (Gul)
SCALE_TEMPO = ["#4B4BFF", "#FF4B4B"]  # Långsam (Ljusblå) -> Snabb (Röd)
SCALE_ACOUSTIC = ["#8A2BE2", "#2E8B57"]  # Elektronisk (Lila) -> Akustisk (Grön)
SCALE_EXPLICIT = "Purples"  # Plotlys inbyggda lila skala
SCALE_SCATTER = "Burgyl"  # För Dancefloor scatter

# -- Specifika färger --
COLOR_RADAR = ["#1DB954", "#8A2BE2"]  # Spotify-grön och Synth-lila
COLOR_LINES = "#8D8D8D"  # Referenslinjer i grafer (Korset i scatter grafen)

# -- Layout & Bakgrunder --
BG_TRANSPARENT = "rgba(0, 0, 0, 0)"
BG_PLOT_DARK = "rgba(0, 0, 0, 0.08)"  # Kontrastruta bakom graferna
# ===============================
