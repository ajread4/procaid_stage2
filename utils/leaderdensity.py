import pandas as pd
import networkx as nx
import json
import os
import numpy as np
from operator import itemgetter
from itertools import combinations

class LeaderDensity():
    def __init__(self,verbose):
        # Data Ingestion Variables
        self.json_data = []  # the input data in list form
        self.json_folder = []  # the input data files if provided as a data directory

        # Graph Specific Variables
        self.nodes = []  # the list node types requested by the user
        self.edges = []  # the list of edge types requested by the user
        self.Graph= nx.Graph()
        self.keymap = []  # a list that holds the keys for each node
        self.GraphDB=pd.DataFrame()
        self.edgesattr = []  # edge attributes

        # Graph Analysis Measures
        self.leadership_value = 0  # leadership value of a graph
        self.density_value = 0  # density value of a graph
        self.inv_leadership_value = 0  # inverse leadership value of a graph
        self.inv_density_value = 0  # inverse density value of a graph

        # Utility variables
        self.verbose=verbose

    # Ingest file for graph creation using JSON loads and Pandas DataFrames
    # Input: filepath - absolute location of the file path
    # Ouput: None
    def ingest_file(self, filepath):
        if self.verbose:
            print(f"Beginning ingestion of data at file {filepath}")
        for l in open(filepath).readlines():
            self.json_data.append(json.loads(l))
        self.GraphDB = pd.DataFrame(self.json_data)

    # Ingest folder containing files for graph creation
    # Input: folderpath - absolute location of the folder
    # Output: None
    def ingest_folder(self, folderpath):
        if self.verbose:
            print(f"Beginning ingestion of data at folder {folderpath}")
        for (root, directory, files) in sorted(os.walk(folderpath)):
            if files:
                for f in files:
                    self.json_folder.append(u'%s' % os.path.join(str(root), str(f)))
        if self.verbose:
            print(f"Done walking folder {folderpath}")
        for j in self.json_folder:
            self.ingest_file(j)
        if len(self.json_folder) == 0:
            # If the folder is really just a single file
            if self.verbose:
                print(f'{folderpath} is a single file.')
            self.ingest_file(folderpath)

    # Add weights to the nodes [Unused right now]
    # Input: input_Graph - NetworkX Graph to add node degrees to
    # Output: None
    def add_weights(self, input_Graph):
        for n in input_Graph.nodes():
            input_Graph.nodes[n]['weight'] = 1 / input_Graph.degree(n)
        if self.verbose:
            print(f'Done adding weights to node in graph')

    # Combine two entities
    # Input: first - first entity, second - second entity
    # Output: first+second - addition of the two input entities
    def combine(self, first, second):
        return first + second

    # Return the node attribute from an ID in keymap
    # Input: input_id - integer that represents the requested node ID
    # Output: the node that corresponds to that ID
    def return_nodeattr_fromid(self, input_id):
        return self.keymap[input_id]

    # Create a string that represents the node attributes placed together
    # Input: firstnode - attributes of the first node, secondnode - attributes of the second node
    # Output: string that respresnts the node attributes combined with a "--" between them
    def create_edge(self, firstnode, secondnode):
        return str(firstnode) + "--" + str(secondnode)

    # Ensure the request edges make sense, are not missing, and are not empty
    # Input: error_check - list of edges to check
    # Output: None
    def checkerrors_edge(self, error_check):
        for e in error_check:
            if str(e) == "" or str(e).split("-")[-1] == "":
                print(f'ERROR: Mission edge in input')
                quit()
            elif len(str(e).split("-")) == 1:
                print(f'ERROR: Missing node within edge in input')
                quit()

    # Ensure the nodes are columns in the Pandas DataFrame of data
    # Input: testnode - requested node to test
    # Output: None
    def checkerrors_node(self, testnode):
        # print(f'Checking the dataset and requested node to ensure compliance.')
        if testnode in list(self.GraphDB):
            if self.verbose:
                print(f'Found {testnode} in dataset')
            return True
        else:
            print(f'ERROR: Did not find node {testnode} in dataset')
            return False

    # Run error checking mechanisms on input edges
    # Input: input_edges - list of input edges in the form of Node1--Node2,Node2--Node3
    # Output: None
    def feature_check(self,input_edges):
        edgelist=input_edges.split(",")
        self.checkerrors_edge(edgelist)
        for edge in edgelist:
            n1,n2=self.split_edge(edge)
            if (self.checkerrors_node(n1)) and (self.checkerrors_node(n2)):
                self.save_edge(edge)
                if self.verbose:
                    print(f'Feature check complete')
            else:
                quit()
    # Save the edges for the graph
    # Input: good_edge - edge to save
    # Output: None
    def save_edge(self, good_edge):
        self.edges.append(good_edge)

    # Split an edge based on "-"
    # Input: input_edge - input edge
    # Output: node1 - first node in edge, node2 - second node in edge
    def split_edge(self, input_edge):
        node1 = str(input_edge).split("--")[0]
        node2 = str(input_edge).split("--")[1]
        return node1, node2

    # Create edge from two indices of nodes
    # Input: n1 - first node id, n2 - second node id
    # Output: (n1,n2) - edge created with two node ids
    def create_edge_from_ids(self, n1, n2):
        return (n1, n2)

    # Find the attributes for the node
    # Input: r - row within the Pandas DataFrame of data, requested_node - node to find attributes for
    # Output: attributes of a specific column in the Pandas DataFrame
    def return_nodevalues(self, r, requested_node):
        return getattr(r, str(requested_node))

    # Retrieve the index of the attributes of a node if already created. If not already created, add the attributes to the keymap.
    # Input: node - the specific node, attr - attributes of the node
    # Output: keymap index of the node attributes
    def add_nodehandler(self, node, attr,input_graph):
        if attr not in self.keymap:
            input_graph.add_node(len(self.keymap), props={str(node): str(attr)})
            self.keymap.append(str(attr))
        return self.keymap.index(str(attr))

    # Create Graph in GraphDB dataframe
    # Input: None
    # Output: None
    def process(self):
        for row in self.GraphDB.itertuples():
            for e in self.edges:
                n1, n2 = self.split_edge(e)
                firstnode = self.return_nodevalues(row, str(n1))
                secondnode = self.return_nodevalues(row, str(n2))
                nodeid_firstnode = self.add_nodehandler(n1, str(firstnode),self.Graph)
                nodeid_secondnode = self.add_nodehandler(n2, str(secondnode),self.Graph)
                if self.verbose:
                    print(f'Node: {firstnode} and id: {nodeid_firstnode}')
                    print(f'Node: {secondnode} and id: {nodeid_secondnode}')
                self.edgesattr.append(self.create_edge(firstnode, secondnode))
                self.Graph.add_edge(nodeid_firstnode, nodeid_secondnode)
        if self.verbose:
            print(f"Number of Training Nodes: {len(self.Graph.nodes())}")
            print(f"Number of Training Edges: {len(self.Graph.edges())}")

    # Find the leadership value of a graph
    # Input: input_Graph - a NetworkX graph to analyze
    # Output: None
    def leadership(self):
        sorted_node_degree = self.return_sorted_node_degree()
        d = 0
        deg = 0
        for x, y in list(sorted_node_degree):
            deg = sorted_node_degree[0][1] - y
            d = d + deg
        self.leadership_value = float(d / ((len(self.Graph.nodes()) * 2) * (len(self.Graph.nodes()) - 1)))

    # Find the density value of a graph
    # Input: input_Graph - a NetworkX graph to analyze
    # Output: None
    def density(self):
        self.density_value = float(nx.density(self.Graph))

    # Find the inverse leadership value of a graph
    # Input: input_Graph - a NetworkX graph to analyze
    # Output: None
    def inv_leadership(self):
        sorted_node_degree = self.return_sorted_node_degree()
        d = 0
        deg = 0
        for x, y in list(sorted_node_degree):
            deg = sorted_node_degree[0][1] - y
            d = d + deg
        self.inv_leadership_value = float(((len(self.Graph.nodes()) * 2) * (len(self.Graph.nodes()) - 1)) / d)

    # Find the inverse density value of a graph
    # Input: input_Graph - a NetworkX graph to analyze
    # Output: None
    def inv_density(self):
        self.inv_density_value = float(1 / nx.density(self.Graph))

    # Return the leadership value of the graph
    # Input: None
    # Output: None
    def return_leadership(self):
        return self.leadership_value

    # Return the density value of the graph
    # Input: None
    # Output: None
    def return_density(self):
        return self.density_value

    # Return the inverse leadership value of the graph
    # Input: None
    # Output: None
    def return_inv_leadership(self):
        return self.inv_leadership_value

    # Return the inverse density value of the graph
    # Input: None
    # Output: None
    def return_inv_density(self):
        return self.inv_density_value

    # Return a list of nodes sorted based on degree
    # Input: input_Graph - the graph to analyze and sort nodes based on degree
    # Output: a sorted dictionary of nodes and their corresponding degree, sorted largest to smallest
    def return_sorted_node_degree(self):
        sorted_degree = sorted(dict(self.Graph.degree(self.Graph.nodes())).items(), key=itemgetter(1), reverse=True)
        return sorted_degree

    # Function to create all possible combinations of input nodes
    # Input: input_nodes - list of input notes in format [node1,node2,node3...]
    # Output: None
    def combination_edges(self, input_nodes):
        combo_edges = list(combinations(input_nodes, 2))
        for e in combo_edges:
            self.save_edge(self.create_edge(e[0], e[1]))

    # Function for creating ludacris mode graph which sets the correct nodes and edges before processing
    # Input: None
    # Output: None
    def ludacris_process(self):
        self.nodes = self.GraphDB.columns
        self.combination_edges(self.nodes)