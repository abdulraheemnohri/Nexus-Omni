import networkx as nx
from pyvis.network import Network
import os
from modules.utils import get_logger

logger = get_logger("Graph")

class GraphManager:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.graph = nx.MultiDiGraph()
        self.output_path = "modules/templates/graph_view.html"

    def refresh_from_memory(self):
        edges = self.memory_manager.get_graph_data()
        self.graph.clear()
        for source, target, relation in edges:
            self.graph.add_edge(source, target, label=relation)
        logger.info(f"Refreshed graph with {len(edges)} edges.")

    def generate_visualization(self):
        self.refresh_from_memory()
        net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", directed=True)

        # Add nodes and edges to pyvis network
        for node in self.graph.nodes():
            net.add_node(node, label=node, color="#4CAF50")

        for u, v, data in self.graph.edges(data=True):
            net.add_edge(u, v, label=data['label'], color="#888888")

        net.save_graph(self.output_path)
        logger.info(f"Generated graph visualization at {self.output_path}")

    def add_relation(self, source, target, relation):
        self.memory_manager.add_graph_edge(source, target, relation)
        self.refresh_from_memory()
