import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
import sys
import preprocessing
import parsing
import postprocessing
import embedding
import model
import argparse

def print_outdata(outdata, out_file):
    f = open(out_file, 'w')
    for row in outdata:
        text = ''
        for val in row:
            text += str(val) + '\t'
        text = text[:-1]
        f.write(text+'\n')
    f.flush()

def get_outdata_from_textfile(textfile):
    data = []
    f = open(textfile, 'r')
    while True:
        line = f.readline()
        line = line[:-1]
        if not line:
            break
        else:
            line = line.strip().split('\t')
            data.append(line)
    return data

def result_for_sentence(origin_key_list, result):
    sen_TF = {}
    key_list = []
    for idx in range(len(origin_key_list)):
        key_list.append(str(origin_key_list[idx][origin_key_list[idx].find('_')+1:origin_key_list[idx].rfind('.')]))
    for idx in range(len(key_list)):
        sen_TF[key_list[idx]] = [0,0] 
    for idx in range(len(key_list)):
        if result[idx][0] > result[idx][1]:
            sen_TF[key_list[idx]][0] += 1
        else:
            sen_TF[key_list[idx]][1] += 1
    '''
    for key in list(sen_TF.keys()):
        if sen_TF[key][0] > sen_TF[key][1]:
            sen_TF[key] = 'true'
        else:
            sen_TF[key] = 'false'
    '''
    for key in list(sen_TF.keys()):
        if sen_TF[key][0] >= 1:
            sen_TF[key] = 'true'
        else:
            sen_TF[key] = 'false'
    return sen_TF

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True,
            help='The input data. Should be in tagged sentence format (e.g. exmple_data/example.ner.txt).',
            metavar="FILE")
    parser.add_argument('--output', required=True,
            help="The output file where the RE result will be written.",
            metavar="FILE")
    parser.add_argument('--model',
            help="The model to be used for RE.",
            default="./models/model.h5",
            metavar="FILE")
    parser.add_argument('--resource_dir', dest='resource',
            help="The directory where resources are stored.",
            default="./resource/",
            metavar="DIR")
    args = parser.parse_args()
    
    test_file = args.input
    out_file = args.output

    data = preprocessing.get_data_from_textfile(test_file, 'test')
    data = preprocessing.bacdis_preprocessing(data)
    word_index_file = args.resource+'/word_index.json'
    word_index = preprocessing.get_word_index_file(word_index_file)

    parsed_data = parsing.merged_data(data)
    parsed_data = parsing.corpus_parsing(parsed_data)

    data = postprocessing.make_sequences(data, parsed_data)
    data = postprocessing.word_to_index(data, word_index)
    del parsed_data
    del word_index

    word_file = args.resource+'/vectorOfword.json'
    pos_file = args.resource+'/vectorOfpostag.json'
    dep_file = args.resource+'/vectorOfdeptag.json'
    word_dict, pos_dict, dep_dict = embedding.read_dict(word_file, pos_file, dep_file, data) 
    for key in list(data.keys()):
        data[key] = embedding.padding_feature(data[key])
    embed_data = embedding.data_embedding(data, word_dict, pos_dict, dep_dict)
    key_list = embed_data[12]
    del data
    del word_dict
    del pos_dict
    del dep_dict

    my_model = model.make_model()
    my_model.load_weights(args.model)
    test_feature, test_label, test_info = model.make_feature_label(embed_data, 'test')
    result = my_model.predict(test_feature, batch_size=len(test_label)) 
    sen_result = result_for_sentence(key_list, result)

    outdata = get_outdata_from_textfile(test_file)
    for idx in range(len(outdata)):
        try:
            own_result = sen_result[outdata[idx][0]]
        except:
            own_result = 'None'
        try:
            outdata[idx][2] = own_result
        except:
            outdata[idx].append(own_result)

    print_outdata(outdata, out_file)

