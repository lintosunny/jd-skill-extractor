import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from llm_helper import skill_extractor

# Set up page
st.set_page_config(page_title="JD Skill Extractor", layout="centered", page_icon="🔥")

# Custom styling
st.markdown("""
<style>
    body {
        background-color: #f5f7fa;
        color: #333333;
    }
    .stApp {
        font-family: 'Segoe UI', sans-serif;
        padding: 2rem;
    }
    .title {
        text-align: center;
        font-size: 2.7rem;
        font-weight: 700;
        color: #2b6777;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">JD Skill Extractor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Extract key skills from any job description and see what really matters.</div>', unsafe_allow_html=True)

# Input area
job_description = st.text_area("📄 Paste Job Description Below", height=250, placeholder="Paste the job description here...")

# Button
if st.button("🔍 Analyze"):
    with st.spinner("Analyzing job description..."):
        try:
            output_json = skill_extractor(job_description)
            df = pd.DataFrame(output_json)
            df = df.sort_values(by="importance", ascending=True)  # for bar chart

            # Chart using Plotly
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=df["importance"],
                y=df["skill"],
                orientation='h',
                marker=dict(
                    color=df["importance"],
                    colorscale='tealgrn',
                    line=dict(color='rgba(0,0,0,0)', width=1)
                ),
                hoverinfo='x+y',
                text=df["importance"].astype(str) + "%",
                textposition='outside',
            ))

            fig.update_layout(
                title="📊 Skill Importance Breakdown",
                xaxis=dict(title="Importance (%)", range=[0, 100]),
                yaxis=dict(title="Skill", automargin=True),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(family="Segoe UI", size=14),
                height=550,
                margin=dict(l=80, r=40, t=60, b=30)
            )

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error("❌ Could not extract or render skills. Please try again.")
            st.code(str(e))