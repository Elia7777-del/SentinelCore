"""SentinelCore defensive assessment utilities."""
from .network import fetch_url, scan_host
from .scan import scan_directory
__all__ = ["fetch_url", "scan_host", "scan_directory"]
