import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import numpy as np

canvas = None  # Define canvas globally
main_frame = None
G = None
description_label = None
adj_matrix_label = None

def place_brace(event, row, column):
    label = event.widget
    if label['text'] == "":
        label.config(text="↘", font=("Arial", 14))
    else:
        label.config(text="")
    update_bipartite_graph()

def generate_grid(master, rows, columns):
    global main_frame, G, canvas, description_label, adj_matrix_label
    if main_frame is not None:
        main_frame.destroy()  # Destroy the existing frame to update the grid
    main_frame = ttk.Frame(master)
    main_frame.pack(pady=20)

    # Create row labels and grid lines
    for i in range(rows + 1):
        for j in range(columns + 1):
            if i == 0 and j == 0:
                continue  # Skip label for (0, 0)
            elif i == 0:
                ttk.Label(main_frame, text=f"C{j}", borderwidth=1, relief="solid", width=10, font=("Arial", 10)).grid(row=i, column=j, sticky="nsew")
            elif j == 0:
                ttk.Label(main_frame, text=f"R{i}", borderwidth=1, relief="solid", width=10, font=("Arial", 10)).grid(row=i, column=j, sticky="nsew")
            else:
                label = ttk.Label(main_frame, text="", borderwidth=1, relief="solid", width=10, font=("Arial", 10))
                label.grid(row=i, column=j, sticky="nsew")
                label.bind("<Button-1>", lambda event, row=i, column=j: place_brace(event, row, column))

    # Description label
    description_label = ttk.Label(main_frame, text="", font=("Arial", 14, "bold"), foreground="red")
    description_label.grid(row=rows+2, column=0, columnspan=columns+1, pady=10)

    # Adjacency matrix label
    adj_matrix_label = ttk.Label(main_frame, text="", font=("Arial", 12), wraplength=500)
    adj_matrix_label.grid(row=rows+3, column=0, columnspan=columns+1, pady=10)

    # Initialize bipartite graph
    G = nx.Graph()
    for i in range(rows):
        G.add_node(f"R{i+1}", bipartite=0)
    for j in range(columns):
        G.add_node(f"C{j+1}", bipartite=1)

    # Draw bipartite graph
    draw_bipartite_graph()

    # Update description and adjacency matrix labels
    update_description()
   #update_adjacency_matrix()

def update_bipartite_graph():
    global G
    braces = []
    for widget in main_frame.winfo_children():
        if isinstance(widget, ttk.Label) and widget['text'] == "↘":
            row = widget.grid_info()['row'] - 1
            column = widget.grid_info()['column'] - 1
            braces.append((row, column))

    new_edges = [(f"R{brace[0]+1}", f"C{brace[1]+1}") for brace in braces]

    # Remove existing edges
    G.remove_edges_from(G.edges())

    # Add new edges
    G.add_edges_from(new_edges)

    draw_bipartite_graph()

def draw_bipartite_graph():
    global canvas
    fig, ax = plt.subplots()
    rows, columns = get_grid_size()
    pos = {}
    for i, node in enumerate(G.nodes()):
        if node[0] == 'R':
            if int(node[1:]) <= rows:  # Ensure only existing rows are drawn
                pos[node] = (i, 1)
        else:
            if int(node[1:]) <= columns:  # Ensure only existing columns are drawn
                pos[node] = (i - rows, -1)
    nx.draw(G, pos, ax=ax, with_labels=True, node_size=400)

    if nx.cycle_basis(G):
        cycles = nx.cycle_basis(G)
        cycle_edges = []
        for cycle in cycles:
            cycle_edges.extend([(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)])
            cycle_edges.append((cycle[-1], cycle[0]))  # Closing the cycle
        nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, edge_color='r', width=2)

    if canvas:
        canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=rows+4, column=0, columnspan=columns+1, pady=10)

    # Update description and adjacency matrix labels
    update_description()
    #update_adjacency_matrix()

def update_description():
    global description_label, G
    rows, columns = get_grid_size()

    if nx.is_connected(G) and not nx.cycle_basis(G):
        description = "The graph is rigid and optimal because it is connected and contains no cycles."
    elif nx.cycle_basis(G):
        description = f"The graph is over rigid because it contains a cycle in the bipartite graph:\n{nx.cycle_basis(G)}"
    else:
        # Find disconnected components
        disconnected_nodes = list(nx.connected_components(G))
        disconnected_info = "\nDisconnected nodes:\n"
        for component in disconnected_nodes:
            disconnected_info += f"{component}\n"
        description = f"The graph is not rigid because it has disconnected components.\n{disconnected_info}"
    description_label.config(text=description)

# def update_adjacency_matrix():
#    global G, adj_matrix_label
#    adj_matrix = nx.adjacency_matrix(G)
#    adj_matrix_str = "Adjacency Matrix:\n" + str(adj_matrix.todense())
#    adj_matrix_label.config(text=adj_matrix_str)

def get_grid_size():
    rows = len([widget for widget in main_frame.winfo_children() if isinstance(widget, ttk.Label) and widget.grid_info()['row'] == 1])
    columns = len([widget for widget in main_frame.winfo_children() if isinstance(widget, ttk.Label) and widget.grid_info()['column'] == 1])
    return rows, columns
