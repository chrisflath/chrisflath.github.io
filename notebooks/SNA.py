import marimo

__generated_with = "0.14.9"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Social Network Analysis with networkx""")
    return


@app.cell
def _():
    import pandas as pd
    import marimo as mo
    import networkx as nx
    import plotly.graph_objects as go
    import random
    return go, mo, nx, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Load Datasets""")
    return


@app.cell
def _(nx):
    # Load the Les Miserables graph
    graph_lm = nx.les_miserables_graph()


    return (graph_lm,)


@app.cell
def _(nx, pd):
    # Load the node ID mapping
    id_map_url = "https://raw.githubusercontent.com/efekarakus/potter-network/refs/heads/master/data/characters.csv"
    id_map_df = pd.read_csv(id_map_url)

    # Create a mapping dictionary
    node_id_mapping = dict(zip(id_map_df['id'], id_map_df['name']))

    # Load the network data (assuming it's in a format suitable for nx.from_pandas_edgelist)
    network_url = "https://raw.githubusercontent.com/efekarakus/potter-network/refs/heads/master/data/relations.csv"
    network_df = pd.read_csv(network_url)

    # Create the graph from the dataframe
    numeric_graph = nx.from_pandas_edgelist(network_df, 'source', 'target', edge_attr='type', create_using=nx.Graph())


    return node_id_mapping, numeric_graph


@app.cell
def _(graph_lm, node_id_mapping, numeric_graph, nx, pd):
    graph_data = {}


    # Relabel the nodes using the mapping
    hp_graph = nx.relabel_nodes(numeric_graph, node_id_mapping)
    graph_data["Harry Potter"] = hp_graph

    url = "https://raw.githubusercontent.com/mathbeveridge/asoiaf/refs/heads/master/data/asoiaf-all-edges.csv"
    df = pd.read_csv(url)
    graph_got = nx.from_pandas_edgelist(df, 'Source', 'Target', edge_attr='weight', create_using=nx.Graph())


    # Define URLs for each Got book
    urls = {
        "Game of Thrones Book 1": "https://raw.githubusercontent.com/mathbeveridge/asoiaf/refs/heads/master/data/asoiaf-book1-edges.csv",
        "Game of Thrones Book 2": "https://raw.githubusercontent.com/mathbeveridge/asoiaf/refs/heads/master/data/asoiaf-book2-edges.csv",
        "Game of Thrones Book 3": "https://raw.githubusercontent.com/mathbeveridge/asoiaf/refs/heads/master/data/asoiaf-book3-edges.csv",
        "Game of Thrones Book 4": "https://raw.githubusercontent.com/mathbeveridge/asoiaf/refs/heads/master/data/asoiaf-book4-edges.csv",
        "Game of Thrones Book 5": "https://raw.githubusercontent.com/mathbeveridge/asoiaf/refs/heads/master/data/asoiaf-book5-edges.csv"
    }

    # Create graphs from the datasets
    for book, url in urls.items():
        df = pd.read_csv(url)
        graph_data[book] = nx.from_pandas_edgelist(df, 'Source', 'Target', edge_attr='weight', create_using=nx.Graph())

    # Add Les Miserables graph
    graph_data["Les Miserables"] = graph_lm

    # Add the complete Game of Thrones graph
    graph_data["Game of Thrones Complete"] = graph_got
    return (graph_data,)


@app.cell
def _(graph_data, mo):
    bookSelector = mo.ui.dropdown(graph_data, value="Les Miserables")

    return (bookSelector,)


@app.cell
def _(bookSelector):
    bookSelector
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Base Stats and Visualization""")
    return


@app.cell
def _(bookSelector):

    graph = bookSelector.value
    return (graph,)


@app.cell
def _(graph, mo):
    mo.vstack([
    mo.md(f"Number of nodes: {graph.number_of_nodes()}"),
    mo.md(f"Number of edges: {graph.number_of_edges()}")])
    return


@app.cell
def _(mo):
    topNChooser = mo.ui.slider(start = 10, stop = 200, step = 5, value = 10, label = "Number of Top Characters to Plot")
    return (topNChooser,)


@app.cell
def _(bookSelector, degree_centrality, go, graph, mo, nx, topNChooser):
    # Number of top characters to display
    top_n = topNChooser.value

    # Get the top N characters based on degree centrality
    top_characters = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:top_n]

    # Create a subgraph with only the top characters and their edges
    subgraph = graph.subgraph(top_characters)

    # Get node positions using a layout algorithm for the subgraph
    pos = nx.spring_layout(subgraph)

    # Extract node positions
    x_nodes = [pos[node][0] for node in subgraph.nodes()]
    y_nodes = [pos[node][1] for node in subgraph.nodes()]

    # Create edge traces for Plotly
    edge_x = []
    edge_y = []
    for edge in subgraph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node trace for Plotly
    node_trace = go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        marker=dict(
            size=10,
            color='skyblue',
            line=dict(width=2)
        ),
        text=list(subgraph.nodes()),
        textposition="top center",
        hoverinfo="text"
    )

    # Create the figure and layout
    _plot = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f"{bookSelector.selected_key} Character Network (Top {top_n} Characters)",
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        width=1100
                    ))

    plot = mo.ui.plotly(_plot)

    return edge_trace, plot, pos, subgraph, top_characters, top_n


@app.cell
def _(mo, plot, topNChooser):
    mo.vstack([topNChooser,plot])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Centrality""")
    return


@app.cell
def _(graph, nx):
    # Degree Centrality
    degree_centrality = nx.degree_centrality(graph)
    top_5_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 Characters by Degree Centrality:")
    for _character, _centrality in top_5_degree:
        print(f"{_character}: {_centrality:.2f}")

    return (degree_centrality,)


@app.cell
def _(graph, nx):
    # Betweenness Centrality
    betweenness_centrality = nx.betweenness_centrality(graph, normalized=True)
    top_5_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 Characters by Betweenness Centrality:")
    for _character, _centrality in top_5_betweenness:
        print(f"{_character}: {_centrality:.2f}")

    return (betweenness_centrality,)


@app.cell
def _(graph, nx):
    # Closeness Centrality
    closeness_centrality = nx.closeness_centrality(graph)
    top_5_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 Characters by Closeness Centrality:")
    for _character, _centrality in top_5_closeness:
        print(f"{_character}: {_centrality:.2f}")

    return (closeness_centrality,)


@app.cell
def _(betweenness_centrality, closeness_centrality, degree_centrality, pd):
    centrality_df = pd.DataFrame({
            "Character": list(degree_centrality.keys()),
            "Degree Centrality": list(degree_centrality.values()),
            "Betweenness Centrality": [betweenness_centrality[node] for node in degree_centrality.keys()],
            "Closeness Centrality": [closeness_centrality[node] for node in degree_centrality.keys()]
    })
    centrality_df

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Graph Metrics""")
    return


@app.cell
def _(graph, nx):
    # Network Density
    graph_density = nx.density(graph)
    print(f"Graph Density: {graph_density:.4f}")

    return


@app.cell
def _(graph, nx):
    # Graph Diameter
    # Note: Diameter can only be calculated for connected components, so we find the largest connected component
    if nx.is_connected(graph):
        graph_diameter = nx.diameter(graph)
        print(f"Graph Diameter: {graph_diameter}")
    else:
        # If the graph is not connected, find the diameter of the largest connected component
        largest_cc = max(nx.connected_components(graph), key=len)
        _subgraph = graph.subgraph(largest_cc)
        graph_diameter = nx.diameter(_subgraph)
        print(f"Graph Diameter (Largest Connected Component): {graph_diameter}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Communities""")
    return


@app.cell
def _(pd, subgraph):
    from networkx.algorithms import community

    # Use greedy modularity communities for community detection
    communities_generator = community.greedy_modularity_communities(subgraph)
    communities = list(communities_generator)

    # Organize communities by nodes
    community_dict = {}
    for i, community_nodes in enumerate(communities):
        for node in community_nodes:
            community_dict[node] = i  # Assign community ID to each node

    # Create a dictionary to store community members
    organized_communities = {}
    for node, community_id in community_dict.items():
        if community_id not in organized_communities:
            organized_communities[community_id] = []
        organized_communities[community_id].append(node)

    # Display communities in a dataframe
    community_df = pd.DataFrame({
        "Community": [f"Community {community_id + 1}" for community_id in organized_communities.keys()],
        "Members": [", ".join(members) for members in organized_communities.values()]
    })

    community_df
    return (organized_communities,)


@app.cell
def _(bookSelector, edge_trace, go, mo, organized_communities, pos):
    _colors = ['blue', 'red', 'green', 'orange', 'pink', 'yellow', 'purple', 'cyan', 'magenta', 'brown']
    _num_communities = len(organized_communities)

    if _num_communities > len(_colors):
        _colors = _colors * (_num_communities // len(_colors) + 1)

    # Create node traces for each community
    _node_traces = []
    for _i, _community_id in enumerate(organized_communities.keys()):
        _nodes = organized_communities[_community_id]
        _x_nodes = [pos[_node][0] for _node in _nodes]
        _y_nodes = [pos[_node][1] for _node in _nodes]
        _node_trace = go.Scatter(
            x=_x_nodes, y=_y_nodes,
            mode='markers+text',
            marker=dict(
                size=10,
                color=_colors[_i],  # Use a distinct color for each community
                line=dict(width=2)
            ),
            text=_nodes,
            textposition="top center",
            hoverinfo="text"
        )
        _node_traces.append(_node_trace)

    # Create figure
    _plot_2 = go.Figure(data=[edge_trace] + _node_traces,
                         layout=go.Layout(
                             title=f"{bookSelector.selected_key} Character Network by Community",
                             showlegend=False,
                             hovermode='closest',
                             margin=dict(b=0, l=0, r=0, t=40),
                             xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                             yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                             width=1000
                         ))

    plot_2 = mo.ui.plotly(_plot_2)
    return (plot_2,)


@app.cell
def _(mo, plot_2, topNChooser):
    mo.vstack([topNChooser,plot_2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Ego Networks""")
    return


@app.cell
def _(mo, top_characters):
    characterSelector = mo.ui.dropdown(top_characters, value=top_characters[0], label="Select Character")
    return (characterSelector,)


@app.cell
def _(go, mo, nx, top_n):
    def visualize_ego_network(graph, character):

        # Extract the ego network for the character
        ego_graph = nx.ego_graph(graph, character)

        # Create a subgraph with only the top characters from the ego network
        subgraph = ego_graph

        # Calculate the size of the subgraph (number of nodes and edges)
        num_nodes = subgraph.number_of_nodes()
        num_edges = subgraph.number_of_edges()
        print(f"Ego Network for {character} (Top {top_n} Characters):")
        print(f"Number of Nodes: {num_nodes}")
        print(f"Number of Edges: {num_edges}")

        # Get positions for nodes in the subgraph
        _pos = nx.spring_layout(subgraph, seed=42)

        # Create edge traces for Plotly
        _edge_x = []
        _edge_y = []
        for _edge in subgraph.edges():
            _x0, _y0 = _pos[_edge[0]]
            _x1, _y1 = _pos[_edge[1]]
            _edge_x += [_x0, _x1, None]
            _edge_y += [_y0, _y1, None]

        _edge_trace = go.Scatter(
            x=_edge_x, y=_edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        # Create node trace for Plotly
        _node_x = []
        _node_y = []
        _node_text = []
        for _node in subgraph.nodes():
            _x, _y = _pos[_node]
            _node_x.append(_x)
            _node_y.append(_y)
            _node_text.append(_node)  # Node label (character name)

        _node_trace = go.Scatter(
            x=_node_x, y=_node_y,
            mode='markers+text',
            marker=dict(
                size=10,
                color='skyblue',
                line=dict(width=2, color='darkblue')
            ),
            text=_node_text,
            textposition="top center",
            hoverinfo="text"
        )

        # Create the figure
        _plot = go.Figure(data=[_edge_trace, _node_trace],
                            layout=go.Layout(
                                title=f"Ego Network for {character} (Top {top_n} Characters)",
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=0, l=0, r=0, t=40),
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                width=1000, height=600
                            ))
        mo.ui.plotly(_plot)
        return _plot
    return (visualize_ego_network,)


@app.cell
def _(mo, plot_3):
    mo.hstack([plot_3])
    return


@app.cell
def _(characterSelector, graph, visualize_ego_network):
    plot_3 = visualize_ego_network(graph, characterSelector.value)
    return (plot_3,)


@app.cell
def _(characterSelector, mo, plot_3):
    mo.vstack([characterSelector,plot_3])
    return


if __name__ == "__main__":
    app.run()
