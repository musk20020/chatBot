#-*- coding:utf-8 -*-

import pandas as pd
import jieba

#data = pd.read_excel('redwine_train_set_musk.xlsx',sheet_name=0)
#sheet_name --> 讀取excel的第幾個分頁

data = pd.read_excel("Mr.Carson_Dialogue_Design_spec_Simple_Chinese_v0.1_musk.xlsx",sheet_name=1)
#data = pd.read_excel("redwine_test_data.xlsx",sheet_name=0)
library = pd.read_csv("entity_type_redwine.csv")

redwine_type = [tag.decode('utf-8') for tag in library.iloc[1:,1] if type(tag) != type(0.0)]
redwine_location = [tag.decode('utf-8') for tag in library.iloc[1:,2] if type(tag) != type(0.0)]
redwine_contry = [tag.decode('utf-8') for tag in library.iloc[1:,3] if type(tag) != type(0.0)]
redwine_year = [tag.decode('utf-8') for tag in library.iloc[1:,4] if type(tag) != type(0.0)]
redwine_variety = [tag.decode('utf-8') for tag in library.iloc[1:,5] if type(tag) != type(0.0)]
redwine_des = [tag.decode('utf-8') for tag in library.iloc[1:,6] if type(tag) != type(0.0)]
redwine_food = [tag.decode('utf-8') for tag in library.iloc[1:,7] if type(tag) != type(0.0)]
redwine_page = [tag.decode('utf-8') for tag in library.iloc[1:,8] if type(tag) != type(0.0)]
redwine_function = [tag.decode('utf-8') for tag in library.iloc[1:,9] if type(tag) != type(0.0)]

jieba.set_dictionary
jieba.load_userdict(redwine_type)
jieba.load_userdict(redwine_location)
jieba.load_userdict(redwine_contry)
jieba.load_userdict(redwine_year)
jieba.load_userdict(redwine_variety)
jieba.load_userdict(redwine_des)
jieba.load_userdict(redwine_food)
jieba.load_userdict(redwine_page)
jieba.load_userdict(redwine_function)


f = open('redwine_training_data_musk.iob', 'w')

sentence = data.iloc[:,1]
utts = [" ".join(jieba.cut(tag.encode("utf-8"))) if type(tag)==type(u"unicode") else unicode(tag) for tag in sentence ]
#print(" ".join(jieba.cut(data.iloc[1,1])))
count = 0
for utt in utts:
    utt = u"BOS " + utt
    entity = []
    for word in utt.split(u" "):
        if word in redwine_type:
            entity.append(u"B-酒种类")
        elif word in redwine_location:
            entity.append( u"B-产区" )
        elif word in redwine_contry:
            entity.append( u"B-国家" )
        elif word in redwine_year:
            entity.append( u"B-年份" )
        elif word in redwine_variety:
            entity.append( u"B-葡萄品种" )
        elif word in redwine_des:
            entity.append( u"B-酒属性" )
        elif word in redwine_food:
            entity.append( u"B-食物" )
        elif word in redwine_page:
            entity.append( u"B-页面" )
        elif word in redwine_function:
            entity.append( u"B-功能" )
        else:
            entity.append( u"O" )

    entity_out = u" ".join(entity)
    output = utt.encode("utf-8") + " EOS" + "\t"+ entity_out.encode("utf-8") + " " + data.iloc[count,2].encode("utf-8") + "\n"
    f.write(output)
    count += 1
    print(output)






'''
Entity_list = ['红酒','白酒','葡萄酒','波尔多','义大利','2013','2016','海鲜'
             ,'最好','最贵','最近','梅洛','市集页','活动','首页','控制板'
             ,'念出酒名']
Entity_Label_list = ['B-酒种类','B-酒种类','B-酒种类','B-产区','B-产区','B-年份','B-年份','B-食物'
             ,'B-酒属性','B-酒属性','B-酒属性','B-葡萄品种','B-页面','B-页面','B-页面','B-页面'
             ,'B-功能']

def get_slot_type_ground_truth(sentance, entity_list, entity_label_list):
    output_list = list()
    output_string = ''
    for word in sentance:
        word = word.encode('utf-8')
        if word in entity_list:
            label = entity_label_list[entity_list.index(word)]

            # List Version
            #output_list.append(label)
            # String Version
            output_string = output_string + str(label) + ' '

        else:
            #output_list.append('O')
            output_string = output_string + 'O '
    return output_string

utterance = ""
intent = ""
entity = ""

print(data.values[283][0])
for i in range(0, len(data)):
    utterance = data.values[i][0]
    intent = data.values[i][1]
    entity = data.values[i][2]

    slot_type_list = []
    slot_value_list = []

    if type(entity) == float:
        print("entity是空的")
    else:
        slot = entity.split(';')
        #slot --> [u'somword', u''] --> len=2

        for j in range(0, (len(slot)-1)):

            slot_temp = slot[j].split(',')

            slot_type_list.append(slot_temp[0])
            slot_value_list.append(slot_temp[1])

    utterance_temp = utterance.split(' ')
    if type(utterance_temp) == int :
        utterance_temp = str(utterance_temp)
    slot_type_ground_truth = get_slot_type_ground_truth( utterance_temp[1:-1], Entity_list, Entity_Label_list )

    # slot_format = ""
    # entity_temp = ""
    # for k in range(0, (len(utterance_temp)-1)):
    #     if type(entity) == float:
    #         entity_temp = "O "
    #     else:
    #         for slot_num in range(0, len(slot_type_list)):
    #             if slot_value_list[slot_num] == utterance_temp[k]:
    #                 entity_temp = "B-" + slot_type_list[slot_num] + " "
    #                 break
    #             else:
    #                 entity_temp = "O "
    #     slot_format = slot_format + entity_temp
    # print("slot_format: ") + slot_format
    # #iob_format = utterance + "\t" + slot_format + intent + "\n"

    iob_format = utterance.encode('utf-8') + "\t" + 'O ' + slot_type_ground_truth + intent.encode('utf-8') + "\n"

    print("iob_format: ") + iob_format
    f.write(iob_format)

f.close()
'''