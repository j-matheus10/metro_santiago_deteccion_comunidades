 Analizador de la Red de Metro de Santiago

Este proyecto consiste en una aplicación web interactiva desarrollada con Streamlit que permite analizar la topología de la red de Metro de Santiago de Chile mediante algoritmos de detección de comunidades.
 Características principales

    Visualización Interactiva: Utiliza PyVis para renderizar el grafo de la red, permitiendo explorar las conexiones entre estaciones.

    Algoritmos de Detección: Implementación comparativa de:

        Girvan-Newman: Simulación paso a paso que permite visualizar cómo la eliminación de aristas con alta centralidad de intermediación divide la red.

        Infomap: Detección de comunidades basada en flujos de información, forzada a 4 módulos principales.

    Métricas de Red: Cálculo de Betweenness Centrality para identificar las aristas clave (puentes) que conectan diferentes sectores de la red.

    Simulación Paso a Paso: Control deslizante (slider) para visualizar la evolución del proceso de partición en tiempo real.

Tecnologías utilizadas

    Python: Lenguaje principal.

    Streamlit: Framework para la interfaz web.

    NetworkX: Para la manipulación y análisis de grafos.

    Infomap: Algoritmo para la detección de comunidades.

    PyVis: Biblioteca para la visualización interactiva.

    Pandas: Para el manejo de datos (estaciones y aristas).

    📂 Estructura del Proyecto

    ├── src/
│   ├── app.py              # Interfaz principal de Streamlit
│   ├── grafo.py            # Lógica de carga y algoritmos
│   ├── visualizacion.py    # Generación de gráficos con PyVis
│   ├── estaciones.csv      # Datos de las estaciones
│   └── aristas.csv         # Datos de las conexiones
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo

👨‍💻 Autor

Jesús Matheus, Martin Jofre Proyecto académico desarrollado para el análisis de redes complejas.
