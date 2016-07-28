# Import the relevant libraries
import networkx as nx
from networkx.readwrite import json_graph
import json
import pandas as pd

# Read the edgelist as a dataframe and determine the type of nodes
df = pd.read_csv("uiucData.txt", header = None, delimiter = '\t')
df.columns = ['Department', 'People']
department = df.Department.unique()
people = df.People.unique()

# Set up the network and obtain the node degrees
G = nx.from_pandas_dataframe(df, 'Department', 'People')
d = nx.degree(G)

# Assign a scaled value for each node and its category classification
for n in G:
    G.node[n]['name'] = n
    G.node[n]['value'] = (((d[n] - min(d.values())) * (10 - 1)) / (max(d.values()) - min(d.values()))) + 1
    if n in department:
        G.node[n]['group'] = 'Department'
    else:
        G.node[n]['group'] = 'People'

# Output the node to a json
d = json_graph.node_link_data(G)
json.dump(d, open('uiuc.json','w'))