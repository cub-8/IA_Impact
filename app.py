import streamlit as st
import kagglehub as kh
import pandas as pd
import matplotlib.pyplot as plt

from kagglehub import KaggleDatasetAdapter

df = kh.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  "guriya79/how-ai-is-changing-student-life",
  "AI_Student_Life_Pakistan_2026.csv"
)

st.title("Impacto de la IA en la vida estudiantil en Pakistán") 

# st.write(df.head())

#1.1

city = st.selectbox("Selecciona una ciudad", ["Todas"] + list(df["City"].unique()))

bar_impact_ia = df

if city != "Todas":
    bar_impact_ia = bar_impact_ia[bar_impact_ia["City"] == city]
    st.bar_chart(bar_impact_ia.groupby(["AI_Tool_Used", "Impact_on_Grades"]).size().unstack())
else:
    st.bar_chart(bar_impact_ia.groupby(["AI_Tool_Used", "Impact_on_Grades"]).size().unstack())

