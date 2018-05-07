#encoding=utf-8

import re
import random
import copy
import openpyxl
import pandas as pd

shop_list = list()
locate_list = list()
type_list = list()
food_list = list()
mrt_list = list()
build_list = list()
other_list = list()
training_data = open("ijia_dataset_musk.iob", "r").readlines()
training_data_expend = open("ijia_dataset_musk_expend.iob", "w")
other_type_data = open("./dataset/ijia_dataset_othertype.iob","r").readlines()

file = "entity_type.xlsx"

#entity_type =openpyxl.load_workbook(file)
#sheets = entity_type.sheetnames
#sheet1 = sheets[1]
#ws = entity_type.get_sheet_by_name(sheet1)

data = pd.read_csv("entity_type_add_sentance.csv")
print(data.iloc[1:20,4])
l = len(data)
def add_sentance(list, label):
    print("========== 正在處理 " + label + " ===========")
    for i in range(1,21):
        if data.iloc[0,i] == label:
            ws_colum = i
            #print(i)
            break
    else:
        print("no label match")

    for row in range(1,l):
        if row%500 == 0:
            print("已處理 " +str(row)+" 筆資料")

        word = data.iloc[row,ws_colum]
        if type(word) != type(0.0):
            sentance_index = random.randint(0,len(list)-1)
            word_index = list[sentance_index][1].index(label)
            #expend_sentance = copy.deepcopy( list[sentance_index] )
            expend_sentance = copy.deepcopy(list[sentance_index])
            expend_sentance[0][word_index] = word

            a = " ".join( expend_sentance[0] )
            b = " ".join( expend_sentance[1] )
            s = a + "\t" + b + " " + expend_sentance[2]

            training_data_expend.write( s )
        else:
            break

'''
def add_single_entity_sentence(entity,intent):
    for i in range(1,21):
        if data.iloc[0,i] == entity:
            ws_colum = i
            #print(i)
            break
    else:
        print("no label match")

    for row in range(1,l):
        if row%500 == 0:
            print("已處理 " +str(row)+" 筆資料")

        word = data.iloc[row,ws_colum]
        if type(word) != type(0.0):


            a = "BOS " + word + " EOS"
            b = "O " + entity
            s = a + "\t" + b + " " + intent + "\n"

            training_data_expend.write( s )
        else:
            break
'''

def add_single_entity_sentence(entity,intent,samelabel=1):

    if samelabel:
        label = entity
    else:
        label = "O"

    for i in range(1,21):
        if data.iloc[0,i] == entity:
            ws_colum = i
            #print(i)
            break
    else:
        print("no label match")

    for row in range(1,l):
        if row%500 == 0:
            print("已處理 " +str(row)+" 筆資料")

        word = data.iloc[row,ws_colum]
        if type(word) != type(0.0):


            a = "BOS " + word + " EOS"
            b = "O " + label
            s = a + "\t" + b + " " + intent + "\n"

            training_data_expend.write( s )
        else:
            break

for t in training_data:
    #train_data = re.sub("\n", "", line).sub("\t", " ", line).split(" ")
    train_data = [t.split( "\t" )[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]]

    if train_data[2] == "找餐廳\n":
        if "B-餐廳需求::地點" in train_data[1]:
            locate_list.append(train_data)
        if "B-餐廳需求::地標" in train_data[1]:
            build_list.append(train_data)
        if "B-餐廳需求::捷運站" in train_data[1]:
            mrt_list.append(train_data)
        if "B-餐廳需求::店名" in train_data[1]:
            shop_list.append(train_data)
        if "B-餐廳需求::餐點" in train_data[1]:
            food_list.append(train_data)
        if "B-餐廳需求::類型" in train_data[1]:
            type_list.append(train_data)
    else:
        other_list.append(train_data)

curse_list = list()
hello_list = list()
for t in other_type_data:
    othertype_data =[t.split( "\t" )[0].split(" "), t.split("\t")[1].split(" ")[:-1], t.split("\t")[1].split(" ")[-1]]

    if "B-對罵" in othertype_data[1]:
        curse_list.append(othertype_data)
    if "B-打招呼" in othertype_data[1]:
        hello_list.append(othertype_data)

add_sentance(shop_list,"B-餐廳需求::店名")
add_sentance(type_list,"B-餐廳需求::類型")
add_sentance(food_list,"B-餐廳需求::餐點")
add_sentance(locate_list,"B-餐廳需求::地點")
#add_sentance(build_list,"B-餐廳需求::地標")
#add_sentance(mrt_list,"B-餐廳需求::捷運站")
#add_sentance(curse_list,"B-對罵")
#add_sentance(hello_list,"B-打招呼")
add_single_entity_sentence("B-餐廳需求::店名","找餐廳")
add_single_entity_sentence("B-餐廳需求::類型","找餐廳")
add_single_entity_sentence("B-餐廳需求::餐點","找餐廳")
add_single_entity_sentence("B-餐廳需求::地點","找餐廳")
add_single_entity_sentence("B-狀態::肯定","肯定句",0)
add_single_entity_sentence("B-狀態::否定","否定句",0)
for i in other_list:
    a = " ".join( i[0] )
    b = " ".join( i[1] )
    s = a + "\t" + b + " " + i[2]

    training_data_expend.write( s )
