import sys
import os
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx

# Añadir ruta para importar módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from grafo import cargar_grafo, historial_girvan_newman, ejecutar_infomap
from visualizacion import generar_visualizacion_pyvis

st.set_page_config(layout="wide", page_title="Analizador Metro de Santiago")
st.title("Analizador de la Red de Metro de Santiago (L1,L2,L4 Y L5)")

# 1. Cargar el grafo (se cachea para no recargar datos al mover sliders)
@st.cache_data
def obtener_grafo():
    return cargar_grafo()

G = obtener_grafo()

# 2. Sidebar para selección
st.sidebar.header("Configuración")
algoritmo = st.sidebar.selectbox("Selecciona el algoritmo:", ["Girvan-Newman", "Infomap"])

# 3. Lógica de Simulación Paso a Paso
if algoritmo == "Girvan-Newman":
    historial = historial_girvan_newman(G)
    paso = st.sidebar.slider("Paso de la simulación:", 0, len(historial) - 1, 0)
    comunidades_actuales = historial[paso]
    comunidades = {i + 1: c for i, c in enumerate(comunidades_actuales)}
    st.write(f"### Simulación Girvan-Newman: Paso {paso}")
    st.write("El algoritmo divide el grafo eliminando las aristas con mayor intermediación.")
else:
    # Infomap no es paso a paso jerárquico natural, lo tratamos como ejecución única
    comunidades = ejecutar_infomap(G)
    st.write("### Resultados utilizando: Infomap")
    st.write("Infomap optimiza la descripción del flujo de información en la red.")

# 4. Generación y Visualización
archivo_html = 'temp_graph.html'
generar_visualizacion_pyvis(G, comunidades, output_html=archivo_html)

with open(archivo_html, 'r', encoding='utf-8') as HtmlFile:
    components.html(HtmlFile.read(), height=750)

# 5. Desglose de comunidades
st.subheader("🔍 Detalle de Comunidades Detectadas")
for id_comunidad, nodos in comunidades.items():
    titulo = f"Comunidad {id_comunidad} ({len(nodos)} estaciones)"
    with st.expander(titulo):
        st.write(f"**Estaciones:** {', '.join(sorted(nodos))}")

# 6. Métricas adicionales
st.divider()
st.subheader("Top 5 Aristas Puente (Betweenness Centrality)")
betweenness = nx.edge_betweenness_centrality(G)
aristas_top = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
for arista, valor in aristas_top:
    st.write(f"🔹 **{arista[0]}** ↔ **{arista[1]}** | Valor: `{valor:.4f}`")
