# -*- coding: utf-8 -*-
import json
import re
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# constants
NAME = 'Business Name'
OWNER = 'Owner'
REG_AGENT = 'Registered Agent'
COM_REG_AGENT = 'Commercial Registered Agent'

DETAILS = [NAME, OWNER, REG_AGENT, COM_REG_AGENT]


def handle_data(data):
    '''
    Reads the JSON, extracts Business Name, Owner, Registered Agent,
    and Commercial Registered Agent, then stores them as tuples
    (i.e. name, category) in set of nodes and edges.
    Returns nodes, edges
    @param {JSON object} d
    '''
    nodes = set()
    edges = set()
    for _, v in data.items():
        business_name = clean(v[NAME])
        for category in DETAILS[1:]:
            if category in v:
                person = clean(v[category])
                nodes.add((person, category))  # (name, category)
                edges.add(((person, category), (business_name, NAME)))
    return nodes, edges


def clean(s):
    '''
    Makes a mild effort to clean names
    Returns a cleaner version of s
    @param {str} s
    '''
    ss = s.split('\n')
    s = ss[0]
    s = re.sub('[!@#$.-]', '', s)
    s = s.upper().strip()
    return s


def plot_data(nodes, edges):
    '''
    Uses networkx to plot a set of nodes, connecting them using a set of edges.
    Saves the plot as xbusinesses.png.
    @param {set} nodes - set of nodes
    @param {set} edges - set of edges
    '''
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)
    cm = {
        NAME: 'mediumseagreen',
        COM_REG_AGENT: 'salmon',
        REG_AGENT: 'orchid',
        OWNER: 'slateblue'
    }
    legend_handles = [mpatches.Patch(color=cm[x], label=x) for x in DETAILS]
    C = (G.subgraph(c) for c in nx.connected_components(G))
    for g in C:
        colormap = [cm[x[1]] for x in g.nodes]
        nx.draw(g,
                pos=pos,
                node_size=40,
                node_color=colormap,
                with_labels=False)
    plt.legend(handles=legend_handles, loc='upper right')
    plt.title('Active Businesses Starting with X')
    plt.savefig('xbusinesses.png')


if __name__ == '__main__':
    with open('XSPider_data.json') as f:
        data = json.load(f)
    nodes, edges = handle_data(data)
    plot_data(nodes, edges)
