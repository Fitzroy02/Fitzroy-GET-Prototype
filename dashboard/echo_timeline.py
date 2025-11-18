# Echo Timeline Viewer for GETS VI
import streamlit as st
import json

st.title("📜 Echo Timeline — GETS VI")

with open("manifest/legacy_manifest.json", "r") as f:
    archive = json.load(f)["echo_archive"]

for echo in archive:
    st.markdown(f"**{echo['timestamp']}** — *{echo['badge']}* — {echo['mood']}")
    st.markdown(f"> {echo['transmission']}")
