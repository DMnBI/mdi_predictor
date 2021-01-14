import os
import sys
import numpy as np
import json

def position_onehot(d):
    d   = int(d)
    dis_dic = { 
        -31:    [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        -21:    [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        -11:    [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        -6:     [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        -5:     [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        -4:     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
        -3:     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0],
        -2:     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
        -1:     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        0:      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        1:      [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        2:      [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
        3:      [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0],
        4:      [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0],
        5:      [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        6:      [1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        11:     [1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        21:     [1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        31:     [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        }

    if d <= -6 and d > -11:
        d = -6
    elif d <= -11 and d > -21:
        d = -11
    elif d <= -21 and d > -31:
        d = -21
    elif d <= -31:
        d = -31
    elif d >= 6 and d < 11:
        d = 6
    elif d >= 11 and d < 21:
        d = 11
    elif d >= 21 and d < 31:
        d = 21
    elif d >= 31:
        d = 31
    else:
        None
    return dis_dic[d]

def label_embedding(label):
    label   = label.lower()
    if label == 'true': 
        label = [1, 0]
    elif label == 'false': 
        label = [0, 1]
    else:
        print('error')
        exit()
    return label

def padding_error(pairs, length):
    if len(pairs) != length:
        print('padding error')
        exit()
    else:
        None

def padding_shortest(pairs, error, length):
    if len(pairs) < length:
        for cnt in range(length-len(pairs)):
            pairs.append(error)
    else:
        pairs   = pairs[:length]
    padding_error(pairs, length)
    return pairs

def padding_seq3(pairs, error, length):
    if len(pairs) < length:
        for cnt in range(length-len(pairs)):
            pairs.append(error)
    else:
        pairs   = pairs[:length]
    padding_error(pairs, length)
    return pairs

def padding_seq2(pairs, error, length):
    if len(pairs) < length:
        for cnt in range(length-len(pairs)):
            pairs.append(error)
    else:
        if length%2 == 0:
            pairs   = pairs[:int(length/2)] + pairs[len(pairs)-int(length/2):]
        else:
            pairs   = pairs[:int(length/2)+1] + pairs[len(pairs)-int(length/2):]
    padding_error(pairs, length)
    return pairs

def padding_seq1(pairs, error, length):
    if len(pairs) < length:
        for cnt in range(length-len(pairs)):
            pairs.append(error)
    else:
        pairs   = pairs[len(pairs)-length:]
    padding_error(pairs, length)
    return pairs

def padding_feature(pair):
    error = ['N', 'N', 'N', 0, 0]
    pair['seq1'] = padding_seq1(pair['seq1'], error, 60)
    pair['seq2'] = padding_seq2(pair['seq2'], error, 60)
    pair['seq3']= padding_seq3(pair['seq3'], error, 60)
    pair['shortest'] = padding_shortest(pair['shortest'], error, 12)
    return pair

def data_embedding(data, word_dict, pos_dict, dep_dict):
    seq1_w = []
    seq1_f = []
    seq2_w = []
    seq2_f = []
    seq3_w = []
    seq3_f = []
    shortest_w = []
    shortest_f = []
    entity1 = []
    entity2 = []
    label = []
    index_list = []
    key_list = []
    sid = []
    index = 0
    for key in list(data.keys()):
        index_list.append(index)
        key_list.append(key)
        pair = data[key]
        s1_w = []
        s1_f = []
        for node in pair['seq1']:
            s1_w.append(list(word_dict[node[0]]))
            s1_f.append(list(list(pos_dict[node[1]]) + list(dep_dict[node[2]]) + position_onehot(node[3]) + position_onehot(node[4])))
        s2_w = []
        s2_f = []
        for node in pair['seq2']:
            s2_w.append(list(word_dict[node[0]]))
            s2_f.append(list(list(pos_dict[node[1]]) + list(dep_dict[node[2]]) + position_onehot(node[3]) + position_onehot(node[4])))
        s3_w = []
        s3_f = []
        for node in pair['seq3']:
            s3_w.append(list(word_dict[node[0]]))
            s3_f.append(list(list(pos_dict[node[1]]) + list(dep_dict[node[2]]) + position_onehot(node[3]) + position_onehot(node[4])))
        short_w = []
        short_f = []
        for node in pair['shortest']:
            short_w.append(list(word_dict[node[0]]))
            short_f.append(list(list(pos_dict[node[1]]) + list(dep_dict[node[2]]) + position_onehot(node[3]) + position_onehot(node[4])))
        e1 = []
        for node in pair['e1']:
            e1.append(list(word_dict[node[0]]))
        e2 = []
        for node in pair['e2']:
            e2.append(list(word_dict[node[0]]))
        l = label_embedding(pair['bdi'])
        seq1_w.append(s1_w)
        seq1_f.append(s1_f)
        seq2_w.append(s2_w)
        seq2_f.append(s2_f)
        seq3_w.append(s3_w)
        seq3_f.append(s3_f)
        shortest_w.append(short_w)
        shortest_f.append(short_f)
        entity1.append(e1)
        entity2.append(e2)
        label.append(l)
        index += 1
        sid.append(key[key.find('_')+1:key.rfind('.')])
    return [seq1_w, seq1_f, seq2_w, seq2_f, seq3_w, seq3_f, shortest_w, shortest_f, entity1, entity2, label, index_list, key_list, sid]

def read_dict(word_file, pos_file, dep_file, data):
    with open(word_file, 'r') as json_file:
        word_dict = json.load(json_file)
    with open(pos_file, 'r') as json_file:
        pos_dict = json.load(json_file)
    with open(dep_file, 'r') as json_file:
        dep_dict = json.load(json_file)
    error = []
    for idx in range(200):
        error.append(0.0)
    word_dict['N'] = error 
    pos_dict['N'] = error[:10]
    dep_dict['N'] = error[:10]

    pos = []
    dep = []
    for key in list(data.keys()):
        pair = data[key]
        for node in pair['seq1']:
            pos.append(node[1])
            dep.append(node[2])
        for node in pair['seq2']:
            pos.append(node[1])
            dep.append(node[2])
        for node in pair['seq3']:
            pos.append(node[1])
            dep.append(node[2])
        for node in pair['shortest']:
            pos.append(node[1])
            dep.append(node[2])
    pos = list(set(pos))
    dep = list(set(dep))
    for p in pos:
        try:
            a = pos_dict[p]
        except:
            print(p)
            pos_dict[p] = error[:10]
    for d in dep:
        try:
            a = dep_dict[d]
        except:
            print(d)
            dep_dict[d] = error[:10]
    return word_dict, pos_dict, dep_dict

