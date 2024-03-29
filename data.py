# coding=utf-8
# @author: cer

import random
import numpy as np
import codecs
import pandas as pd
import copy


flatten = lambda l: [item for sublist in l for item in sublist]  # 二维展成一维
index_seq2slot = lambda s, index2slot: [index2slot[i] for i in s]
index_seq2word = lambda s, index2word: [index2word[i] for i in s]


def data_pipeline_musk(data, length=50):
    data = [t[:-1] for t in data]  # 去掉'\n'
    # 数据的一行像这样：'BOS i want to fly from baltimore to dallas round trip EOS
    # \tO O O O O O B-fromloc.city_name O B-toloc.city_name B-round_trip I-round_trip atis_flight'
    # 分割成这样[原始句子的词，标注的序列，intent]
    data = [[t.split("\t")[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]] for t in
            data]
    data = [[t[0][1:-1], t[1][1:], t[2]] for t in data]  # 将BOS和EOS去掉，并去掉对应标注序列中相应的标注
    seq_in, seq_out, intent = list(zip(*data))
    sin = []
    sout = []
    # padding，原始序列和标注序列结尾+<EOS>+n×<PAD>
    empty = list( np.full( length, "<PAD>" ) )
    for i in xrange( len( seq_in ) ):
        temp_in = copy.deepcopy(empty)
        temp_out = copy.deepcopy(empty)
        len_in = len(seq_in[i])
        len_out = len(seq_out[i])
        if len_in < length:
            temp_in[0:len_in] = seq_in[i][0:]
            temp_in[len_in] = "<EOS>"
        else:
            temp_in = seq_in[i][:length]
            temp_in[-1] = '<EOS>'
        sin.append(temp_in)

        if len_out < length:
            temp_out[0:len_out] = seq_out[i][0:]
            temp_out[len_out] = "<EOS>"
        else:
            temp_out = seq_out[i][:length]
            temp_out[-1] = '<EOS>'
        sout.append(temp_out)

        data = list(zip(sin, sout, intent))
    return data

def data_pipeline(data, length=50):
    data = [t[:-1] for t in data]  # 去掉'\n'
    # 数据的一行像这样：'BOS i want to fly from baltimore to dallas round trip EOS
    # \tO O O O O O B-fromloc.city_name O B-toloc.city_name B-round_trip I-round_trip atis_flight'
    # 分割成这样[原始句子的词，标注的序列，intent]
    data = [[t.split("\t")[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]] for t in
            data]
    data = [[t[0][1:-1], t[1][1:], t[2]] for t in data]  # 将BOS和EOS去掉，并去掉对应标注序列中相应的标注
    seq_in, seq_out, intent = list(zip(*data))
    sin = []
    sout = []
    # padding，原始序列和标注序列结尾+<EOS>+n×<PAD>
    for i in range(len(seq_in)):
        temp = seq_in[i]
        if len(temp) < length:
            temp.append('<EOS>')
            while len(temp) < length:
                temp.append('<PAD>')
        else:
            temp = temp[:length]
            temp[-1] = '<EOS>'
        sin.append(temp)

        temp = seq_out[i]
        if len(temp) < length:
            while len(temp) < length:
                temp.append('<PAD>')
        else:
            temp = temp[:length]
            temp[-1] = '<EOS>'
        sout.append(temp)
        data = list(zip(sin, sout, intent))
    return data


def get_info_from_training_data(data):
    seq_in, seq_out, intent = list(zip(*data))
    vocab = set(flatten(seq_in))
    slot_tag = set(flatten(seq_out))
    intent_tag = set(intent)
    
    # create new word2index and index2word

    vocab_file = codecs.open('word2index_calibrated.txt', 'r+')
    vocabs = vocab_file.readlines()

    vocab_count = 0
    word2index = {}
    for token in vocabs:
        word2index[token.strip()] = vocab_count
        vocab_count += 1

    # 生成word2index
    #word2index = {'<PAD>': 0, '<UNK>': 1, '<SOS>': 2, '<EOS>': 3}
    for token in vocab:
        if token not in word2index.keys():
            word2index[token] = len(word2index)
            token_filewrite = token + '\n'
            vocab_file.write(token_filewrite)
            vocab_count += 1
    vocab_file.close()


    # 生成index2word
    index2word = {v: k for k, v in word2index.items()}
   

    # 生成tag2index
    tag2index = {'<PAD>': 0, '<UNK>': 1, "O": 2}
    for tag in slot_tag:
        if tag not in tag2index.keys():
            tag2index[tag] = len(tag2index)

    # 生成index2tag
    index2tag = {v: k for k, v in tag2index.items()}

    # 生成intent2index
    intent2index = {'<UNK>': 0}
    for ii in intent_tag:
        if ii not in intent2index.keys():
            intent2index[ii] = len(intent2index)

    # 生成index2intent
    index2intent = {v: k for k, v in intent2index.items()}
    return word2index, index2word, tag2index, index2tag, intent2index, index2intent


def getBatch(batch_size, train_data):
    #print("JerryB len(train_data): {}".format(len(train_data)))

    random.shuffle(train_data)
    
    sindex = 0
    eindex = batch_size
    #JerryB +++
    if len(train_data) == 1:
        yield train_data[sindex:eindex]
    else:
        while eindex < len(train_data):
            batch = train_data[sindex:eindex]
            temp = eindex
            eindex = eindex + batch_size
            sindex = temp
            yield batch
    #JerryB ---

def getBatchUT(batch_size, train_data):
    #original getBatch, remove shuffle

    sindex = 0
    eindex = batch_size

    # change to 'less or equal then', otherwise it will miss the alst one
    while eindex <= len(train_data):
            batch = train_data[sindex:eindex]
            temp = eindex
            eindex = eindex + batch_size
            sindex = temp
            # print ('sindex: ' + str(sindex) + ', eindex: ' + str(eindex))
            yield batch

def to_index(train, word2index, slot2index, intent2index):
    new_train = []
    for sin, sout, intent in train:
        sin_ix = list(map(lambda i: word2index[i] if i in word2index else word2index["<UNK>"],
                          sin))
        true_length = sin.index("<EOS>")
        sout_ix = list(map(lambda i: slot2index[i] if i in slot2index else slot2index["<UNK>"],
                           sout))
        intent_ix = intent2index[intent] if intent in intent2index else intent2index["<UNK>"]
        new_train.append([sin_ix, true_length, sout_ix, intent_ix])
    return new_train

def to_index_musk(train, word2index, slot2index, intent2index):
    new_train = []
    for sin, sout, intent in train:
        sin_ix = list(map(lambda i: word2index[i] if i in word2index else word2index["<UNK>"],
                          sin))
        true_length = sin.index("<EOS>")
        sout_ix = list(map(lambda i: slot2index[i] if i in slot2index else slot2index["<UNK>"],
                           sout))
        intent_ix = intent2index[intent] if intent in intent2index else intent2index["<UNK>"]
        new_train.append([sin_ix, true_length, sout_ix, intent_ix])
    return new_train

def to_index_musk_ver_1(train, word2index, slot2index, intent2index):
    new_train = []
    for sin, sout, intent in train:
        sin_ix = list(map(lambda i: word2index[i] if i in word2index else word2index["<UNK>"],
                          sin))
        true_length = sin.index("<EOS>")
        sout_ix = list(map(lambda i: slot2index[i] if i in slot2index else slot2index["<UNK>"],
                           sout))
        intent_ix = intent2index[intent] if intent in intent2index else intent2index["<UNK>"]
        new_train.append([sin, true_length, sout_ix, intent_ix])
    return new_train
