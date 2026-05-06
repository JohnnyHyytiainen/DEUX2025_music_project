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