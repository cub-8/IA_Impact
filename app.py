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

#1.4
st.subheader("Promedio de uso diario por género o nivel de educación")

st.write("Selecciona el grupo para comparar el promedio de horas de uso diario de IA")
gender = st.checkbox("Género", value=True)
education = st.checkbox("Nivel de Educación")

mean = df["Daily_Usage_Hours"].mean()

if gender and education:
    gender_education = df.groupby(["Education_Level", "Gender"])["Daily_Usage_Hours"].mean().unstack()
    st.bar_chart(gender_education)
elif gender:
    gender_education = df.groupby("Gender")["Daily_Usage_Hours"].mean()
    st.bar_chart(gender_education)
elif education:
    gender_education = df.groupby("Education_Level")["Daily_Usage_Hours"].mean()
    st.bar_chart(gender_education)
else:
    st.write("El promedio de horas de uso diario de IA es:", mean)

#1.5
st.subheader("Comparación del impacto de la IA en las calificaciones por ciudad")

cities = st.multiselect("Selecciona las ciudades para comparar", df["City"].unique())

if cities:
    cities_impact = df[df["City"].isin(cities)].groupby(["City", "Impact_on_Grades"]).size().unstack(fill_value=0)
    st.bar_chart(cities_impact[["Improved"]])
else:
    st.info("Selecciona al menos una ciudad para ver la comparación.")

#Conclusiones
st.subheader("Conclusiones")

st.markdown("""
**1. El uso determina el impacto académico**  
Los estudiantes que utilizan IA para investigar, resolver problemas o mejorar
su comprensión de los temas muestran una mejora en sus califcaciones, mientras
que los que ocupan estas herramientas para entretenimiento o automatizar tareas
no muestran tal mejora, sugiriendo que el cómo se usa la IA es crucial
en el rendimiento académico.
            
**2. Alta satisfacción no garantiza mejor rendimiento.**  
Un grupo significativo de estudiantes menciona estar muy satisfechos con el uso de IA 
a pesar de experimentar una ligera disminución en sus calificaciones, sugiriendo 
que la utilidad de la IA no solo se enfoca en los resultados académicos, 
también puede estar relacionada con otras cosas.

**3. El impacto de la IA varía según el entorno geográfico y educativo.**  
Las diferencias entre ciudades respecto al porcentaje de estudiantes que 
muestran mejora en sus calificaciones con IA muestran que el entorno de los
estudiantes influye en cómo los estudiantes ocupan estas herramientas.
""")