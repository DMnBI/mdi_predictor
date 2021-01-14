import os
import sys
import stanza
import json

def text_parsing(text, parser):
    node_info   = []
    dependency_doc = parser(text)
    for sent in dependency_doc.sentences:
        for word in sent.words:
            node_info.append([word.text, word.id, word.xpos, word.head, word.deprel])
    return node_info

def corpus_parsing(data):
    new_data = {}
    cnt = 0
    parser  = stanza.Pipeline(tokenize_pretokenized=True, use_gpu=True, processors='tokenize,pos,lemma,depparse')
    for key in list(data.keys()):
        cnt += 1
        if cnt%1000 == 0:
            print(cnt)
        new_data[key] = text_parsing(data[key], parser)
    return new_data

def merged_data(data):
    merged_data = {}
    for key in list(data.keys()):
        sid = key[:key.rfind('.')]
        merged_data[sid] = ''
    for key in list(data.keys()):
        sid = key[:key.rfind('.')]
        if merged_data[sid] != '':
            None
        else:
            text = data[key]['text']
            sen = ''
            for word in text:
                sen += word + ' '
            sen = sen[:-1]
            merged_data[sid] = sen
    return merged_data

if __name__ == '__main__':
    with open('../preprocessing/data.json', 'r') as json_file:
        data = json.load(json_file)

    data = merged_data(data)
    parsed_data = corpus_parsing(data)

    with open('./parsed_data.json', 'w') as json_file:
        json.dump(parsed_data, json_file, indent=4, sort_keys=True)

