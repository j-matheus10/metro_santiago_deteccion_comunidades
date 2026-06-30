from pyvis.network import Network
import networkx as nx

def generar_visualizacion_pyvis(G, comunidades, output_html='temp_graph.html'):
    from pyvis.network import Network
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', directed=False)
    net.toggle_physics(False)

    # Crear mapa de colores
    # 'comunidades' será o un diccionario {id: [nodos]} o lista de listas
    color_map = {}
    colores = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#F1C40F', '#8E44AD']
    
    # Manejar ambos formatos de entrada
    if isinstance(comunidades, dict):
        for mod_id, nodos in comunidades.items():
            color = colores[mod_id % len(colores)]
            for nodo in nodos: color_map[nodo] = color
    else: # Es lista de listas (Girvan)
        for i, nodos in enumerate(comunidades):
            color = colores[i % len(colores)]
            for nodo in nodos: color_map[nodo] = color

    for nodo in G.nodes():
        net.add_node(nodo, label=nodo, color=color_map.get(nodo, '#FFFFFF'))

    for u, v in G.edges():
        net.add_edge(u, v, color='#888888')

    net.save_graph(output_html)
    print(f"Visualización guardada en: {output_html}")

# Para probarlo:
if __name__ == "__main__":
    # Importa tu función de carga de grafo aquí
    from grafo import cargar_grafo
    G = cargar_grafo()
    generar_visualizacion_pyvis(G)
