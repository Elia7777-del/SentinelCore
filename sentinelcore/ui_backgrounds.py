"""Cyber-themed backgrounds for SentinelCore Streamlit pages."""
from pathlib import Path
import base64
import streamlit as st

ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"

BACKGROUND_MAP = {
    "dashboard": "cyber-bg.svg",
    "network": "network-bg.svg",
    "threats": "threat-bg.svg",
    "ai": "ai-bg.svg",
    "incidents": "incident-bg.svg",
    "soc": "soc-bg.svg",
    "forensics": "forensics-bg.svg",
    "vulnerability": "vulnerability-bg.svg",
    "assets": "assets-bg.svg",
    "reports": "reports-bg.svg",
}

def set_background(section="dashboard"):
    filename = BACKGROUND_MAP.get(section, BACKGROUND_MAP["dashboard"])
    image = base64.b64encode((ASSET_DIR / filename).read_bytes()).decode("ascii")
    css = (ASSET_DIR / "sentinelcore.css").read_text(encoding="utf-8")
    css = css.replace('url("../assets/cyber-bg.svg")', f'url("data:image/svg+xml;base64,{image}")')
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown('<div class="sc-scanline"></div>', unsafe_allow_html=True)

def cyber_header(title, subtitle, status="● SYSTEM ONLINE"):
    st.markdown(f"""
    <div class="cyber-panel">
      <div class="cyber-title">{title}</div>
      <div class="cyber-subtitle">{subtitle}</div>
      <br><span class="status-online">{status}</span>
    </div>
    """, unsafe_allow_html=True)
