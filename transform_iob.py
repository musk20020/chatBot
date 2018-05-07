#-*- coding:utf-8 -*-

import pandas as pd

#data = pd.read_excel('ijia_test.xls',sheetname='Sheet1')
# data = pd.read_excel('iob_out.xls',sheetname='jieba_sheet')


#print("len data:", len(data))

# f = open('ijia_dataset.iob', 'w')

data = pd.read_excel('./utterance/primary_seg_out.xls',sheetname='jieba_sheet')
f = open('ijia_primiry130.iob', 'w')

utterance = ""
intent = ""
entity = ""

for i in range(0, len(data)):
#for i in range(0, 1):
    utterance = data.values[i][1]
    intent = data.values[i][2]
    entity = data.values[i][3]

    #print("utterance: ") + utterance
    #print("intent: ") + intent
    #print("entity: ") + entity

    slot_type_list = []
    slot_value_list = []

    if type(entity) == float:
        print("entity是空的")
    else:
        slot = entity.split(';')



        #print("len slot: ", len(slot))
        for j in range(0, (len(slot)-1)):
            #print("j: ", j)
            #print("slot: ") + slot[j]

            slot_temp = slot[j].split(',')
            #print("slot_temp: ") + slot_temp[0]

            slot_type_list.append(slot_temp[0])
            slot_value_list.append(slot_temp[1])
            #slot_type = slot_temp[0]
            #slot_value = slot_temp[1]

            #print("slot_type_list: ") + slot_type_list[j]
            #print("slot_value_list: ") + slot_value_list[j]

            #slot_type = slot_temp[0]
            #slot_value = slot_temp[1]

            #print("slot_type: ") + slot_type
            #print("slot_value: ") + slot_value

    utterance_temp = utterance.split(' ')
    #print("len utterance_temp: ", len(utterance_temp))

    slot_format = ""
    entity_temp = ""
    for k in range(0, (len(utterance_temp)-1)):
        if type(entity) == float:
            entity_temp = "O "
        else:
            for slot_num in range(0, len(slot_type_list)):
                if slot_value_list[slot_num] == utterance_temp[k]:
                    entity_temp = "B-" + slot_type_list[slot_num] + " "
                    break
                else:
                    entity_temp = "O "
        slot_format = slot_format + entity_temp
    print("slot_format: ") + slot_format


    iob_format = utterance + "\t" + slot_format + intent + "\n"
    print("iob_format: ") + iob_format
    f.write(iob_format.encode('utf-8'))

f.close()
