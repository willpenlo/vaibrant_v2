import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8002"
API_KEY = "vaibrant_sk_W9x2mP8qRkL4nX876Jxg6244jGXJXZK86253JCbcg7243jk78651Njxb76HjKSv"
HEADERS = {"x-api-key": API_KEY}

st.set_page_config(page_title="vAIbrant", layout="wide")
st.title("vAIbrant Security Dashboard")

col1, col2, col3, = st.columns(3)

stats = requests.get(f"{API_URL}/stats", headers=HEADERS).json()
total = stats.get("total_scans", 0)
by_risk = stats.get("by_risk", {})

col1.metric("Total Scans", total)
col2.metric("Critical", by_risk.get("CRITICAL", 0))
col3.metric("High Risk", by_risk.get("HIGH", 0))

st.subheader("Recent Scans")
history = requests.get(f"{API_URL}/history", headers=HEADERS).json()
scans = history.get("scans", [])

if scans:
    df = pd.DataFrame(scans)[["filename", "risk_level","lines_of_code","scanned_at"]]
    st.dataframe(df, use_container_width=True)

st.subheader("Analyze a File")
uploaded = st.file_uploader("Upload a .py or .js file", type=["py", "js", "ts"])
if uploaded:
    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            resp = requests.post(
                f"{API_URL}/analyze/upload",
                files={"file": uploaded},
                headers=HEADERS
            )
            result = resp.json()
            risk = result.get("risk_level", "UNKNOWN")
            color = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "yellow", "LOW": "green"}.get(risk, "gray")
            st.markdown(f"### Risk: :{color}[{risk}]")
            st.write(result.get("analysis",""))