import os
import sys
import re
import json
import copy

def ne_clear(text):
    delimeter = re.search('(BAC00)[^ ]+', text)
    while(delimeter):
        s = delimeter.start()
        e = delimeter.end()
        entity = text[s:e]
        entity = re.sub('[^a-zA-Z0-9 ]+', ' ', entity)
        entity = re.sub('[ ]+', ' ', entity)
        entity = entity.replace(' ', '_')
        entity = entity.lower()
        text = text[:s]+entity+text[e:]
        delimeter = re.search('(BAC00)[^ ]+', text)
    delimeter = re.search('(DIS00)[^ ]+', text)
    while(delimeter):
        s = delimeter.start()
        e = delimeter.end()
        entity = text[s:e]
        entity = re.sub('[^a-zA-Z0-9 ]+', ' ', entity)
        entity = re.sub('[ ]+', ' ', entity)
        entity = entity.replace(' ', '_')
        entity = entity.lower()
        text = text[:s]+entity+text[e:]
        delimeter = re.search('(DIS00)[^ ]+', text)
    return text

def clear_text(text):
    text = ' '+text+' '
    delimeter = re.search('[^a-zA-Z0-9_ ]+[^ ]', text)
    while(delimeter):
        e = delimeter.end()
        text = text[:e-1]+' '+text[e-1:]
        delimeter = re.search('[^a-zA-Z0-9_ ]+[^ ]', text)
    delimeter = re.search('[^ ][^a-zA-Z0-9_ ]+', text)
    while(delimeter):
        s = delimeter.start()
        text = text[:s+1]+' '+text[s+1:]
        delimeter = re.search('[^ ][^a-zA-Z0-9_ ]+', text)
    delimeter = re.search('[ ][0-9 ]*[.][ ][0-9]+[ ]', text)
    while(delimeter):
        s = delimeter.start()
        e = delimeter.end()
        text = text[:s+1]+'float'+text[e-1:]
        delimeter = re.search('[ ][0-9 ]*[.][ ][0-9]+[ ]', text)
    delimeter = re.search('[ ][0-9]+[ ]', text)
    while(delimeter):
        s = delimeter.start()
        e = delimeter.end()
        text = text[:s+1]+'num'+text[e-1:]
        delimeter = re.search('[ ][0-9]+[ ]', text)
    text = text[1:-1]
    text = text.lower()
    return text

def bdi_clear(text):
    if str(text) == 'None':
        return {}
    bdi = {}
    bdi_list = text.strip().split(',')
    for l in bdi_list:
        row = l.strip().split('&')
        if len(row) != 3:
            continue
        entity0 = ' '+row[1]+' '
        entity0 = re.sub('[^a-zA-Z0-9 ]+', ' ', entity0)
        entity0 = re.sub('[ ]+', ' ', entity0)
        entity0 = entity0.replace(' ', '_')
        entity0 = entity0.lower()
        entity0 = entity0[1:-1]
        entity1 = ' '+row[0]+' '
        entity1 = re.sub('[^a-zA-Z0-9 ]+', ' ', entity1)
        entity1 = re.sub('[ ]+', ' ', entity1)
        entity1 = entity1.replace(' ', '_')
        entity1 = entity1.lower()
        entity1 = entity1[1:-1]
        bdi[entity0+' '+entity1] = 'true'
    return bdi

def get_pairs(origin_text, bdi, sid):
    pairs = {}
    text = origin_text.strip().split(' ')
    disease_cnt = 0
    disease_index = {}
    for idx in range(len(text)):
        has_dis00 = re.search('(dis00)', text[idx])
        if has_dis00:
            disease_index[str(disease_cnt)] = [idx, text[idx]]
            #text[idx] = 'disease'+str(disease_cnt)
            text[idx] = 'disease1'
            disease_cnt += 1
    bacteria_cnt = 0
    bacteria_index = {}
    for idx in range(len(text)):
        has_bac00 = re.search('(bac00)', text[idx])
        if has_bac00:
            bacteria_index[str(bacteria_cnt)] = [idx, text[idx]]
            #text[idx] = 'bacteria'+str(bacteria_cnt)
            text[idx] = 'bacteria1'
            bacteria_cnt += 1
    bdi_keys = list(bdi.keys())
    pair_cnt = 0
    for bacteria_key in list(bacteria_index.keys()):
        for disease_key in list(disease_index.keys()):
            pair_id = sid+'.p'+str(pair_cnt)
            pair_cnt += 1
            value = {}
            if len(bdi_keys) != 0:
                bdi_check = bacteria_index[bacteria_key][1]+' '+disease_index[disease_key][1]
                for bdi_key in bdi_keys:
                    if bdi_check == bdi_key:
                        value['bdi'] = 'true'
                        break
                    else:
                        value['bdi'] = 'false'
            else:
                value['bdi'] = 'false'
            pair_text = copy.deepcopy(text)
            pair_text[bacteria_index[bacteria_key][0]] = 'bacteria0'
            pair_text[disease_index[disease_key][0]] = 'disease0'
            #value['text'] = text
            value['text'] = pair_text
            bac_idx = bacteria_index[bacteria_key][0]
            dis_idx = disease_index[disease_key][0]
            if bac_idx < dis_idx:
                value['e1_index'] = bac_idx
                value['e2_index'] = dis_idx
            else:
                value['e1_index'] = dis_idx
                value['e2_index'] = bac_idx
            pairs[pair_id] = value
    return pairs

def bacdis_preprocessing(data):
    new_data = {}
    for sid in list(data.keys()):
        text = ne_clear(data[sid][0])
        text = clear_text(text)
        bdi = bdi_clear(data[sid][1])
        pairs = get_pairs(text, bdi, sid)
        for key in list(pairs.keys()):
            new_data[key] = pairs[key]
    return new_data

def get_word_index_file(file_name):
    with open(file_name, 'r') as json_file:    
        word_index = json.load(json_file)
    return word_index

def get_data_from_textfile(textfile, file_tag):
    data = {}
    f = open(textfile, 'r')
    while True:
        line = f.readline()
        line = line[:-1]
        if not line:
            break
        else:
            line = line.strip().split('\t')
            sid = line[0]
            sid = file_tag + '_' + sid
            text = line[1]
            try:
                result = line[2]
            except:
                result = "None"
            data[sid] = [text, result]
    return data

