from maximum_matching import find_augmenting_path
import networkx as nx
import matplotlib.pyplot as plt
import random
random.seed(42)

def nodes_in_matching(matching):
    nodes_in_matching = set()
    for edge in matching.edges:
        nodes_in_matching.add(edge[0])
        nodes_in_matching.add(edge[1])
    return nodes_in_matching



def construct_colour_appearance_counter(G):
    colour_appearance_counter = {}
    for colour in G.graph['colour_map']:
        colour_appearance_counter[colour] = 0
    nodes_in_matching = set()
    for edge in G.graph['matching'].edges:
        nodes_in_matching.add(edge[0])
        nodes_in_matching.add(edge[1])
    for node in nodes_in_matching:
        if node != 'z':
            colour_appearance_counter[G.graph['colour_map'][node]] += 1
    return colour_appearance_counter


def create_g_prime(G, new_colour_appearance_counter):
 
    G_prime = nx.Graph()

    # ADDING NODES
    for node in G: # add all nodes of the original graph whose colour does not appear once in M 
        if node != 'z' and new_colour_appearance_counter[G.graph['colour_map'][node]] != 1:
            G_prime.add_node(node)
    for node in nodes_in_matching(G.graph['matching']): # add all nodes of M whose colour appears once in M
        if node != 'z' and new_colour_appearance_counter[G.graph['colour_map'][node]] == 1:
            G_prime.add_node(node)
    G_prime.add_node('z') # add extra node z

    # ADDING EDGES
    for edge in G.edges: # add any edges of the original graph that are induced in the new graph
        if edge[0] != 'z' and edge[1] != 'z' and edge[0] in G_prime.nodes and edge[1] in G_prime.nodes:
            G_prime.add_edge(*edge)
    for node in G_prime.nodes: # add an edge from z to all images of matched nodes from the original graph whose colour does not appear once in M
        if node != 'z' and node in nodes_in_matching(G.graph['matching']) and new_colour_appearance_counter[G.graph['colour_map'][node]] != 1:
            G_prime.add_edge('z', node)

    G_prime.graph['colour_map'] = G.graph['colour_map']
    G_prime.graph['matching'] = G.graph['matching']
    G_prime.graph['marked_nodes'] = []
    G_prime.graph['marked_edges'] = []
    return G_prime

def current_num_colours_in_matching(G):
    colours = set()
    for node in nodes_in_matching(G.graph['matching']):
        if node != 'z':
            colours.add(G.graph['colour_map'][node])
    return len(colours)

# An alternative function to find an augmenting path ~ note it is very slow
'''
def find_augmenting_path_max_size(_G_):
    nodes_in_matching = set()
    for edge in _G_.graph['matching'].edges():
        nodes_in_matching.add(edge[0])
        nodes_in_matching.add(edge[1])
    longest_augmenting_path = []
    for node in list(_G_.nodes()):
        if node in nodes_in_matching:
            continue
        for node2 in list(_G_.nodes()):
            if node2 in nodes_in_matching or node2 == node:
                continue 
            paths = nx.all_simple_paths(_G_, node, node2)
            for path in map(nx.utils.pairwise, paths):
                broken = False
                path = list(path)
                if len(path) % 2 == 0:
                    continue
                if len(path) == 1 and len(longest_augmenting_path) == 0 and path[-1] not in _G_.graph['matching'].edges():
                    longest_augmenting_path = path
                    continue
                for i in range(1, len(path)-1, 2):
                    if not (path[i] in _G_.graph['matching'].edges() and path[i-1] not in _G_.graph['matching'].edges()):
                        broken = True
                        break
                if len(path) > len(longest_augmenting_path) and not broken and path[-1] not in _G_.graph['matching'].edges():
                    longest_augmenting_path = path
    return longest_augmenting_path
    '''





def find_max_colourful_matching(G):
    while True:
        new_colour_appearance_counter = construct_colour_appearance_counter(G)
        G_prime = create_g_prime(G, new_colour_appearance_counter)
        path = find_augmenting_path(G_prime)
        if not path or (len(path) == 1 and (path[0][0] == 'z' or path[0][1] == 'z')):
            return [G.graph['matching'], current_num_colours_in_matching(G)]
        else:
            # Update the matching associated to G
            previous_num_colours_in_matching = current_num_colours_in_matching(G)
            for edge in path:
                if edge[0] == 'z' or edge[1] == 'z':
                    continue
                if G.graph['matching'].has_edge(*edge):
                    G.graph['matching'].remove_edge(*edge)
                else:
                    G.graph['matching'].add_edge(*edge)
            if current_num_colours_in_matching(G) < previous_num_colours_in_matching:
                print('Error - case 0')
                exit()
            elif current_num_colours_in_matching(G) == previous_num_colours_in_matching:
                return [G.graph['matching'], current_num_colours_in_matching(G)]
