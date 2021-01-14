import os
import sys
import json
import copy

def make_position(nodes, e1, e2):
    new_nodes = []
    e1_loc = int(nodes[e1][1])
    e2_loc = int(nodes[e2][1])
    for idx in range(len(nodes)):
        word = nodes[idx][0]
        postag = nodes[idx][2]
        deptag = nodes[idx][4]
        position1 = e1_loc - int(nodes[idx][1])
        position2 = e2_loc - int(nodes[idx][1])
        head = nodes[idx][3] - 1
        new_nodes.append([word, postag, deptag, position1, position2, head])
    return new_nodes

def find_path_to_root(nodes, e_idx):
    path = []
    idx = nodes[e_idx][5]
    while(idx != -1):
        path.append(idx)
        idx = nodes[idx][5]
    return path

def get_shortest_path(e1_path, e2_path):
    if len(e1_path) == 0 and len(e2_path) == 0:
        return []
    elif len(e1_path) == 0:
        return e2_path
    elif len(e2_path) == 0:
        return e1_path
    else:
        for i in range(len(e1_path)):
            for j in range(len(e2_path)):
                if e1_path[i] == e2_path[j]:
                    return e1_path[:i+1] + e2_path[:j+1]
                else:
                    None
        print('error')

def find_shortest_nodes(nodes, e1, e2):
    shortest_nodes = []
    e1_to_root = find_path_to_root(nodes, e1)
    e2_to_root = find_path_to_root(nodes, e2)
    shortest_path = get_shortest_path(e1_to_root, e2_to_root)
    shortest_path = list(set(shortest_path))
    shortest_path.sort()
    for idx in shortest_path:
        node = copy.deepcopy(nodes[idx])
        shortest_nodes.append(node)
    return shortest_nodes

def remove_head(nodes):
    for idx in range(len(nodes)):
        del nodes[idx][5]
    return nodes

def make_sequences(data, parsed_data):
    new_data = {}
    for key in list(data.keys()):
        new_data[key] = {}
        e1 = data[key]['e1_index']
        e2 = data[key]['e2_index']
        ddi = data[key]['bdi']
        sid = key[:key.rfind('.')]
        node_list = parsed_data[sid]
        node_list = make_position(node_list, e1, e2)
        shortest = find_shortest_nodes(node_list, e1, e2)
        node_list = remove_head(node_list)
        shortest = remove_head(shortest)
        new_data[key]['seq1'] = node_list[:e1]
        new_data[key]['e1'] = [node_list[e1]]
        new_data[key]['seq2'] = node_list[e1+1:e2]
        new_data[key]['e2'] = [node_list[e2]]
        new_data[key]['seq3'] = node_list[e2+1:]
        new_data[key]['shortest'] = shortest
        new_data[key]['bdi'] = ddi
    return new_data

def word_to_index(data, word_index):
    key2s = ['seq1', 'seq2', 'seq3', 'e1', 'e2', 'shortest']
    for key in list(data.keys()):
        for key2 in key2s:
            for idx in range(len(data[key][key2])):
                try:
                    data[key][key2][idx][0] = word_index[data[key][key2][idx][0]]
                except:
                    data[key][key2][idx][0] = 'N'
    return data

def get_embedding_data(data, node_idx):
    new_data = []
    for key in list(data.keys()):
        nodes = data[key]
        text = ''
        for node in nodes:
            text += str(node[node_idx]) + ' '
        text = text[:-1]
        new_data.append(text)
    return new_data

if __name__ == '__main__':
    with open('../preprocessing/word_index.json', 'r') as json_file:    
        word_index = json.load(json_file)
    with open('../preprocessing/data.json', 'r') as json_file:    
        data = json.load(json_file)
    with open('../parsing/parsed_data.json', 'r') as json_file:    
        parsed_data = json.load(json_file)

    word_data = get_embedding_data(parsed_data, 0)
    pos_data = get_embedding_data(parsed_data, 2)
    dep_data = get_embedding_data(parsed_data, 4)

    data = make_sequences(data, parsed_data)
    data = word_to_index(data, word_index)

    with open('./word_data.json', 'w') as json_file:
        json.dump(word_data, json_file, indent=4, sort_keys=True)
    with open('./pos_data.json', 'w') as json_file:
        json.dump(pos_data, json_file, indent=4, sort_keys=True)
    with open('./dep_data.json', 'w') as json_file:
        json.dump(dep_data, json_file, indent=4, sort_keys=True)
    with open('./data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4, sort_keys=True)

