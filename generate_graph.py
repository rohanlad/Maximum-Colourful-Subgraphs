import networkx as nx
import random
from random import randrange
import matplotlib.colors as mcolors
random.seed(42)


colour_dict_less_15 = ['red', 'blue', 'yellow', 'pink', 'orange', 'purple', 'white', 'grey', 'aqua', 'lightskyblue', 'maroon', 'goldenrod', 'olive', 'indigo', 'tan']
colour_dict = list(mcolors.CSS4_COLORS)

def generate_graph(num_dominating, num_isolating, num_colours, fixed_num_vertices=0, desired_num_edges=0, offset=0, colouring=True):

    if fixed_num_vertices != 0:
        num_nodes = fixed_num_vertices
    else:
        num_nodes = num_dominating + num_isolating
        if num_dominating < 1:
            print('Error: number of dominating vertices must be at least 1')
            exit()
    if num_colours > num_nodes:
        print('Error: number of colours cannot be greater than number of nodes')
        exit()
    if num_colours < 15:
        colours_to_use = colour_dict_less_15[:num_colours]
    else:
        colours_to_use = colour_dict[:num_colours]
    while True:
        already_set_dom_and_iso = False
        G = nx.Graph()
        if fixed_num_vertices != 0:
            if desired_num_edges == 0:
                num_dominating = randrange(2, fixed_num_vertices)
                num_isolating = fixed_num_vertices - num_dominating
            else:
                G.graph['dominating_vertices'] = (random.choices([True, False], weights=(1-offset, offset), k=(fixed_num_vertices-2)))
                G.graph['dominating_vertices'].append(True)
                G.graph['dominating_vertices'] = [False] + G.graph['dominating_vertices']
                num_dominating = G.graph['dominating_vertices'].count(True)
                already_set_dom_and_iso = True
        if not already_set_dom_and_iso:
            G.graph['dominating_vertices'] = [None] * num_nodes
            G.graph['dominating_vertices'][0] = False
            G.graph['dominating_vertices'][num_nodes-1] = True
            dominating_vertices_to_add = num_dominating - 1
            while dominating_vertices_to_add > 0:
                random_index_ = randrange(num_nodes-1)
                if G.graph['dominating_vertices'][random_index_] == None:
                    G.graph['dominating_vertices'][random_index_] = True
                    dominating_vertices_to_add = dominating_vertices_to_add - 1
            for i in range(0, len(G.graph['dominating_vertices'])):
                if G.graph['dominating_vertices'][i] == None:
                    G.graph['dominating_vertices'][i] = False
        count = 0
        for type in G.graph['dominating_vertices']:
            if type == False:
                G.add_node(count)
                count += 1
            elif type == True:
                G.add_node(count)
                count += 1
                for n in list(G.nodes()):
                    if n != (count-1):
                        G.add_edge((count-1), n)
        if len(G.edges()) <= 1:
            # print('------case1')
            continue
        if num_dominating == 2 and G.graph['dominating_vertices'][0] and G.graph['dominating_vertices'][num_nodes-1]: # no cycle exists in this graph
            # print('------case2')
            continue
        if desired_num_edges != 0 and G.number_of_edges() != desired_num_edges:
            # print('------case3')
            # print(desired_num_edges)
            # print(G.number_of_edges())
            continue
        if colouring:
            G.graph['colour_map'] = [None] * num_nodes
            for colour in colours_to_use:
                while True:
                    random_index = randrange(num_nodes)
                    if G.graph['colour_map'][random_index] == None:
                        G.graph['colour_map'][random_index] = colour
                        break
            for j in range(0, len(G.graph['colour_map'])):
                if G.graph['colour_map'][j] == None:
                    G.graph['colour_map'][j] = random.choice(colours_to_use)
        return G



def generate_graph_2(num_colours, desired_num_edges, min_node_count=0, max_node_count=0):
    colours_to_use = colour_dict[:num_colours]
    while True:
        num_dominating = random.randrange(1, min_node_count)
        num_isolating = random.randrange((min_node_count-num_dominating), (max_node_count-num_dominating+1))
        num_nodes = num_dominating + num_isolating
        if num_colours > num_nodes:
            print('Error: number of colours cannot be greater than number of nodes')
            exit()
        G = nx.Graph()
        G.graph['dominating_vertices'] = [None] * num_nodes
        G.graph['dominating_vertices'][0] = False
        G.graph['dominating_vertices'][num_nodes-1] = True
        dominating_vertices_to_add = num_dominating - 1
        while dominating_vertices_to_add > 0:
            random_index_ = randrange(num_nodes-1)
            if G.graph['dominating_vertices'][random_index_] == None:
                G.graph['dominating_vertices'][random_index_] = True
                dominating_vertices_to_add = dominating_vertices_to_add - 1
        for i in range(0, len(G.graph['dominating_vertices'])):
            if G.graph['dominating_vertices'][i] == None:
                G.graph['dominating_vertices'][i] = False

        count = 0
        for type in G.graph['dominating_vertices']:
            if type == False:
                G.add_node(count)
                count += 1
            elif type == True:
                G.add_node(count)
                count += 1
                for n in list(G.nodes()):
                    if n != (count-1):
                        G.add_edge((count-1), n)
        if len(G.edges()) <= 1:
            continue
        if num_dominating == 2 and G.graph['dominating_vertices'][0] and G.graph['dominating_vertices'][num_nodes-1]: # no cycle exists in this graph
            continue
        if desired_num_edges != 0 and abs(G.number_of_edges() - desired_num_edges) > 100:
            # print('------case3')
            # print(desired_num_edges)
            # print(G.number_of_edges())
            continue
        G.graph['colour_map'] = [None] * num_nodes
        for colour in colours_to_use:
            while True:
                random_index = randrange(num_nodes)
                if G.graph['colour_map'][random_index] == None:
                    G.graph['colour_map'][random_index] = colour
                    break
        for j in range(0, len(G.graph['colour_map'])):
            if G.graph['colour_map'][j] == None:
                G.graph['colour_map'][j] = random.choice(colours_to_use)
        return G
