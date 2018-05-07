# coding=utf-8
import tensorflow as tf
from data import *
# from model import Model
from model import Model
from model_musk_ver_1 import Model_musk
from my_metrics import *
from tensorflow.python import debug as tf_debug
import numpy as np
import jieba
from flask import Flask
from flask import request
import json
import requests
import cgi
import pandas

#a = requests.post("http://52.224.222.139:80")

app = Flask(__name__)

input_steps = 50
embedding_size = 4819
hidden_size = 150
batch_size = 1
vocab_size = 42452
slot_size = 12
intent_size = 5
epoch_num = 1
n_layers = 2

model_path = './model/ijia/'
#model_path = '/var/www/demoapp/test-app/model/ijia/'

def transform(inputs_strs):
    utterance_temp = inputs_strs.split( ' ' )

    # print("len utterance_temp: ", len(utterance_temp))

    slot_format = ""
    for i in range( 0, (len( utterance_temp ) - 1) ):
        slot_format = slot_format + "O "

    iob_format = inputs_strs + "\t" + slot_format + "<UNK>"
    # print("iob_format: ") + str(iob_format).decode('string_escape')
    # print ('iob_format: '+ iob_format)

    return iob_format

def get_model():
    model = Model_musk( input_steps, embedding_size, hidden_size, vocab_size, slot_size,
                   intent_size, epoch_num, batch_size, n_layers )
    model.build()

    return model

@app.route('/BuildModel', methods=['POST'])
def build_model():

    error_message = 'build model success'
    try:
        global model_run, sess
        model_run = get_model()
        sess = tf.Session()
        sess.run( tf.global_variables_initializer() )
    except:
        error_message = 'get model error'

    try:
        # JerryB +++ 建立 saver 物件
        saver = tf.train.Saver( tf.global_variables() )
        ckpt = tf.train.get_checkpoint_state( model_path )
        saver.restore( sess, ckpt.model_checkpoint_path )
        # JerryB ---
    except:
        error_message = 'get saver error'

    try:
        train_data = open( "./dataset/redwine_dataset_musk_expend.iob", "r" ).readlines()
        train_data_ed = data_pipeline( train_data )

        global word2index, index2word, slot2index, index2slot, intent2index, index2intent
        word2index, index2word, slot2index, index2slot, intent2index, index2intent = \
            get_info_from_training_data( train_data_ed )
    except:
        error_message = 'get dataset error'

    try:
        # Musk_embedding +++
        global word_dic
        word_list = pd.read_csv( "word_list.csv" )
        word_dic = {}

        num = 0
        # a = word_list.iloc[:,3]
        for i in word_list.iloc[:, 4]:
            word_dic[i.decode( "utf-8" )] = num
            num += 1
        for i in range( 0, 10 ):
            word_dic[str( i )] = num
            num += 1
        word_dic[u"non"] = num

        #index_train = to_index_musk_ver_1( train_data_ed, word2index, slot2index, intent2index )
        #index_test = to_index_musk_ver_1( test_data_ed, word2index, slot2index, intent2index )
        # Musk_embedding ---
    except:
        error_message = 'read word_list error'

    return error_message

@app.route('/LoadDict', methods=['POST'])
def load_dict():
    try:
        jieba.set_dictionary

        #jieba_dict = "/var/www/demoapp/test-app/dict.txt"
        redwine_dict = "entity_type.txt"
        #corpus_dict = "/var/www/demoapp/test-app/corpus_jieba.txt"
        jieba.load_userdict( redwine_dict )
        error_message = "load dict seccess"
    except:
        error_message = "get something error when laod dict"
    return error_message

@app.route('/GetIntentEntity', methods=['POST'])
def get_intent_entity():
    #print(request)
    #inputs_strs = request.form["input_str"]

    return_dict = {'slot': "", 'intent': "",
                   'intent_acc': "", 'entity_output': "",
                   'error_message':""}
    try:
        inputs_strs = json.loads(request.data)['input_str']
    except:
        return_dict['error_message'] = 'load json error'

    try:
        test_data = []
        action = False

        input_seg = ('BOS ' + ' '.join( jieba.cut( inputs_strs ) ) + ' EOS').encode( 'utf-8' )

        iob_format = transform( input_seg )
        test_data = []
        test_data.append( iob_format )

        test_data_ed = data_pipeline( test_data )

        index_test = to_index_musk_ver_1( test_data_ed, word2index, slot2index, intent2index )
    except:
        return_dict['error_message'] = 'sentence process error'

    try:
        # 每训一个epoch，测试一次
        decoder_prediction, intent, intent_accuracy = model_run.step( sess, "test", index_test, word_dic )
        decoder_prediction = np.transpose( decoder_prediction, [1, 0] )
        sen_len = index_test[0][1]

        sentence_list = index_test[0][0][:sen_len]
        entity_list = index_seq2slot( decoder_prediction[0], index2slot )[:sen_len]
        Input_Sentence = " ".join(sentence_list)
        Slot_Prediction = " ".join([tag.decode( "utf-8" ) for tag in entity_list])
        entity_output = u""
        for n in range(sen_len):
            if entity_list[n] != 'O':
                #entity_output.append(entity_list[n] +',' + sentence_list[n] + ';')
                entity_output = entity_output + entity_list[n].decode('utf-8') + u',' + sentence_list[n].decode('utf-8') + u';'
        #entity_output = "".join(entity_output)
        Intent_Prediction = str(index2intent[intent[0]]).decode("utf-8")
    except:
        return_dict['error_message'] = 'predict error'

    return_dict = {'slot':Slot_Prediction,'intent':Intent_Prediction,'intent_acc':str(intent_accuracy).decode("utf-8"),'entity_output':entity_output}
    return_form = json.dumps(return_dict,ensure_ascii=False)

    return return_form

@app.route('/')
def HelloWorld():
    return "Hello world !!!"

if __name__ == '__main__':
    # jieba dict
    app.run()
    #app.run(host='0.0.0.0',port=8080)
