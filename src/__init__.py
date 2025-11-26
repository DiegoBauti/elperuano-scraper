from .scraper import ElPeruanoScraper
from .config import Config
from .logger import setup_logger
from .exceptions import (
    ScraperError,
    ElementNotFoundError,
    DownloadError,
    ConfigurationError
)

__all__ = [
    "ElPeruanoScraper",
    "Config",
    "setup_logger",
    "ScraperError",
    "ElementNotFoundError",
    "DownloadError",
    "ConfigurationError",
]