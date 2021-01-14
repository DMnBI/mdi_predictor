import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
import sys
import argparse

import preprocessing
import parsing
import postprocessing
import embedding
import model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_data', dest="train_data", required=True,
                        help="train data", metavar="FILE")
    parser.add_argument('--valid_data', dest="valid_data", required=True,
                        help="validation data", metavar="FILE")
    parser.add_argument('--resource_dir', dest="resource", required=True,
                        help="Directory with resource data", metavar="FILE")
    parser.add_argument('--model', dest="model", required=True,
                        help="model path", metavar="FILE",)
    parser.add_argument('--batch_size', dest="batch_size", 
                        default=64, type=int)
    parser.add_argument('--epochs', dest="epochs", default=50, type=int)
    
    args=parser.parse_args()

    train_file = args.train_data
    valid_file = args.valid_data
    
    print(train_file)

    train_data = preprocessing.get_data_from_textfile(train_file, 'train')
    valid_data = preprocessing.get_data_from_textfile(valid_file, 'valid')
    train_data = preprocessing.bacdis_preprocessing(train_data)
    valid_data = preprocessing.bacdis_preprocessing(valid_data)
    
    data = {}
    data.update(train_data)
    data.update(valid_data)
    del train_data
    del valid_data
    
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
    del data
    del word_dict
    del pos_dict
    del dep_dict
    
    my_model = model.make_model()
    train_feature, train_label, train_info = model.make_feature_label(embed_data, 'train')
    valid_feature, valid_label, valid_info = model.make_feature_label(embed_data, 'valid')
    del embed_data
    
    my_model.fit(train_feature, train_label, batch_size=args.batch_size, epochs=args.epochs, verbose=1)
    result = my_model.predict(valid_feature, batch_size=len(valid_label)) 
    p, r, f = model.evaluation(result, valid_label)
    my_model.save_weights(args.model)

