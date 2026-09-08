#se debe tener esta libreria descargada para que funcione pip install networkx numpy matplotlib


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def crear_grafo_logistica():
    # Grafo no dirigido que representa puntos de entrega
    G = nx.Graph()
    
    # Nodos: Puntos estratégicos
    nodos = ["Centro D.", "Bodega Norte", "Tienda A", "Tienda B", "Cliente X"]
    G.add_nodes_from(nodos)
    
    # Aristas con distancias (km)
    conexiones = [
        ("Centro D.", "Bodega Norte", 5),
        ("Centro D.", "Tienda A", 3),
        ("Centro D.", "Tienda B", 4),
        ("Bodega Norte", "Tienda A", 6),
        ("Tienda A", "Tienda B", 2),
        ("Tienda B", "Cliente X", 3),
        ("Cliente X", "Centro D.", 7)
    ]
    G.add_weighted_edges_from(conexiones)
    return G

def analizar_grafo(G):
    nodos = list(G.nodes())
    
    # 1. Matriz de Adyacencia
    matriz_adyacencia = nx.to_numpy_array(G, dtype=int)
    
    print("=== MATRIZ DE ADYACENCIA ===")
    print("Nodos:", nodos)
    print(matriz_adyacencia)
    print("\n" + "="*30 + "\n")

    # 2. Validación Camino / Ciclo Euleriano
    # Euleriano: Recorrer todas las ARISTAS exactamente una vez.
    es_euleriano = nx.is_eulerian(G)
    tiene_camino_euler = nx.has_eulerian_path(G)
    
    # 3. Validación Camino / Ciclo Hamiltoniano
    # Hamiltoniano: Recorrer todos los NODOS exactamente una vez.
    # Un grafo completo o con ciertas condiciones de grado suele tener ciclo hamiltoniano.
    # Implementación manual de búsqueda por backtracking:
    def buscar_camino_hamiltoniano(grafo):
        n = len(grafo.nodes())
        nodos_lista = list(grafo.nodes())
        
        def es_valido(v, pos, camino):
            if not grafo.has_edge(camino[pos - 1], v):
                return False
            if v in camino:
                return False
            return True

        def resolver_hamilton(camino, pos):
            if pos == n:
                return True
            for v in nodos_lista:
                if es_valido(v, pos, camino):
                    camino[pos] = v
                    if resolver_hamilton(camino, pos):
                        return True
                    camino[pos] = None
            return False

        for inicio in nodos_lista:
            camino = [None] * n
            camino[0] = inicio
            if resolver_hamilton(camino, 1):
                return True, camino
        return False, []

    tiene_hamilton, camino_hamilton = buscar_camino_hamiltoniano(G)
    
    # Verificar si es ciclo Hamiltoniano
    es_ciclo_hamilton = False
    if tiene_hamilton and G.has_edge(camino_hamilton[-1], camino_hamilton[0]):
        es_ciclo_hamilton = True

    # 4. Evaluación de resultados
    cumple_euler = es_euleriano or tiene_camino_euler
    cumple_hamilton = tiene_hamilton or es_ciclo_hamilton

    print("=== EVALUACIÓN EULER Y HAMILTON ===")
    if cumple_euler:
        if es_euleriano:
            print("- Cumple con: CICLO EULERIANO (Recorre todas las aristas y regresa al inicio).")
        else:
            print("- Cumple con: CAMINO EULERIANO (Recorre todas las aristas sin repetir).")
    
    if cumple_hamilton:
        if es_ciclo_hamilton:
            print(f"- Cumple con: CICLO HAMILTONIANO ({' -> '.join(camino_hamilton)} -> {camino_hamilton[0]})")
        else:
            print(f"- Cumple con: CAMINO HAMILTONIANO ({' -> '.join(camino_hamilton)})")

    if not cumple_euler and not cumple_hamilton:
        print("El grafo NO cumple con ninguna propiedad (Ni Euleriana ni Hamiltoniana).")

# 5. Visualización del Grafo
def graficar_grafo(G):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    
    # Dibujar nodos y aristas
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, width=2, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    
    # Etiquetas de peso (distancias)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{w} km" for (u, v), w in labels.items()})
    
    plt.title("Red de Logística Urbano - Grafo de Entregas")
    plt.axis("off")
    plt.show()

# Ejecución
if __name__ == "__main__":
    G = crear_grafo_logistica()
    analizar_grafo(G)
    graficar_grafo(G)
