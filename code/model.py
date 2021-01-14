import os
import sys
import json
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Concatenate, LSTM, Bidirectional, Dropout, Reshape
from tensorflow.keras.activations import softmax
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras import backend as K

class entity_attention(tf.keras.Model):
    def call(self, x):
        merge = x[0]
        word = x[1]
        e1 = x[2]
        e2 = x[3]
        scaler = int(merge.shape[1])
        pretheta1 = K.batch_dot(word, e1, axes=[2,2])/2000
        pretheta1_re = K.reshape(pretheta1, (-1, merge.shape[1]))
        theta1 = softmax(pretheta1_re, axis=1)
        pretheta2 = K.batch_dot(word, e2, axes=[2,2])/2000
        pretheta2_re = K.reshape(pretheta2, (-1, merge.shape[1]))
        theta2 = softmax(pretheta2_re, axis=1)
        theta = (theta1+theta2)/2.0 * scaler
        theta_re = K.reshape(theta, (-1, merge.shape[1], 1))
        merge_att = merge * theta_re
        return merge_att

    def get_output_shape_for(self, input_shape):
        return (input_shape[0])

def make_model():
    e1_in = Input(shape=(1, 200))
    e2_in = Input(shape=(1, 200))

    seq1_word = Input(shape=(60, 200))
    seq1_other = Input(shape=(60, 40))
    seq1_in = Concatenate(axis=2)([seq1_word, seq1_other])
    seq1_att = entity_attention()([seq1_in, seq1_word, e1_in, e2_in])
    seq1_drop = Dropout(0.7)(seq1_att)
    seq1_out = Bidirectional(LSTM(100, return_sequences=False), merge_mode='concat')(seq1_drop)
    seq1_re = Reshape((1, 200))(seq1_out)

    seq2_word = Input(shape=(60, 200))
    seq2_other = Input(shape=(60, 40))
    seq2_in = Concatenate(axis=2)([seq2_word, seq2_other])
    seq2_att = entity_attention()([seq2_in, seq2_word, e1_in, e2_in])
    seq2_drop = Dropout(0.7)(seq2_att)
    seq2_out = Bidirectional(LSTM(100, return_sequences=False), merge_mode='concat')(seq2_drop)
    seq2_re = Reshape((1, 200))(seq2_out)

    seq3_word = Input(shape=(60, 200))
    seq3_other = Input(shape=(60, 40))
    seq3_in = Concatenate(axis=2)([seq3_word, seq3_other])
    seq3_att = entity_attention()([seq3_in, seq3_word, e1_in, e2_in])
    seq3_drop = Dropout(0.7)(seq3_att)
    seq3_out = Bidirectional(LSTM(100, return_sequences=False), merge_mode='concat')(seq3_drop)
    seq3_re = Reshape((1, 200))(seq3_out)

    shortest_word = Input(shape=(12, 200))
    shortest_other = Input(shape=(12, 40))
    shortest_in = Concatenate(axis=2)([shortest_word, shortest_other])
    shortest_att = entity_attention()([shortest_in, shortest_word, e1_in, e2_in])
    shortest_drop = Dropout(0.7)(shortest_att)
    shortest_out = Bidirectional(LSTM(100, return_sequences=False), merge_mode='concat')(shortest_drop)
    shortest_re = Reshape((1, 200))(shortest_out)
    
    top_in = Concatenate(axis=1)([seq1_re, e1_in, seq2_re, e2_in, seq3_re, shortest_re]) 
    top_out = Bidirectional(LSTM(100, return_sequences=False), merge_mode='concat')(top_in)
    top_drop = Dropout(0.5)(top_out)

    out = Dense(2, activation='softmax')(top_drop)
    
    model  = Model(inputs=[seq1_word, seq1_other, seq2_word, seq2_other, seq3_word, seq3_other, shortest_word, shortest_other, e1_in, e2_in], outputs=out)
    model.summary()
    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])
    return model

def evaluation(result, label):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for i in range(len(label)):
        if label[i][0] > label[i][1]:
            if result[i][0] > result[i][1]:
                true_positive += 1
            else:
                false_negative += 1
        else:
            if result[i][0] > result[i][1]:
                false_positive += 1
            else:
                true_negative += 1
    print('tp: ', true_positive, 'tn: ', true_negative, 'fp: ', false_positive, 'fn: ', false_negative)
    if true_positive + false_positive == 0.0:
        precision = 0.0
        recall = 0.0
        f_score = 0.0
    else:
        precision   = float(float(true_positive) / float(true_positive + false_positive))
        recall      = float(float(true_positive) / float(true_positive + false_negative))
        f_score     = float(2*precision*recall / float(precision + recall))
    print('precision: ', precision, ' recall: ', recall, ' fscore: ', f_score)
    return precision, recall, f_score

def make_feature_label(embed, data_name):
    index = []
    key = []
    if data_name == 'train':
        print('train')
        for idx in range(len(embed[12])):
            if embed[12][idx][:5] == 'train':
                key.append(embed[12][idx])
                index.append(embed[11][idx])
            else:
                None
    elif data_name == 'valid':
        print('valid')
        for idx in range(len(embed[12])):
            if embed[12][idx][:5] == 'valid':
                key.append(embed[12][idx])
                index.append(embed[11][idx])
            else:
                None
    elif data_name == 'test':
        for idx in range(len(embed[12])):
            if embed[12][idx][:4] == 'test':
                key.append(embed[12][idx])
                index.append(embed[11][idx])
            else:
                None
    else:
        None
    seq1w = []
    seq1w = []
    seq1w = []
    seq1f = []
    seq2w = []
    seq2f = []
    seq3w = []
    seq3f = []
    shortestw = []
    shortestf = []
    e1 = []
    e2 = []
    label = []
    for idx in index:
        seq1w.append(embed[0][idx])
        seq1f.append(embed[1][idx])
        seq2w.append(embed[2][idx])
        seq2f.append(embed[3][idx])
        seq3w.append(embed[4][idx])
        seq3f.append(embed[5][idx])
        shortestw.append(embed[6][idx])
        shortestf.append(embed[7][idx])
        e1.append(embed[8][idx])
        e2.append(embed[9][idx])
        label.append(embed[10][idx])
    seq1w = np.array(seq1w)
    seq1f = np.array(seq1f)
    seq2w = np.array(seq2w)
    seq2f = np.array(seq2f)
    seq3w = np.array(seq3w)
    seq3f = np.array(seq3f)
    shortestw = np.array(shortestw)
    shortestf = np.array(shortestf)
    e1 = np.array(e1)
    e2 = np.array(e2)
    label = np.array(label)
    return [seq1w, seq1f, seq2w, seq2f, seq3w, seq3f, shortestw, shortestf, e1, e2], label, [index, key]

