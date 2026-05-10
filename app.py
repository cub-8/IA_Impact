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

st.write(df.head())

#1.1
st.subheader("Impacto de la IA en las calificaciones por ciudad")

city = st.selectbox("Selecciona una ciudad", ["Todas"] + list(df["City"].unique()))

bar_impact_ia = df

if city != "Todas":
    bar_impact_ia = bar_impact_ia[bar_impact_ia["City"] == city]
    st.bar_chart(bar_impact_ia.groupby(["AI_Tool_Used", "Impact_on_Grades"]).size().unstack())
else:
    st.bar_chart(bar_impact_ia.groupby(["AI_Tool_Used", "Impact_on_Grades"]).size().unstack())

#1.2
st.subheader("Impacto de la IA en las calificaciones por propósito de uso")

purpose = st.radio("Selecciona el uso de IA", df["Purpose"].unique())

bar_purpose_ia = df[df["Purpose"] == purpose]

st.bar_chart(bar_purpose_ia["Impact_on_Grades"].value_counts())

#1.3
st.subheader("Alumnos con alto nivel de satisfacción y ligera disminución en las calificaciones")

high_decline = df[(df["Impact_on_Grades"] == "Slight Decline") & (df["Satisfaction_Level"] == "High")]

num_high_decline = len(high_decline)

st.write("Total de estudiantes con satisfacción alta y ligera disminución en las calificaciones:", num_high_decline)

min_hours = float(df["Daily_Usage_Hours"].min())
max_hours = float(df["Daily_Usage_Hours"].max())

hours = st.slider("Rango de horas de uso diario", min_value=min_hours, max_value=max_hours, value=(min_hours, max_hours))

high_decline_hours = high_decline[(high_decline["Daily_Usage_Hours"] >= hours[0]) & (high_decline["Daily_Usage_Hours"] <= hours[1])]

ia_students = (
    high_decline_hours["AI_Tool_Used"]
    .value_counts()
    .reset_index()
)
ia_students.columns = ["Herramienta", "Cantidad de estudiantes"]
st.dataframe(ia_students)


