import streamlit as st
from PIL import Image
import os

# Configuración de la página
st.set_page_config(page_title="Visualización de Gráficas del Análisis", layout="wide")
st.title("📊 Visualización del Análisis de Datos")
st.markdown("A continuación se muestran las **27 gráficas** más relevantes del análisis realizado sobre los datos de la GEIH.")

# --- Mostrar las 27 gráficas ---
st.header("🖼️ Gráficas")
image_folder = "graficas"
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith((".png"))])[:27]

cols = st.columns(3)
for i, image_name in enumerate(image_files):
    img_path = os.path.join(image_folder, image_name)
    with cols[i % 3]:
        st.image(Image.open(img_path), caption=f"Gráfica {i+1}")

st.markdown("---")

# --- Sección de Código del Notebook ---
st.header("🧠 Fragmentos de Código del Análisis")

codigo_ejemplos = [
    """# Filtrado de datos por mes
df_enero_dic = df_clean[df_clean['MES_NOMBRE'].isin(['Enero', 'Diciembre'])]""",

    """# Agrupación para comparar ingresos por sexo y mes
ingresos_comp = df_enero_dic.groupby(["MES_NOMBRE", "P3271"])["P7495"].mean().reset_index()""",

    """# Gráfico de barras con seaborn
plt.figure(figsize=(8,5))
sns.barplot(data=ingresos_comp, x="MES_NOMBRE", y="P7495", hue="P3271")
plt.title("Comparación Enero vs Diciembre")""",

    """# Evolución mensual de la brecha salarial
sns.lineplot(x=orden_meses, y=brechas, marker='o', linewidth=2.5, color='red')""",

    """# Cálculo de brecha porcentual
pivot_comp["Brecha (%)"] = ((pivot_comp["Enero"] - pivot_comp["Diciembre"]) / pivot_comp["Enero"]) * 100""",
]

for i, fragment in enumerate(codigo_ejemplos, 1):
    st.subheader(f"Fragmento {i}")
    st.code(fragment, language="python")

st.success("Fin del informe visual.")
