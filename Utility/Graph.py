

import networkx as nx

from Utility.CategoryData import category_base_structure


def create_graph_from_structure(structure, parent=None, graph=None, path=""):
    """Creates a directed graph from a nested dictionary/list structure."""
    if graph is None:
        graph = nx.DiGraph()

    if isinstance(structure, dict):
        for key, value in structure.items():
            current_path = f"{path}/{key}" if path else key
            graph.add_node(current_path, label=key)
            if parent:
                graph.add_edge(parent, current_path)
            create_graph_from_structure(value, current_path, graph, current_path)
    elif isinstance(structure, list):
        for item in structure:
            current_path = f"{path}/{item}" if path else item
            graph.add_node(current_path, label=item)
            if parent:
                graph.add_edge(parent, current_path)
    return graph


def classify_columns_with_graph(columns, graph):
    """Classifies columns using a graph structure."""
    classified_data = {"Не определено": []}
    for col in columns:
        found_node = None
        for node in graph.nodes:
            if graph.nodes[node]['label'] == col:
                found_node = node
                break

        if found_node:
            path = []
            current = found_node
            while current:
                path.insert(0, graph.nodes[current]["label"])
                parents = list(graph.predecessors(current))
                current = parents[0] if parents else None

            current_level = classified_data
            for part in path[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]

            if isinstance(current_level, dict):
                if "values" not in current_level:
                    current_level["values"] = []
                current_level["values"].append(col)
            elif isinstance(current_level, list):
                current_level.append(col)

        else:
            classified_data["Не определено"].append(col)
    return classified_data


def transform_graph_for_tree(graph, root_node=""):
    """Transforms a graph into a tree structure for streamlit-tree-select."""
    tree_data = []
    if not root_node:
        root_nodes = [node for node, degree in graph.in_degree() if degree == 0]
        if root_nodes:
            root_node = root_nodes[0]
        else:
            return []

    def recursive_build(node):
        children = list(graph.successors(node))
        tree_node = {"label": graph.nodes[node]["label"], "value": node}

        if children:
            tree_node["children"] = [recursive_build(child) for child in children]
        return tree_node

    tree_data = recursive_build(root_node)

    return [tree_data]


def graph_to_dict(graph):
    """Converts a networkx graph to a dictionary, reconstructing the original nested structure."""

    def reconstruct_structure(node):
        children = list(graph.successors(node))
        if children:
            result = {}
            for child in children:
                child_label = graph.nodes[child]["label"]
                result[child_label] = reconstruct_structure(child)
            return result
        else:
            return graph.nodes[node]["label"]

    root_nodes = [node for node, degree in graph.in_degree() if degree == 0]
    if root_nodes:
        root_node = root_nodes[0]
        return {graph.nodes[root_node]["label"]: reconstruct_structure(root_node)}
    else:
        return {}

graph = create_graph_from_structure(category_base_structure)
df_columns =[]
# Classify columns
classified_columns = classify_columns_with_graph(df_columns, graph)


#Transform Graph to tree for streamlit
transformed_data = transform_graph_for_tree(graph)

# Convert graph to dictionary
graph_dict = graph_to_dict(graph)



# st.title("Tree Select Component Example")
# selected = tree_select(transformed_data)
#
# st.write("Selected values:")
# st.write(selected)
# st.write("Классифицированные данные:")
# st.write(classified_columns)
#
# st.write("Структура графа в виде словаря:")
# st.write(graph_dict)