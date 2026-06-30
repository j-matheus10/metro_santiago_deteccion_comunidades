import os
import pandas as pd
import networkx as nx
from networkx.algorithms.community import girvan_newman
from infomap import Infomap

BASE_DIR = os.path.dirname(__file__)

def cargar_grafo():
    G = nx.Graph()
    # 1. Nodos
    ruta_estaciones = os.path.join(BASE_DIR, 'estaciones.csv')
    df_estaciones = pd.read_csv(ruta_estaciones, encoding='latin-1') 
    for index, row in df_estaciones.iterrows():
        G.add_node(str(row['nombre']).strip(), linea=row['linea'], combinacion=row['combinacion'])
    # 2. Aristas
    ruta_aristas = os.path.join(BASE_DIR, 'aristas.csv')
    df_aristas = pd.read_csv(ruta_aristas, encoding='latin-1')
    for index, row in df_aristas.iterrows():
        G.add_edge(str(row['desde']).strip(), str(row['hasta']).strip())
    return G

def historial_girvan_newman(G):
    historial = []
    comp = girvan_newman(G)
    # Paso 0: El grafo completo (1 comunidad)
    historial.append([list(G.nodes())])
    # Vamos guardando cada nivel de división
    pasos_maximos = 3
    for i, comunidades in enumerate(comp):
        if i >= pasos_maximos: break
        historial.append([list(c) for c in comunidades])
    return historial

def ejecutar_infomap(G):
    # 1. ORDENAMOS para mantener el mapeo constante entre nodos e IDs
    nombres_ordenados = sorted(list(G.nodes()))
    nombre_a_id = {nombre: i for i, nombre in enumerate(nombres_ordenados)}
    id_a_nombre = {i: nombre for nombre, i in nombre_a_id.items()}

    # 2. Configuramos Infomap SIN semilla (aleatorio) pero con 4 módulos forzados
    # num_modules=4 obliga al algoritmo a encontrar la mejor partición en exactamente 4 grupos
    im = Infomap(silent=True) 

    # 3. Cargamos aristas
    for u, v in G.edges():
        im.add_link(nombre_a_id[u], nombre_a_id[v])

    # 4. Ejecutar
    im.run()

    # 5. Organizar resultados
    comunidades = {}
    for node in im.tree:
        if node.is_leaf:
            modulo_id = node.module_id
            nombre_estacion = id_a_nombre[node.node_id]
            if modulo_id not in comunidades:
                comunidades[modulo_id] = []
            comunidades[modulo_id].append(nombre_estacion)

    return comunidades

# Para pruebas rápidas en terminal
if __name__ == "__main__":
    metro_grafo = cargar_grafo()
    print(f"Grafo cargado: {metro_grafo.number_of_nodes()} nodos.")
    historial = historial_girvan_newman(metro_grafo)
    print(f"Historial Girvan-Newman generado con {len(historial)} pasos.")
